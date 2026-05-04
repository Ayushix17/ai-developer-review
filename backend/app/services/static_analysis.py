import ast


def _warning(title: str, description: str, line_number: int | None, suggestion: str | None) -> dict:
    return {
        "severity": "warn",
        "title": title,
        "description": description,
        "line_number": line_number,
        "suggestion": suggestion,
        "category": "static",
    }


def run_static_analysis(code: str, language: str) -> list[dict]:
    if language.lower() != "python":
        return []

    findings: list[dict] = []

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [
            {
                "severity": "blocker",
                "title": "Syntax error",
                "description": exc.msg,
                "line_number": exc.lineno,
                "suggestion": "Fix the syntax error before running review again.",
                "category": "static",
            }
        ]

    imported_names: dict[str, int] = {}
    used_names: set[str] = set()

    class Analyzer(ast.NodeVisitor):
        def __init__(self) -> None:
            self.current_depth = 0

        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                imported_names[alias.asname or alias.name.split(".")[0]] = node.lineno
            self.generic_visit(node)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            for alias in node.names:
                imported_names[alias.asname or alias.name] = node.lineno
            self.generic_visit(node)

        def visit_Name(self, node: ast.Name) -> None:
            used_names.add(node.id)
            self.generic_visit(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            body_len = len(node.body)
            if body_len > 20:
                findings.append(
                    _warning(
                        "Long function",
                        f"Function `{node.name}` has {body_len} statements.",
                        node.lineno,
                        "Split the function into smaller units.",
                    )
                )
            self.generic_visit(node)

        def _visit_nested_block(self, node: ast.AST) -> None:
            self.current_depth += 1
            if self.current_depth > 3:
                findings.append(
                    _warning(
                        "Deep nesting",
                        "Control flow nesting is deeper than 3 levels.",
                        getattr(node, "lineno", None),
                        "Extract inner branches into a helper function or return early.",
                    )
                )
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_If(self, node: ast.If) -> None:
            self._visit_nested_block(node)

        def visit_For(self, node: ast.For) -> None:
            self._visit_nested_block(node)

        def visit_While(self, node: ast.While) -> None:
            self._visit_nested_block(node)

        def visit_Try(self, node: ast.Try) -> None:
            self._visit_nested_block(node)

        def visit_Call(self, node: ast.Call) -> None:
            if isinstance(node.func, ast.Name) and node.func.id == "print":
                findings.append(
                    _warning(
                        "Debug print",
                        "Found `print()` call in code under review.",
                        node.lineno,
                        "Replace it with structured logging or remove it.",
                    )
                )
            self.generic_visit(node)

    Analyzer().visit(tree)

    for name, lineno in imported_names.items():
        if name not in used_names:
            findings.append(
                _warning(
                    "Unused import",
                    f"Imported name `{name}` is not used.",
                    lineno,
                    f"Remove the `{name}` import.",
                )
            )

    return findings
