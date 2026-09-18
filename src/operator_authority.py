"""External operator authority for protected GROWER boundary changes.

The incubator never treats a boolean flag as proof of human authority.
Authorization is explicit, externally proven, target-bound and one-shot.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable


class ProtectedTarget(str, Enum):
    GROWTH_BOUNDARY = "GROWTH_BOUNDARY"


@dataclass(frozen=True)
class SurgeryRequest:
    change_id: str
    target: ProtectedTarget
    operator_id: str
    request_id: str
    confirmed: bool = False


@dataclass(frozen=True)
class SurgeryAuthorization:
    token_id: str
    change_id: str
    target: ProtectedTarget
    operator_id: str
    request_id: str
    _issuer: object


class OperatorAuthority:
    def __init__(self, proof_verifier: Callable[[str, SurgeryRequest], bool]):
        if not callable(proof_verifier):
            raise TypeError("proof_verifier must be callable")
        self._verify = proof_verifier
        self._issuer = object()
        self._counter = 0
        self._tokens: dict[str, SurgeryAuthorization] = {}

    def authorize(self, request: SurgeryRequest, external_proof: str) -> SurgeryAuthorization:
        if not request.confirmed:
            raise PermissionError("explicit operator confirmation is required")
        if not self._verify(external_proof, request):
            raise PermissionError("operator proof rejected")
        self._counter += 1
        token = SurgeryAuthorization(
            token_id=f"SURGERY-{self._counter}",
            change_id=request.change_id,
            target=request.target,
            operator_id=request.operator_id,
            request_id=request.request_id,
            _issuer=self._issuer,
        )
        self._tokens[token.token_id] = token
        return token

    def consume(self, token: SurgeryAuthorization, request: SurgeryRequest) -> None:
        if token._issuer is not self._issuer:
            raise PermissionError("authorization issued by another authority")
        current = self._tokens.get(token.token_id)
        if current != token:
            raise PermissionError("authorization missing, consumed or invalid")
        if (token.change_id, token.target, token.operator_id, token.request_id) != (
            request.change_id, request.target, request.operator_id, request.request_id
        ):
            raise PermissionError("authorization binding mismatch")
        del self._tokens[token.token_id]
