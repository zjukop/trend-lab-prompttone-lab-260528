from prompttone_lab.main import patch_prompt, run_benchmark


def test_smoke_run_benchmark():
    rows = run_benchmark("Say hello")
    assert len(rows) == 4
    assert {r["tone"] for r in rows} == {"authoritarian", "neutral", "empathetic", "coaching"}


def test_smoke_patch_prompt():
    patched = patch_prompt("Do this now and don't fail")
    assert patched.lower().startswith("please help")
