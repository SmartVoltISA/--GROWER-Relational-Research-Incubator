import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from operator_authority import OperatorAuthority, ProtectedTarget, SurgeryRequest
from boundary_gate import evaluate


def verifier(proof, request):
    return proof == "VALID" and request.operator_id == "operator-1"


def valid_candidate():
    return {
        "falsification_attempted": True,
        "controls_pass": True,
        "uncertainty_reported": True,
    }


def test_boundary_change_requires_external_operator_authority():
    request = SurgeryRequest("C-1", ProtectedTarget.GROWTH_BOUNDARY, "operator-1", "R-1", True)
    authority = OperatorAuthority(verifier)
    token = authority.authorize(request, "VALID")
    assert evaluate({**valid_candidate(), "boundary_change_proposed": True},
                    operator_authority=authority,
                    operator_authorization=token,
                    surgery_request=request).status == "ADMISSIBLE"


def test_boundary_authorization_is_one_shot():
    request = SurgeryRequest("C-2", ProtectedTarget.GROWTH_BOUNDARY, "operator-1", "R-2", True)
    authority = OperatorAuthority(verifier)
    token = authority.authorize(request, "VALID")
    candidate = {**valid_candidate(), "boundary_change_proposed": True}
    assert evaluate(candidate, operator_authority=authority,
                    operator_authorization=token, surgery_request=request).status == "ADMISSIBLE"
    assert evaluate(candidate, operator_authority=authority,
                    operator_authorization=token, surgery_request=request).status == "FAIL"


def test_invalid_operator_proof_is_rejected():
    request = SurgeryRequest("C-3", ProtectedTarget.GROWTH_BOUNDARY, "operator-1", "R-3", True)
    authority = OperatorAuthority(verifier)
    try:
        authority.authorize(request, "INVALID")
    except PermissionError:
        pass
    else:
        raise AssertionError("invalid proof was accepted")
