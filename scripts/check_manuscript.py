#!/usr/bin/env python3
"""Regression checks for the revised manuscript (stdlib only).

Focuses on the defects found in the 2026-09-16 developmental audit:
rendered-chapter-number consistency, superseded series branding, dead
links, and the source/render claim that all 12 projects have starter code.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Rendered chapter number for each configured unit (projects and the
# toolkit are numbered by Quarto; verified against _book output).
RENDERED = {
    "index.qmd": None,
    "copyright.qmd": None,
    "acknowledgments.qmd": None,
    "chapters/chapter-understanding-ai-partner.qmd": 1,
    "chapters/chapter-input-process-output.qmd": 2,
    "chapters/chapter-variables.qmd": 3,
    "chapters/chapter-input.qmd": 4,
    "chapters/chapter-making-decisions.qmd": 5,
    "chapters/chapter-loops.qmd": 6,
    "chapters/expression-toolkit.qmd": 7,
    "projects/fortune-teller.qmd": 8,
    "projects/mad-libs.qmd": 9,
    "projects/number-game.qmd": 10,
    "projects/rock-paper-scissors.qmd": 11,
    "chapters/chapter-functions.qmd": 12,
    "chapters/chapter-organizing-information.qmd": 13,
    "chapters/chapter-saving-work.qmd": 14,
    "chapters/chapter-debugging.qmd": 15,
    "projects/temperature-converter.qmd": 16,
    "projects/contact-book.qmd": 17,
    "projects/journal-app.qmd": 18,
    "projects/quiz-game.qmd": 19,
    "chapters/chapter-working-with-data.qmd": 20,
    "chapters/chapter-connected-programs.qmd": 21,
    "chapters/chapter-interactive-systems.qmd": 22,
    "chapters/chapter-becoming-architect.qmd": 23,
    "projects/grade-analysis.qmd": 24,
    "projects/weather-app.qmd": 25,
    "projects/text-adventure.qmd": 26,
    "projects/todo-gui.qmd": 27,
    "chapters/chapter-next-steps.qmd": 28,
    "chapters/summary.qmd": 29,
    "references.qmd": None,
    "about-author.qmd": None,
}

STALE_BRANDING = (
    "Python Jumpstart",
    "Python Step by Step",
    "Step by Step: Learning",
)

STALE_LINKS = (
    "ship-it-python-in-production",
    "api.quotable.io",
    "michaelborck.dev",
    "michaelborck.education",
)


def configured_files():
    return list(RENDERED)


def skip_appledouble(paths):
    return [p for p in paths if not p.name.startswith("._")]


class ManuscriptChecks(unittest.TestCase):
    def test_every_configured_file_exists(self):
        for name in configured_files():
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).is_file(), name)

    def test_no_hardcoded_chapter_numbers_in_headings(self):
        for name in configured_files():
            text = (ROOT / name).read_text(encoding="utf-8")
            heading = next(
                (line for line in text.splitlines() if line.startswith("# ")),
                "",
            )
            with self.subTest(file=name):
                self.assertNotRegex(heading, r"^# Chapter \d+")

    def test_no_stale_branding(self):
        for name in configured_files():
            text = (ROOT / name).read_text(encoding="utf-8")
            for phrase in STALE_BRANDING:
                with self.subTest(file=name, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_no_stale_links(self):
        for name in configured_files():
            text = (ROOT / name).read_text(encoding="utf-8")
            for target in STALE_LINKS:
                with self.subTest(file=name, target=target):
                    self.assertNotIn(target, text)

    def test_no_mermaid_diagrams(self):
        for name in configured_files():
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(file=name):
                self.assertNotIn("{mermaid}", text)

    def test_exercise_numbers_match_rendered_chapters(self):
        for name, number in RENDERED.items():
            if number is None or name.startswith("projects/"):
                continue
            text = (ROOT / name).read_text(encoding="utf-8")
            expected = f"Exercise {number}."
            found = re.findall(r"Exercise \d+\.", text)
            with self.subTest(file=name):
                self.assertTrue(
                    all(item == expected for item in found),
                    f"{name}: {found} do not match {expected}",
                )

    def test_no_dangling_chapter_references(self):
        # Literal "Chapter N"/"Chapters N-M" references must use numbers
        # that exist in the rendered map, and must not be the first
        # chapter (the superseded 0-indexed scheme's signature).
        valid = {n for n in RENDERED.values() if n is not None}
        pattern = re.compile(r"[Cc]hapters? (\d+)(?:-(\d+))?")
        for name in configured_files():
            text = (ROOT / name).read_text(encoding="utf-8")
            for match in pattern.finditer(text):
                numbers = {int(match.group(1))}
                if match.group(2):
                    numbers.update(range(int(match.group(1)),
                                         int(match.group(2)) + 1))
                with self.subTest(file=name, ref=match.group(0)):
                    self.assertTrue(
                        numbers.issubset(valid),
                        f"{match.group(0)} outside rendered numbering",
                    )

    def test_every_project_has_starter_code(self):
        code = ROOT / "code"
        for path in skip_appledouble(sorted((ROOT / "projects").glob("*.qmd"))):
            stem = path.stem
            with self.subTest(project=stem):
                self.assertTrue((code / f"{stem}.py").is_file(), stem)
                self.assertTrue((code / f"{stem}.ipynb").is_file(), stem)
                notebook = (code / f"{stem}.ipynb").read_text(encoding="utf-8")
                self.assertIn("colab", notebook)

    def test_prerequisites_reference_rendered_numbers(self):
        # Project "Before You Start" callouts must cite chapters that
        # exist, and the numbers must be the rendered ones.
        for name in RENDERED:
            if not name.startswith("projects/"):
                continue
            text = (ROOT / name).read_text(encoding="utf-8")
            for chapter in re.findall(r"- Chapter (\d+):", text):
                with self.subTest(file=name, chapter=chapter):
                    self.assertIn(int(chapter), RENDERED.values())

    def test_source_encoding_is_utf8(self):
        paths = skip_appledouble(sorted(ROOT.glob("**/*.qmd")))
        for path in paths:
            if "_book" in path.parts or "_print_source" in path.parts:
                continue
            with self.subTest(file=str(path)):
                path.read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main(verbosity=2)
