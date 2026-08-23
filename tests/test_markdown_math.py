"""Guard the Markdown math contract used by GitHub and the MkDocs site."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
BRACKET_DELIMITER_RE = re.compile(r"(?<!\\)\\([()[\]])")
ENVIRONMENT_RE = re.compile(r"(?<!\\)\\(?P<kind>begin|end)\{(?P<name>[^}]+)\}")
BLOCK_DOLLAR_RE = re.compile(r"(?<!\\)\$\$")
INLINE_DOLLAR_RE = re.compile(r"(?<!\\)(?<!\$)\$(?!\$)")


def _markdown_sources() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and ".venv" not in path.parts
    )


def _lines_outside_code_blocks(path: Path) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    active_fence: str | None = None

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if active_fence is None:
                active_fence = marker[0]
            elif marker[0] == active_fence:
                active_fence = None
            continue

        if active_fence is None:
            lines.append((line_number, INLINE_CODE_RE.sub("", line)))

    return lines


def _math_delimiter_errors(path: Path) -> list[str]:
    errors: list[str] = []
    bracket_stack: list[tuple[str, int]] = []
    environment_stack: list[tuple[str, int]] = []
    block_dollar_count = 0
    inline_dollar_count = 0

    for line_number, line in _lines_outside_code_blocks(path):
        for match in BRACKET_DELIMITER_RE.finditer(line):
            delimiter = match.group(1)
            if delimiter in "([":
                bracket_stack.append((")" if delimiter == "(" else "]", line_number))
            elif not bracket_stack or bracket_stack[-1][0] != delimiter:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: unexpected \\{delimiter}")
            else:
                bracket_stack.pop()

        for match in ENVIRONMENT_RE.finditer(line):
            kind = match.group("kind")
            name = match.group("name")
            if kind == "begin":
                environment_stack.append((name, line_number))
            elif not environment_stack or environment_stack[-1][0] != name:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: unexpected \\end{{{name}}}")
            else:
                environment_stack.pop()

        block_dollar_count += len(BLOCK_DOLLAR_RE.findall(line))
        inline_dollar_count += len(INLINE_DOLLAR_RE.findall(line))

    errors.extend(
        f"{path.relative_to(ROOT)}:{line_number}: unclosed \\{delimiter}"
        for delimiter, line_number in bracket_stack
    )
    errors.extend(
        f"{path.relative_to(ROOT)}:{line_number}: unclosed \\begin{{{name}}}"
        for name, line_number in environment_stack
    )
    if block_dollar_count % 2:
        errors.append(f"{path.relative_to(ROOT)}: unbalanced $$ delimiters")
    if inline_dollar_count % 2:
        errors.append(f"{path.relative_to(ROOT)}: unbalanced inline $ delimiters")
    return errors


def test_mkdocs_math_renderer_is_configured() -> None:
    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    requirements = (ROOT / "docs" / "requirements.txt").read_text(encoding="utf-8")
    mathjax_config = (ROOT / "docs" / "javascripts" / "mathjax.js").read_text(encoding="utf-8")

    assert "pymdownx.arithmatex:" in config
    assert "generic: true" in config
    assert "javascripts/mathjax.js" in config
    assert "mathjax@3/es5/tex-chtml.js" in config
    assert "pymdown-extensions" in requirements
    assert "processEnvironments: true" in mathjax_config
    assert 'processHtmlClass: "arithmatex"' in mathjax_config


def test_markdown_math_delimiters_are_balanced() -> None:
    errors = [error for path in _markdown_sources() for error in _math_delimiter_errors(path)]
    assert not errors, "\n".join(errors)
