---
{
  "id": "file_mu1kfobt_3q18dq6q",
  "filetype": "document",
  "filename": "Framing",
  "created_at": "2026-09-14T18:17:50.055Z",
  "updated_at": "2026-09-20T12:16:56.187Z",
  "private": false,
  "password": null,
  "encrypted_content": false,
  "encrypted_key_name": null,
  "meta": {
    "description": "",
    "tags": [],
    "categories": [],
    "repos": [],
    "github_pages": [],
    "location": "/module_02",
    "data": {
      "source": "file",
      "sourceUri": "file:///var/mobile/Library/Mobile%20Documents/com~apple~CloudDocs/Documents/MS%20Computer%20Science%20JHU/EN.605.734.81%20-%20Human-in-the-Loop%20AI/module_02/Framing.md",
      "sourceFilename": "Framing.md",
      "sourceExtension": ".md",
      "sourceLinked": true,
      "sourceDefaultLocation": false,
      "sourceFrontMatterFormat": "json"
    }
  }
}
---
# Module 3 - Overview and Objectives

## **Overview**

<table style="min-width: 160px;">
<colgroup><col style="min-width: 80px;"><col style="min-width: 80px;"></colgroup><tbody><tr><td colspan="1" rowspan="1"><h2><strong><img src="https://jhu.instructure.com/courses/134608/files/18914477/preview" alt="ChatGPT Image Jun 11, 2026 at 09_57_32 AM.png"></strong></h2></td><td colspan="1" rowspan="1"><p>This module introduces AI-assisted coding as a new way of developing software—one that shifts the learner’s role from writing every line of code manually to directing, reviewing, testing, and refining AI-generated output. Learners will examine how AI coding assistants differ from traditional development tools, where they are most useful, and where they require careful human oversight.</p><p>The module introduces the concept of “vibe coding” as a practical mental model for working with AI coding tools. Learners will practice thinking like a navigator, reviewer, and decision-maker: setting the direction, breaking work into small tasks, inspecting AI-generated code, testing results, and deciding when to accept, reject, or revise the output.</p><p>The lectures also emphasize structured prompting and iterative development. Learners will explore a staged workflow that moves from planning to requirements, task breakdown, and implementation. They will learn why short development loops are more reliable than large monolithic prompts and how to use reusable prompt templates for planning, implementation, and debugging.</p><p>A major theme of this module is ownership. AI can generate code quickly, explain unfamiliar syntax, suggest tests, and help debug errors, but it cannot guarantee correctness, security, or maintainability. Learners will practice reviewing AI-generated code, generating and running tests, identifying hidden assumptions, managing context, resolving stubs and TODOs, detecting duplication, and using validation hooks to make uncertainty visible.</p><p>By the end of the module, learners will have a repeatable AI-assisted development playbook they can apply to small coding projects and later extend to more complex software engineering work.</p></td></tr></tbody>
</table>

---

## **Objectives**

By the end of this module, you will be able to:

- **3.1 Explain AI-Assisted Coding**
  - Define AI-assisted coding and describe how it differs from traditional software development.
  - Explain how AI coding tools shift the developer’s role from typist to director, reviewer, and decision-maker.
  - Describe why AI-generated code must be verified, tested, and reviewed before it can be trusted.
- **3.2 Describe the Mental Model of Vibe Coding**
  - Explain the “vibe coding” approach and how it helps developers guide AI tools while staying in control.
  - Describe the three roles learners play when working with AI-generated code: navigator, reviewer, and decision-maker.
  - Identify why AI should be treated as a fast but imperfect collaborator rather than a reliable source of truth.
- **3.3 Identify Appropriate and Inappropriate Uses of AI-Assisted Coding**
  - Describe situations where AI-assisted coding is effective, such as prototyping, boilerplate generation, translating logic into code, and explaining unfamiliar code.
  - Identify situations where AI-assisted coding requires extra caution, including complex codebases, specialized domains, security-critical code, and novel problem solving.
  - Explain why the more context the AI lacks, the more human oversight is required.
- **3.4 Apply Structured Prompting Techniques**
  - Explain why prompting is a structured skill rather than a matter of clever phrasing.
  - Use a staged prompting workflow: plan, refine requirements, break work into tasks, and implement one task at a time.
  - Apply prompt templates for planning, task breakdown, implementation, and debugging.
- **3.5 Use an Iterative Development Loop**
  - Apply the Build → Test → Inspect → Refine loop to AI-assisted development.
  - Break coding work into small, focused steps that are easier to test, debug, and understand.
  - Recognize and correct scope creep, context drift, and unclear AI-generated output.
- **3.6 Test and Debug AI-Generated Code**
  - Generate unit tests immediately after producing AI-generated code.
  - Run tests locally and inspect failures before accepting AI-generated corrections.
  - Use debugging prompts that include the code, the full error message, and a request for root-cause explanation.
- **3.7 Review AI-Generated Code with Human Oversight**
  - Apply a code review checklist to determine whether AI-generated code does what was requested, handles edge cases, avoids hidden assumptions, and avoids unnecessary security risk.
  - Explain the principle: “If the AI wrote it, you own it.”
  - Demonstrate accountability by reading, understanding, testing, and explaining AI-generated code before using it.
- **3.8 Manage Context, Stubs, Duplication, and Validation Hooks**
  - Explain how context window limitations can cause AI tools to forget requirements, contradict earlier decisions, or duplicate logic.
  - Use a project specification file or written project notes to maintain continuity across AI-assisted development sessions.
  - Identify and manage stubs, TODOs, duplicated logic, assumptions, and validation hooks as part of a disciplined development workflow.
- **3.9 Apply the AI-Assisted Coding Playbook**
  - Use the repeatable AI-assisted coding playbook: define the goal, ask for a plan, convert the plan into tasks, implement one task, add validation hooks, generate tests, debug and review, then refactor and repeat.
  - Reflect on the balance between speed and comprehension when using AI tools for software development.
  - Recognize that effective AI-assisted coding requires both tool fluency and disciplined engineering judgment.

---

## **How to Complete This Module:**

- Watch the AI-Assisted Coding lecture videos.
- Review the lecture slides and examples.
- Practice the staged prompting workflow using a small coding task.
- Apply the Build → Test → Inspect → Refine loop.
- Generate and review tests for AI-assisted code.
- Complete the module coding activity or discussion as posted in Canvas.
- Respond to any required peer discussion or reflection prompt before the end of the module week.

---

## **Thought for the Week**

“If the AI wrote it, you own it.”

  —  Anonymous