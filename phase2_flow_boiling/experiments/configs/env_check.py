"""Phase 2 환경 점검 스크립트 — 실행: python env_check.py"""
from __future__ import annotations
import sys

PASS, FAIL = "✅", "❌"

def check_python() -> bool:
    v = sys.version_info
    ok = v >= (3, 10)
    print(f"Python {v.major}.{v.minor}.{v.micro} {PASS if ok else FAIL + ' (3.10+ required)'}")
    return ok

def check_torch() -> bool:
    try:
        import torch
        mps = torch.backends.mps.is_available()
        print(f"torch {torch.__version__} {PASS}  MPS={'on' if mps else 'off'}")
        return True
    except ImportError:
        print(f"torch {FAIL}")
        return False

def check_coolprop() -> bool:
    try:
        from CoolProp.CoolProp import PropsSI
        fluids = ["Water", "R134a", "R1234yf", "R1234ze(E)", "R32", "R1233zd(E)"]
        for f in fluids:
            T = PropsSI("T", "P", 101325, "Q", 0, f) - 273.15
        print(f"CoolProp {PASS}  {len(fluids)} fluids verified")
        return True
    except Exception as e:
        print(f"CoolProp {FAIL}: {e}")
        return False

def check_mlflow() -> bool:
    try:
        import mlflow
        print(f"mlflow {mlflow.__version__} {PASS}")
        return True
    except ImportError:
        print(f"mlflow {FAIL}")
        return False

def check_others() -> bool:
    pkgs = [("numpy", "numpy"), ("scipy", "scipy"), ("pandas", "pandas"),
            ("optuna", "optuna"), ("matplotlib", "matplotlib")]
    ok = True
    for name, mod in pkgs:
        try:
            m = __import__(mod)
            print(f"  {name} {m.__version__} {PASS}")
        except ImportError:
            print(f"  {name} {FAIL}")
            ok = False
    return ok

if __name__ == "__main__":
    print("=" * 50)
    print("Phase 2 환경 점검")
    print("=" * 50)
    results = [
        check_python(),
        check_torch(),
        check_coolprop(),
        check_mlflow(),
        check_others(),
    ]
    print("=" * 50)
    if all(results):
        print("전체 점검 통과 ✅ — Phase 2 준비 완료")
    else:
        print("일부 점검 실패 ❌ — requirements.txt 재설치 권장")
