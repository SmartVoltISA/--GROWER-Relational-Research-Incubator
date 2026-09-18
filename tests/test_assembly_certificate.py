import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from assembler import Component, VerificationCertificate, assemble
from grower_core import Status

def test_assembly_without_certificate_is_blocked():
    try: assemble([Component("C", Status.SUPPORTED, ("E",), "x")], "T")
    except ValueError: pass
    else: raise AssertionError("assembly accepted without certificate")

def test_forged_certificate_issuer_is_blocked():
    cert=VerificationCertificate("CYCLE", "E", object())
    try: assemble([Component("C", Status.SUPPORTED, ("E",), "x", certificate=cert)], "T")
    except PermissionError: pass
    else: raise AssertionError("forged certificate was accepted")

def test_certificate_evidence_must_match_component():
    from assembler import _CERTIFICATE_ISSUER
    cert=VerificationCertificate("CYCLE", "OTHER", _CERTIFICATE_ISSUER)
    try: assemble([Component("C", Status.SUPPORTED, ("E",), "x", certificate=cert)], "T")
    except PermissionError: pass
    else: raise AssertionError("certificate evidence mismatch was accepted")
