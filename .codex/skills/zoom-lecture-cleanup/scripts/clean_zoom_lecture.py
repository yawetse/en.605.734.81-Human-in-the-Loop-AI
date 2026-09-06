#!/usr/bin/env python3
"""Clean a Zoom lecture HTML export into transcript + next steps Markdown."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path


class ZoomLectureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_transcript_ul = False
        self.transcript_ul_depth = 0
        self.in_transcript_item = False
        self.in_text_div = False
        self.text_div_depth = 0
        self.text_buffer: list[str] = []
        self.transcript_items: list[str] = []

        self.in_step_area = False
        self.step_div_depth = 0
        self.step_buffer: list[str] = []
        self.in_tips_container = False
        self.tips_div_depth = 0
        self.tips_buffer: list[str] = []

    @staticmethod
    def _classes(attrs: list[tuple[str, str | None]]) -> set[str]:
        attr_map = dict(attrs)
        return set((attr_map.get("class") or "").split())

    @staticmethod
    def _clean_captured_text(parts: list[str]) -> str:
        raw = "".join(parts)
        lines = [line.strip() for line in raw.splitlines()]
        return " ".join(line for line in lines if line)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = self._classes(attrs)

        if tag == "ul" and "transcript-list" in classes:
            self.in_transcript_ul = True
            self.transcript_ul_depth = 1
            return

        if self.in_transcript_ul and tag == "ul":
            self.transcript_ul_depth += 1

        if self.in_transcript_ul and tag == "li":
            self.in_transcript_item = True

        if self.in_transcript_item and tag == "div" and "text" in classes:
            self.in_text_div = True
            self.text_div_depth = 1
            self.text_buffer = []
            return

        if self.in_text_div and tag == "div":
            self.text_div_depth += 1

        if tag == "div" and "step-area" in classes:
            self.in_step_area = True
            self.step_div_depth = 1
            self.step_buffer = []
            return

        if self.in_step_area and tag == "div":
            self.step_div_depth += 1

        if tag == "div" and "tips-container" in classes:
            self.in_tips_container = True
            self.tips_div_depth = 1
            self.tips_buffer = []
            return

        if self.in_tips_container and tag == "div":
            self.tips_div_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.in_text_div and tag == "div":
            self.text_div_depth -= 1
            if self.text_div_depth == 0:
                text = self._clean_captured_text(self.text_buffer)
                if text:
                    self.transcript_items.append(text)
                self.in_text_div = False
                self.text_buffer = []
                return

        if self.in_transcript_ul and tag == "li":
            self.in_transcript_item = False

        if self.in_transcript_ul and tag == "ul":
            self.transcript_ul_depth -= 1
            if self.transcript_ul_depth == 0:
                self.in_transcript_ul = False

        if self.in_step_area and tag == "div":
            self.step_div_depth -= 1
            if self.step_div_depth == 0:
                self.in_step_area = False

        if self.in_tips_container and tag == "div":
            self.tips_div_depth -= 1
            if self.tips_div_depth == 0:
                self.in_tips_container = False

    def handle_data(self, data: str) -> None:
        if self.in_text_div:
            self.text_buffer.append(data)
        if self.in_step_area:
            self.step_buffer.append(data)
        if self.in_tips_container:
            self.tips_buffer.append(data)


def frontmatter_from(path: Path) -> str:
    if not path.exists():
        return ""

    text = path.read_text()
    if not text.startswith("---"):
        return ""

    match = re.match(r"\A---\n.*?\n---\n?", text, flags=re.DOTALL)
    return match.group(0) if match else ""


def parse_next_steps(raw: str) -> list[str]:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if len(lines) > 1:
        return lines

    single_line = lines[0] if lines else ""
    if not single_line:
        return []

    parts = re.split(r"\s+(?=\d+\.\s)", single_line)
    return [part.strip() for part in parts if part.strip()]


def clean_zoom_lecture(html_path: Path, markdown_path: Path, output_path: Path) -> None:
    parser = ZoomLectureParser()
    parser.feed(html_path.read_text())

    if not parser.transcript_items:
        raise SystemExit(f"No transcript items found in {html_path}")

    next_steps = parse_next_steps("".join(parser.step_buffer))
    if not next_steps:
        next_steps = parse_next_steps("".join(parser.tips_buffer))
    if not next_steps:
        raise SystemExit(f"No next steps found in {html_path}")

    lines: list[str] = []
    frontmatter = frontmatter_from(markdown_path)
    if frontmatter:
        lines.append(frontmatter.rstrip())

    lines.extend(["## Audio Transcript", ""])
    lines.extend(f"- {item}" for item in parser.transcript_items)
    lines.extend(["", "## Next Steps", ""])
    lines.extend(next_steps)

    output_path.write_text("\n".join(lines) + "\n")


def main() -> None:
    arg_parser = argparse.ArgumentParser(
        description="Extract Zoom lecture transcript and next steps into clean Markdown."
    )
    arg_parser.add_argument("html", type=Path, help="Zoom recording HTML export")
    arg_parser.add_argument(
        "--markdown",
        type=Path,
        help="Existing Markdown file to update and use for frontmatter",
    )
    arg_parser.add_argument(
        "--output",
        type=Path,
        help="Output Markdown path. Defaults to --markdown or the HTML basename with .md.",
    )
    args = arg_parser.parse_args()

    html_path = args.html
    markdown_path = args.markdown or html_path.with_suffix(".md")
    output_path = args.output or markdown_path

    clean_zoom_lecture(html_path, markdown_path, output_path)


if __name__ == "__main__":
    main()
