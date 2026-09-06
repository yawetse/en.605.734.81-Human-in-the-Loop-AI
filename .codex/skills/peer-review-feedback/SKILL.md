---
name: peer-review-feedback
description: Draft and check EN.605.734 Human-in-the-Loop AI peer feedback when an assignment or Canvas workflow calls for it. Use when the user asks to write, revise, or validate concise peer feedback against the prompt and local module materials.
---

# Peer Review Feedback

## Overview

Use this skill to produce concise, useful EN.605.734 peer feedback. Confirm that the assignment actually requests peer review before treating it as a required course workflow.

## Source Files

Start from the local course files when available:

- The assignment prompt, rubric, and any peer-review instructions supplied by Canvas or the user.
- The active module's overview, readings, lecture notes, or evaluation criteria.
- `course-info/generative-ai-policy.md` when the feedback or assignment requires disclosure guidance.
- The peer's submission and the user's own work, when supplied.

Canvas remains the source of truth for assigned reviews, due dates, and submission status.

## Workflow

1. Identify the assigned peer submission and required feedback format from Canvas or files the user provides.
2. Read the peer's self-check and Yaw's self-check if available.
3. Read the module prompt, rubric, readings, or lecture notes when needed to evaluate the work.
4. Compare claims, evidence, assumptions, human-AI task allocation, evaluation approach, and final recommendation as relevant. Do not focus only on whether the conclusion matches.
5. Draft feedback in first person, with a short confirmation of what looks correct and one concrete item to recheck if needed.
6. Keep the tone direct, respectful, and practical. Use straightforward business language.
7. If the evidence is uncertain, phrase feedback as something to recheck instead of stating it as a fact.

## Feedback Rules

Good peer review feedback is:

1. Specific: name the step, equation, state, node, rule, or assumption.
2. Brief: say enough to be useful without rewriting the whole submission.
3. Evidence-based: tie the comment to the self-check prompt, module materials, lecture, reading, or pseudocode.
4. Respectful: focus on the work, not the person.
5. Practical: point to what the peer should verify next.

Avoid:

1. Grading the peer's work as if you are the instructor.
2. Unrequested implementation help or replacement work.
3. Sharing or asking for code.
4. Outside sources for solving the self-check unless the course materials allow them.
5. Empty comments or vague comments such as "looks good" with no evidence.
6. Posting private peer review details outside Canvas.

## Comment Templates

Use this structure for a normal Canvas comment:

```markdown
I reviewed the submission against the prompt and module materials.

What looks correct:
- 

What I would recheck:
- 

Question or note:
- 
```

If the peer's work appears correct, use a concise verification:

```markdown
I reviewed the stated task, evidence, and conclusion against the module materials. I did not see a mismatch that needs correction. The reasoning is clear enough for me to follow.
```

If there is a likely issue, use careful language:

```markdown
I would recheck the evidence supporting the recommendation. My reading of the prompt is that the human role and evaluation criteria should be stated explicitly, which may affect the conclusion.
```

## Final Check

Before returning or submitting feedback, confirm:

1. The comment references the actual submitted work.
2. The comment gives at least one useful observation, question, or confirmation.
3. The comment does not provide code or programming implementation help.
4. The comment does not claim Canvas submission status unless the user showed it.
5. The comment is short enough to paste into Canvas.
