"""Minimal deterministic Ω-GROWER state core."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import hashlib
import json
from evidence_gate import evaluate as evaluate_evidence
from boundary_gate import BoundaryDecision, _BOUNDARY_DECISION_ISSUER

class Status(str, Enum):
    CANDIDATE="CANDIDATE"; TESTING="TESTING"; SUPPORTED="SUPPORTED"; PARTIAL="PARTIAL"
    NOT_PROVEN="NOT_PROVEN"; FAIL="FAIL"; INVALID="INVALID"; ARCHIVED="ARCHIVED"

@dataclass(frozen=True)
class Relation:
    source:str; relation:str; target:str; value:Any=None; provenance:str=""

@dataclass
class Hypothesis:
    id:str; claim:str; null_hypothesis:str; predictions:list[str]=field(default_factory=list); status:Status=Status.CANDIDATE

@dataclass
class GrowthCycle:
    cycle_id:str; goal:str; relations:list[Relation]=field(default_factory=list)
    hypotheses:list[Hypothesis]=field(default_factory=list); evidence:list[dict[str,Any]]=field(default_factory=list)
    status:Status=Status.CANDIDATE
    _evidence_issuer:object=field(default_factory=object,init=False,repr=False)
    _locked_fingerprint:str|None=field(default=None,init=False,repr=False)

    def __setattr__(self,name:str,value:Any)->None:
        if name=="status" and hasattr(self,"status"): raise AttributeError("status is controlled by GrowthCycle transitions")
        object.__setattr__(self,name,value)
    def _set_status(self,status:Status)->None: object.__setattr__(self,"status",status)
    def add_hypothesis(self,hypothesis:Hypothesis)->None:
        if any(h.id==hypothesis.id for h in self.hypotheses): raise ValueError(f"duplicate hypothesis: {hypothesis.id}")
        self.hypotheses.append(hypothesis)
    def lock_for_testing(self)->None:
        if self.status not in {Status.CANDIDATE,Status.PARTIAL,Status.NOT_PROVEN}: raise ValueError(f"cannot start testing from state {self.status}")
        if not self.goal.strip(): raise ValueError("goal is required")
        if not self.relations: raise ValueError("at least one relation is required")
        if len(self.hypotheses)<2: raise ValueError("at least two competing hypotheses are required")
        if any(not h.null_hypothesis.strip() for h in self.hypotheses): raise ValueError("every hypothesis requires a null hypothesis")
        locked={"cycle_id":self.cycle_id,"goal":self.goal,"relations":[r.__dict__ for r in self.relations],"hypotheses":[h.__dict__ for h in self.hypotheses]}
        object.__setattr__(self,"_locked_fingerprint",hashlib.sha256(json.dumps(locked,sort_keys=True,default=str,separators=(",",":")).encode()).hexdigest())
        self._set_status(Status.TESTING)
    def _inputs_unchanged(self)->bool:
        locked={"cycle_id":self.cycle_id,"goal":self.goal,"relations":[r.__dict__ for r in self.relations],"hypotheses":[h.__dict__ for h in self.hypotheses]}
        current=hashlib.sha256(json.dumps(locked,sort_keys=True,default=str,separators=(",",":")).encode()).hexdigest()
        return current==self._locked_fingerprint
    def record_evidence(self,record:dict[str,Any])->None:
        if self.status not in {Status.TESTING,Status.PARTIAL,Status.NOT_PROVEN}: raise ValueError(f"cannot add evidence in state {self.status}")
        if record.get("type")=="test_result": raise PermissionError("test results must enter through record_test_result")
        self.evidence.append(dict(record))
    def record_test_result(self,record:dict[str,Any],*,boundary_status:BoundaryDecision)->str:
        if self.status not in {Status.TESTING,Status.PARTIAL,Status.NOT_PROVEN}: raise ValueError(f"cannot record test result in state {self.status}")
        if not isinstance(record.get("evidence_id"),str) or not record["evidence_id"].strip(): raise ValueError("evidence_id is required for test results")
        if not isinstance(boundary_status,BoundaryDecision): raise TypeError("record_test_result requires a BoundaryDecision from boundary_gate")
        if boundary_status._issuer is not _BOUNDARY_DECISION_ISSUER: raise PermissionError("untrusted boundary decision")
        evidence_status=evaluate_evidence(record)
        entry=dict(record); entry.update({"type":"test_result","evidence_status":evidence_status,"boundary_status":boundary_status.status,"_cycle_id":self.cycle_id,"_evidence_issuer":self._evidence_issuer})
        canonical = {k: v for k, v in entry.items() if k not in {'_evidence_issuer', '_fingerprint'}}
        entry['_fingerprint'] = hashlib.sha256(json.dumps(canonical, sort_keys=True, default=str, separators=(',', ':')).encode()).hexdigest()
        self.evidence.append(entry); return evidence_status
    def decide(self,status:Status,reason:str)->None:
        allowed={Status.SUPPORTED,Status.PARTIAL,Status.NOT_PROVEN,Status.FAIL,Status.INVALID,Status.ARCHIVED}
        if status not in allowed: raise ValueError(f"invalid terminal decision: {status}")
        if self.status in {Status.SUPPORTED,Status.FAIL,Status.INVALID,Status.ARCHIVED}: raise ValueError(f"terminal cycle cannot transition from {self.status}")
        if not reason.strip(): raise ValueError("decision reason is required")
        if status is Status.SUPPORTED:
            if not self._inputs_unchanged(): raise PermissionError("locked cycle inputs were modified")
            supported=any(e.get("type")=="test_result" and e.get("evidence_status")=="SUPPORTED" and e.get("boundary_status")=="ADMISSIBLE" and e.get("_cycle_id")==self.cycle_id and e.get("_evidence_issuer") is self._evidence_issuer and e.get("_fingerprint")==hashlib.sha256(json.dumps({k:v for k,v in e.items() if k not in {'_evidence_issuer','_fingerprint'}}, sort_keys=True, default=str, separators=(',', ':')).encode()).hexdigest() and evaluate_evidence(e)=="SUPPORTED" for e in self.evidence)
            if not supported: raise PermissionError("SUPPORTED requires a centrally evaluated evidence result and ADMISSIBLE boundary")
        self.evidence.append({"type":"decision","status":status.value,"reason":reason}); self._set_status(status)

# Evidence mutation hardening review: see security tests.
