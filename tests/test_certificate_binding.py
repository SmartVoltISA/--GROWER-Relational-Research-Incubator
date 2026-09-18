import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from assembler import Component, VerificationCertificate, assemble, _CERTIFICATE_ISSUER
from grower_core import Status

def test_certificate_cycle_mismatch_blocked():
    cert=VerificationCertificate("CYCLE-A","E","fp",_CERTIFICATE_ISSUER)
    try:
        assemble([Component("C",Status.SUPPORTED,("E",),"math",certificate=cert,cycle_id="CYCLE-B")],"T")
    except PermissionError:
        pass
    else:
        raise AssertionError("cross-cycle certificate reuse accepted")
