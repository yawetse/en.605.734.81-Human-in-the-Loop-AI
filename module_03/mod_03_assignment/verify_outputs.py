"""Generate repeatable runtime evidence and compare it with project requirements."""

from argparse import ArgumentParser
from datetime import datetime
import os
from pathlib import Path
import re
import subprocess
import sys


ARTIFACT_FILENAMES = {
    "terminal": "terminal_output.txt",
    "tests": "unit_test_output.txt",
    "html": "business_report.html",
    "sanity": "requirements_sanity_check.md",
}


def _check(requirements, description, artifact, evidence, passed):
    return {
        "requirements": requirements,
        "description": description,
        "artifact": artifact,
        "evidence": evidence,
        "passed": bool(passed),
    }


# @spec CKS-VERIFY-003, CKS-VERIFY-004
def evaluate_requirements(
    terminal_output,
    test_output,
    html_output,
    spec_text,
    test_source,
    *,
    program_returncode,
    test_returncode,
    markdown_exists,
):
    """Return output and traceability checks tied to the EARS requirements."""
    required_terminal_sections = (
        "=== Recipes ===",
        "=== Orders ===",
        "=== Order Processing ===",
        "=== Inventory ===",
        "=== Restock ===",
        "=== Status ===",
    )
    required_html_sections = (
        "Cloud Kitchen Business Report",
        "Executive Summary",
        "Order Outcomes",
        "Predictive Stockout Alerts",
        "Unavailable Menu Items",
        "Final Inventory",
        "Restock Recommendations",
        "Expiry Concerns",
    )
    spec_ids = set(re.findall(r"\*\*(CKS-[A-Z0-9-]+)\*\*", spec_text))
    test_ids = set(re.findall(r"@spec[^\n]*?(CKS-[A-Z0-9-]+)", test_source))
    for annotation in re.findall(r"@spec[^\n]+", test_source):
        test_ids.update(re.findall(r"CKS-[A-Z0-9-]+", annotation))
    unchecked_ids = re.findall(r"- \[ \] \*\*(CKS-[A-Z0-9-]+)\*\*", spec_text)
    missing_test_ids = sorted(spec_ids - test_ids)

    checks = [
        _check(
            "CKS-VERIFY-001",
            "Program command completed",
            ARTIFACT_FILENAMES["terminal"],
            f"exit code {program_returncode}",
            program_returncode == 0,
        ),
        _check(
            "CKS-DATA-002",
            "All supplied data and processing sections were printed",
            ARTIFACT_FILENAMES["terminal"],
            ", ".join(required_terminal_sections),
            all(section in terminal_output for section in required_terminal_sections),
        ),
        _check(
            "CKS-PARTIAL-001, CKS-PARTIAL-002",
            "Partial fulfillment produced separate delivered and rejected line evidence",
            ARTIFACT_FILENAMES["terminal"],
            "Order 5 partially delivered Chicken Burger and rejected Caesar Salad",
            all(
                marker in terminal_output
                for marker in (
                    "Orders Partially Delivered: 1",
                    "Partially Delivered: Chicken Burger",
                    "Not Delivered: Caesar Salad",
                )
            ),
        ),
        _check(
            "CKS-FULFILL-003",
            "Cumulative deductions reached the expected final seeded inventory",
            ARTIFACT_FILENAMES["terminal"],
            "Chicken Breast: 800 grams",
            "Chicken Breast: 800 grams" in terminal_output,
        ),
        _check(
            "CKS-RESTOCK-001, CKS-RESTOCK-002, CKS-RESTOCK-003",
            "Restock and expiry evidence was printed",
            ARTIFACT_FILENAMES["terminal"],
            "Chicken Breast restock and Expiry Concerns sections",
            all(
                marker in terminal_output
                for marker in (
                    "Restock Recommendations:",
                    "Chicken Breast: order 9200 grams",
                    "Expiry Concerns:",
                )
            ),
        ),
        _check(
            "CKS-FORECAST-001, CKS-FORECAST-002",
            "Predictive stockout evidence was printed",
            ARTIFACT_FILENAMES["terminal"],
            "Chicken Breast forecast at 1840.0 grams per order",
            all(
                marker in terminal_output
                for marker in (
                    "Predictive Stockout Alerts:",
                    "Chicken Breast: approximately",
                    "1840.0 grams per order",
                )
            ),
        ),
        _check(
            "CKS-MENU-001, CKS-MENU-002",
            "Unavailable menu-item evidence was printed",
            ARTIFACT_FILENAMES["terminal"],
            "Margherita Pizza blocked by expired Flour",
            all(
                marker in terminal_output
                for marker in (
                    "Unavailable Menu Items:",
                    "Margherita Pizza: Flour (Expired)",
                )
            ),
        ),
        _check(
            "CKS-VERIFY-002",
            "Complete unit-test command passed",
            ARTIFACT_FILENAMES["tests"],
            "test command exited 0 and reported OK",
            test_returncode == 0
            and re.search(r"Ran \d+ tests?", test_output) is not None
            and re.search(r"^OK$", test_output, re.MULTILINE) is not None,
        ),
        _check(
            "CKS-REPORT-005",
            "Markdown business report was generated",
            "BUSINESS_REPORT.md",
            "file exists after the program run",
            markdown_exists,
        ),
        _check(
            "CKS-REPORT-006",
            "HTML business report contains every required section",
            ARTIFACT_FILENAMES["html"],
            ", ".join(required_html_sections),
            all(section in html_output for section in required_html_sections),
        ),
        _check(
            "All EARS requirements",
            "Every requirement is marked implemented",
            "cloud-kitchen-simulation-specs.md",
            (
                "no unchecked requirements"
                if not unchecked_ids
                else "unchecked: " + ", ".join(unchecked_ids)
            ),
            not unchecked_ids,
        ),
        _check(
            "All EARS requirements",
            "Every requirement has a test annotation",
            "test_main.py",
            (
                "all requirement IDs are cited"
                if not missing_test_ids
                else "missing test annotations: " + ", ".join(missing_test_ids)
            ),
            not missing_test_ids,
        ),
    ]
    return checks


