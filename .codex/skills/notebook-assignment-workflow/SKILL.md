---
name: notebook-assignment-workflow
description: Work through EN.605.734 Human-in-the-Loop AI notebook and module assignments using local course materials. Use when the user asks to interpret an assignment, analyze human-AI systems, draft or review notebook documentation, verify code, prepare an experiment or evaluation, or refine a reflection or report while following the course GenAI policy.
gpdoc_metadata:
  id: file_ly82qnhq
  filetype: document
  filename: SKILL
  created_at: '2026-05-31T14:22:34.420Z'
  updated_at: '2026-05-31T14:22:34.875Z'
  meta:
    location: /
---
# Notebook Assignment Workflow

## Overview

Use this skill for EN.605.734 Human-in-the-Loop AI work. Ground each response in the assignment and local materials, then help the user produce clear analysis, experiments, notebooks, reflections, or reports that retain the user's own judgment.

## Source Priority

Start with local files in this order:

1. The assignment prompt, rubric, notebook, or user-provided file.
2. The active module's overview, instructions, readings, lecture notes, captions, and provided data.
3. `course-info/generative-ai-policy.md` and other course-wide instructions.
4. Existing user drafts and any examples explicitly supplied for the assignment.
5. Canvas or web sources only if the user provides content or explicitly asks to look something up.

Canvas remains the source of truth when local files conflict.

## Context Gathering

Use fast local commands:

```bash
rg --files module_01
sed -n '1,220p' path/to/file.md
jq -r '.cells[] | "\n---CELL " + .cell_type + "---\n" + (.source | join(""))' notebook.ipynb
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=- file.pdf
```

If a PDF text extractor is unavailable, use Ghostscript `txtwrite` before falling back to `strings`.

Read only enough notebook/caption content to identify the assignment requirements, algorithms, vocabulary, and output format.

## Course GenAI Policy

Read the assignment-specific guidance before writing answers or code. The local course policy permits GenAI use, but it does not replace critical thinking or the student's responsibility for accuracy, bias, and final quality.

Follow these defaults:

1. Follow any assignment-specific restriction when it is stricter than the course-wide policy.
2. Distinguish AI-generated material from the user's analysis and make assumptions visible.
3. Remind the user to include the required GenAI disclosure, including the interaction reference and prompts/responses or conversation link, when the assignment requires it.
4. Prefer course materials over outside sources.

## Notebook and Analysis Style

Use the format required by the prompt. When no format is specified, keep notebooks reproducible: state the question and assumptions, separate setup from analysis, explain the result in Markdown, and add focused checks for calculations or code that affect the conclusion.

For human-AI evaluation work, make the evaluation unit, human role, model or tool, task allocation, metrics, data source, and limitations explicit. Do not imply causal, fairness, or performance conclusions that the available evidence does not support.

## Workflow

1. Identify the active module and assignment artifact.
2. Read the prompt and any related pseudocode.
3. Read module notes/captions for the relevant algorithm concepts.
4. Read course-level instructions for submission and style rules.
5. Summarize the task in plain language.
6. Choose the output type that fits the assignment, such as a concept explanation, evaluation plan, Markdown working guide, notebook documentation, draft review, test/debug help, experiment interpretation, or reflection.
7. Keep outputs specific to the assignment and cite local file names when helpful.
8. If editing files, keep changes scoped and preserve user work.

## Self-Check Workflow

For reflections, short-answer work, or self-checks:

1. Extract the questions from the PDF or prompt.
2. Restate each question before its answer section.
3. Include trace tables for algorithms that require frontier/explored state.
4. Include enough intermediate reasoning to show how the result was reached.
5. Use a clearly labeled structure when information is missing rather than inventing facts or personal experience.
6. Verify the reasoning and format the final Markdown when the user provides their work.

For a human-AI system analysis, include the human role, model role, handoff or escalation points, quality controls, evaluation approach, and relevant ethical or organizational considerations when they are in scope.

## Programming Assignment Workflow

For programming notebooks:

1. Identify what the implementation is expected to demonstrate.
2. Review or develop the work in small, testable parts.
3. Debug by identifying the failed assumption and making the smallest supported correction.
4. Document data, prompts, models, participants, and settings needed to reproduce the result when they are relevant.
5. Help interpret results without overstating them.

## Review Checklist

Before finalizing a guide, notebook response, or edited file, check:

1. The output follows the assignment prompt.
2. The reasoning is visible where required.
3. The wording uses straightforward business language.
4. No placeholder text remains unless intentionally left for the user.
5. Markdown links and anchors are valid.
6. The work follows the assignment's required format and disclosure requirements.
7. Tests or checks are directly tied to the conclusion.
8. Limitations and unverified assumptions are stated.
