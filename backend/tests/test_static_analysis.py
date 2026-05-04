from app.services.static_analysis import run_static_analysis


def test_reports_syntax_error_for_invalid_python():
    findings = run_static_analysis("def broken(:\n    pass", "python")

    assert len(findings) == 1
    assert findings[0]["severity"] == "blocker"
    assert findings[0]["title"] == "Syntax error"


def test_reports_unused_import():
    findings = run_static_analysis("import os\nvalue = 1", "python")

    assert any(f["title"] == "Unused import" for f in findings)


def test_reports_debug_print():
    findings = run_static_analysis("print('debug')", "python")

    assert any(f["title"] == "Debug print" for f in findings)


def test_reports_long_function_and_deep_nesting():
    code = """
def large():
    if True:
        if True:
            if True:
                if True:
                    pass
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
"""
    findings = run_static_analysis(code, "python")

    titles = {f["title"] for f in findings}
    assert "Long function" in titles
    assert "Deep nesting" in titles