# @spec CKS-VERIFY-003, CKS-VERIFY-004
def render_sanity_report(checks, artifact_paths):
    """Render the requirement comparison as a Markdown review artifact."""
    overall_passed = all(check["passed"] for check in checks)
    lines = [
        "# Module 3 Requirements Sanity Check",
        "",
        f"**Generated:** {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"**Overall result:** {'PASS' if overall_passed else 'FAIL'}",
        "",
        "## Evidence Artifacts",
        "",
    ]
    for label, path in artifact_paths.items():
        lines.append(f"- {label}: `{path}`")
    lines.extend(
        [
            "",
            "## Requirement Comparison",
            "",
            "| Result | Requirement | Check | Evidence source | Observed evidence |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for check in checks:
        result = "PASS" if check["passed"] else "FAIL"
        cells = (
            result,
            check["requirements"],
            check["description"],
            check["artifact"],
            check["evidence"],
        )
        escaped_cells = [str(value).replace("|", "\\|").replace("\n", " ") for value in cells]
        lines.append("| " + " | ".join(escaped_cells) + " |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "The captured runtime, rendered HTML, unit tests, and requirement traceability agree. "
                "This is a final sanity check of the current local implementation."
                if overall_passed
                else "At least one check failed. Review the failed row and its source artifact before submission."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def _combined_output(result):
    output = result.stdout
    if result.stderr:
        output += ("\n" if output and not output.endswith("\n") else "") + result.stderr
    return output


# @spec CKS-VERIFY-001, CKS-VERIFY-002, CKS-VERIFY-003, CKS-VERIFY-004, CKS-VERIFY-005
def run_verification(output_dir):
    """Run the real program and tests, then write the checked evidence bundle."""
    base_dir = Path(__file__).resolve().parent
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    program_result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=base_dir,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    test_result = subprocess.run(
        [sys.executable, "-m", "unittest", "-v"],
        cwd=base_dir,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    terminal_output = _combined_output(program_result)
    test_output = _combined_output(test_result)
    html_source = base_dir / "BUSINESS_REPORT.html"
    markdown_source = base_dir / "BUSINESS_REPORT.md"
    html_output = html_source.read_text(encoding="utf-8") if html_source.exists() else ""
    spec_path = (
        base_dir.parent.parent
        / "docs"
        / "intent"
        / "cloud-kitchen-simulation"
        / "cloud-kitchen-simulation-specs.md"
    )
    spec_text = spec_path.read_text(encoding="utf-8")
    test_source = (base_dir / "test_main.py").read_text(encoding="utf-8")

    checks = evaluate_requirements(
        terminal_output,
        test_output,
        html_output,
        spec_text,
        test_source,
        program_returncode=program_result.returncode,
        test_returncode=test_result.returncode,
        markdown_exists=markdown_source.exists(),
    )
    paths = {key: output_dir / filename for key, filename in ARTIFACT_FILENAMES.items()}
    paths["terminal"].write_text(terminal_output, encoding="utf-8")
    paths["tests"].write_text(test_output, encoding="utf-8")
    paths["html"].write_text(html_output, encoding="utf-8")
    artifact_labels = {
        "Program terminal output": ARTIFACT_FILENAMES["terminal"],
        "Unit-test output": ARTIFACT_FILENAMES["tests"],
        "HTML business report": ARTIFACT_FILENAMES["html"],
    }
    sanity_report = render_sanity_report(checks, artifact_labels)
    paths["sanity"].write_text(sanity_report, encoding="utf-8")

    passed = all(check["passed"] for check in checks)
    print(f"Verification result: {'PASS' if passed else 'FAIL'}")
    for path in paths.values():
        print(path)
    return 0 if passed else 1


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "verification",
        help="Directory for regenerated verification artifacts",
    )
    args = parser.parse_args()
    return run_verification(args.output_dir)


if __name__ == "__main__":
    raise SystemExit(main())
