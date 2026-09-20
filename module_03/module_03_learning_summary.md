---
{
  "id": "module_03_learning_summary",
  "filetype": "document",
  "filename": "module_03_learning_summary",
  "created_at": "2026-09-20T00:00:00.000Z",
  "updated_at": "2026-09-20T00:00:00.000Z",
  "meta": {
    "location": "/module_03",
    "tags": [],
    "categories": [],
    "description": "Module 03 learning summary",
    "source": "markdown"
  }
}
---
# Module 03 Learning Summary

> Study note: This is an AI-assisted study artifact. Before submitting any part of it, I need to verify the sources, revise it in my own words, and include the [course-required GenAI disclosure](../course-info/generative-ai-policy.md).

## Sources Reviewed

- [Module 3 overview and objectives](overview_03.md)
- [Module 3 readings page](readings_03.md), which does not list additional readings
- [Vibe Coding lecture slides](Vibe%20Coding.pdf), 80 PDF pages
- [Lecture 1: AI-Assisted Coding](mod_03_lectures/V1%20AI%20Assisted%20Coding%20Complete_Captions_English%20%28United%20States%29.txt)
- [Lecture 2: Building the Skill](mod_03_lectures/V.2%20Skill%20Complete_Captions_English%20%28United%20States%29.txt)
- [Lecture 3: Testing and Debugging](mod_03_lectures/V3_Debugging_Captions_English%20%28United%20States%29.txt)
- [Lecture 4: Advanced Techniques](mod_03_lectures/V4%20Adv_Techniques_Captions_English%20%28United%20States%29.txt)
- [Lecture 5: Key Takeaways](mod_03_lectures/V5%20Key%20Take%20Aways%20Complete_Captions_English%20%28United%20States%29.txt)
- [Module 3 assignment overview](mod_03_assignment/module_03_assignment.md)
- [Cloud kitchen reference PDF](mod_03_assignment/AI-Assisted%20Cloud%20Kitchen%20Inventory%20Simulation.pdf), 14 pages
- The provided [`main.py`](mod_03_assignment/main.py), [`test_main.py`](mod_03_assignment/test_main.py), and [`seed_data-1.py`](mod_03_assignment/seed_data-1.py)

The lecture transcripts do not contain timestamps, so I link to the relevant transcript and name the topic. PDF page references use the viewer's page count.

## Core Summary

My central learning is that AI-assisted coding changes where I apply engineering judgment. I can delegate syntax generation, boilerplate, explanations, test drafts, and debugging suggestions to an AI assistant. I still define the problem, state the constraints, inspect the result, run tests, and accept responsibility for the final system. The slides describe the AI as a probabilistic generator optimized for plausible output, not as a software engineer that verifies correctness. A polished answer can still contain incorrect logic, invented interfaces, missed edge cases, or security problems. [Vibe Coding, PDF pp. 5-9](Vibe%20Coding.pdf#page=5)

The module gives me three roles. As **navigator**, I define the goal, break it into small tasks, and decide what completion means. As **reviewer**, I inspect generated code for correctness, assumptions, gaps, and drift. As **decision-maker**, I accept, reject, revise, or replace the output and own the result. These roles keep the human in control of direction, verification, and accountability. [Vibe Coding, PDF p. 9](Vibe%20Coding.pdf#page=9)

The core workflow is incremental: plan the system, refine the plan into requirements, divide the work into small tasks, and implement one task at a time. Each implementation then follows **Build → Test → Inspect → Refine**. Short loops reduce the amount of code under review, make failures easier to trace, and provide checkpoints before errors spread. [Vibe Coding, PDF pp. 23-31](Vibe%20Coding.pdf#page=23)

Testing does not transfer correctness authority to the AI. The same model can write a faulty function and tests that encode the same faulty assumption. I need to specify normal, boundary, and failure cases, run the tests locally, inspect what they omit, and compare selected outputs with results I can calculate independently. When a test fails, I should read the full error, identify a likely cause, ask the AI to explain the cause and propose a focused correction, then rerun the full suite. [Vibe Coding, PDF pp. 41-47](Vibe%20Coding.pdf#page=41)

For work that spans files or sessions, I need to externalize state. `PROJECT_SPEC.md` records the purpose, component status, decisions, constraints, current task, next task, and verification status. Intentional stubs can serve as visible implementation tasks. Duplication checks protect the global design from locally generated copies of the same logic. Validation hooks make assumptions, uncertainty, and incomplete work visible in the code until I resolve them. [Vibe Coding, PDF pp. 60-70](Vibe%20Coding.pdf#page=60)

## Key Learnings

### I should use AI where I can verify the result

The module identifies prototyping, boilerplate, translating known logic into code, and explaining unfamiliar code as strong use cases. It calls for more caution with specialized domains, long or complex codebases, novel problems, and security-critical work. My decision should depend on the cost of an error, the context available to the model, and whether I have a credible way to evaluate the output. [Vibe Coding, PDF pp. 11-14](Vibe%20Coding.pdf#page=11)

Speed is useful only when I reinvest some of it in review and testing. If I cannot explain, test, or modify generated code, then I do not have enough understanding to accept it. [Lecture 3, ownership discussion](mod_03_lectures/V3_Debugging_Captions_English%20%28United%20States%29.txt) [Vibe Coding, PDF pp. 76-77](Vibe%20Coding.pdf#page=76)

### Structure matters more than prompt phrasing

The course rejects the large, all-in-one prompt because it creates broad scope, tangled logic, hidden placeholders, and a large review surface. The preferred sequence is:

1. Ask for a high-level plan before requesting code.
2. Convert the plan into concrete inputs, outputs, constraints, and edge cases.
3. Split each component into tasks small enough for one prompt.
4. Implement and verify one task before moving to the next.

The four reusable prompt patterns support planning, task breakdown, implementation, and debugging. An implementation prompt should define one task and state that no other task should be changed. A debugging prompt should include the relevant code and full error, ask for a root-cause explanation, and request a focused correction. [Vibe Coding, PDF pp. 24-31](Vibe%20Coding.pdf#page=24)

### I should test immediately and independently

The testing workflow is: generate one focused unit, request tests, run them locally, and feed failures back with the full error. Test coverage should include normal cases, boundaries, invalid inputs, and expected failures. Passing tests are evidence about the tested cases, not proof that the implementation is correct. [Vibe Coding, PDF pp. 42-44](Vibe%20Coding.pdf#page=42)

The five-point review checklist asks whether the function does what I requested, contains hidden assumptions, hard-codes values that should be configurable, handles bad inputs, and touches security-sensitive or business-critical behavior. I should read the code and check outputs I can verify manually before accepting it. [Vibe Coding, PDF p. 46](Vibe%20Coding.pdf#page=46)

### I need deliberate context and codebase management

Context windows are finite. Requirements can lose influence as a session grows, and the model does not provide reliable persistent memory across sessions. The practical response is to keep sessions focused, maintain `PROJECT_SPEC.md`, and re-anchor the AI with the relevant project state at the start of a session. [Vibe Coding, PDF pp. 61-62](Vibe%20Coding.pdf#page=61)

Stubs are useful when they are intentional, visible, and tracked. A scaffold can establish the structure while each stub becomes a later task. Hidden or forgotten stubs are defects. [Vibe Coding, PDF pp. 63-64](Vibe%20Coding.pdf#page=63)

AI assistants tend to optimize for the immediate prompt, so duplicated validation, lookup, or business-rule logic can accumulate across tasks. The module recommends a duplication review after every three or four implementation tasks. Validation hooks should identify assumptions, uncertainty, and incomplete sections, but they should be resolved rather than left permanently in the code. [Vibe Coding, PDF pp. 65-70](Vibe%20Coding.pdf#page=65)

### The complete playbook preserves human control

The closing playbook contains eight steps:

1. Define the goal.
2. Ask for a plan.
3. Convert the plan into tasks.
4. Implement one task.
5. Add validation hooks.
6. Generate and run tests.
7. Debug and review.
8. Refactor and repeat.

The main risks are shallow understanding, accumulated technical debt, and misplaced confidence. The control for all three is the same disciplined habit: constrain the task, inspect the output, verify behavior, record project state, and clean up before proceeding. [Vibe Coding, PDF pp. 75-79](Vibe%20Coding.pdf#page=75)

## Applying the Module to the Cloud Kitchen Assignment

The assignment asks me to audit and improve an existing simulation rather than replace it. I first need to establish a baseline by running the supplied program and tests. I then compare the code against each written requirement, preserve working behavior, make focused changes, add tests for every requirement I implement or correct, and record decisions in `PROJECT_SPEC.md` and `AI_USAGE_LOG.md`. [Assignment overview, How to Use the Provided Starter Code](mod_03_assignment/module_03_assignment.md#how-to-use-the-provided-starter-code)

The required business flow is:

1. Load the five data structures: recipes, inventory, orders, restock records, and status records.
2. Resolve each ordered item to a recipe and multiply ingredient demand by item quantity.
3. Check that every required ingredient exists, has enough quantity, and is usable based on expiry.
4. Deliver the whole order and deduct inventory only if every requirement passes. Otherwise, do not deduct any inventory, record the reason, and add the shortage to restock.
5. Process orders cumulatively so later orders use the inventory left by earlier delivered orders.
6. After processing, flag inventory that is out of stock, at or below 1,000 grams, expired, or within five days of expiry. The par level is 10,000 grams.
7. Produce a summary for a kitchen manager with delivery counts, failures and reasons, final inventory, and restock recommendations.

Source: [Assignment overview, Functional Requirements](mod_03_assignment/module_03_assignment.md#functional-requirements).

There is a source conflict I need to handle explicitly. The reference PDF describes partial fulfillment and periodic restocking in its proposed solution, while the newer assignment overview makes all-or-nothing fulfillment the base rule and treats partial fulfillment as optional. The assignment overview states that it takes precedence when the two conflict. I should therefore implement the Markdown requirements unless the instructor gives a later instruction. [Assignment overview, starter-code guidance and Requirement 4](mod_03_assignment/module_03_assignment.md#requirement-4-fulfill-orders-and-deduct-inventory) [Reference PDF, pp. 3-4 and 12](mod_03_assignment/AI-Assisted%20Cloud%20Kitchen%20Inventory%20Simulation.pdf#page=3)

## Assignment Readiness

I should be able to explain and demonstrate the following before submission:

- Why AI-generated code remains my responsibility.
- How the staged prompts and short iteration loop constrain scope and improve traceability.
- Which requirements the starter code already satisfies and which changes I made.
- How normal, boundary, and failure tests support each business rule.
- Why cumulative inventory must use the stock remaining after prior orders.
- How an explicit reference date makes expiry tests reproducible.
- How `PROJECT_SPEC.md` limits context drift and how `AI_USAGE_LOG.md` shows critical review rather than wholesale replacement.
- Why all-or-nothing fulfillment is the required base behavior despite the conflicting reference PDF.

The current assignment directory also has a baseline setup issue: `main.py` imports `seed_data`, but the supplied file is named `seed_data-1.py`. Running test discovery currently stops with `ModuleNotFoundError: No module named 'seed_data'`, so no test result can yet establish functional correctness. The required project file list calls for `seed_data.py`; renaming or copying must be handled as part of the assignment workflow, not mistaken for a logic failure. [Required Project Files](mod_03_assignment/module_03_assignment.md#required-project-files) [`main.py` import](mod_03_assignment/main.py) [`seed_data-1.py`](mod_03_assignment/seed_data-1.py)

## Specific Evidence to Remember

| Source | Specific evidence | Why it matters |
| --- | --- | --- |
| Mental model, [PDF pp. 7-9](Vibe%20Coding.pdf#page=7) | The model is presented as a probabilistic next-token generator, and the human has three roles: navigator, reviewer, and decision-maker. | Plausibility is not a correctness check; direction and acceptance remain human decisions. |
| Staged workflow, [PDF p. 24](Vibe%20Coding.pdf#page=24) | Four stages: plan, requirements, tasks, and one-task implementation. | I get a review checkpoint before errors compound. |
| Iteration loop, [PDF pp. 27-28](Vibe%20Coding.pdf#page=27) | Build, test, inspect, and refine; the example contrasts roughly 15-20 lines for one function with a 200-line pass. | The line counts are instructional examples, but they show how smaller review surfaces improve traceability. |
| Testing workflow, [PDF pp. 42-43](Vibe%20Coding.pdf#page=42) | Generate focused code, request tests immediately, run them locally, and feed failures back. Tests should cover normal, edge, and failure cases. | Generated test text has no evidentiary value until it is executed and reviewed. |
| Review checklist, [PDF p. 46](Vibe%20Coding.pdf#page=46) | Five checks cover requested behavior, hidden assumptions, hard-coded values, bad inputs, and sensitive logic. | This converts general skepticism into a repeatable review step. |
| Context management, [PDF pp. 61-62](Vibe%20Coding.pdf#page=61) | The AI has no reliable persistent memory between sessions; `PROJECT_SPEC.md` externalizes purpose, status, decisions, constraints, and next work. | Project continuity should come from an inspected artifact, not assumed model memory. |
| Duplication guidance, [PDF p. 66](Vibe%20Coding.pdf#page=66) | Run a duplication check after every three or four implementation tasks. | Local prompts can create competing sources of truth in the codebase. |
| Final playbook, [PDF pp. 75-76](Vibe%20Coding.pdf#page=75) | The course ends with an eight-step playbook and three risks: shallow understanding, technical debt, and misplaced confidence. | Completion requires comprehension, verification, and maintainability, not code generation alone. |
| Assignment rules, [Functional Requirements](mod_03_assignment/module_03_assignment.md#functional-requirements) | Low stock is quantity at or below 1,000g, par is 10,000g, and expiring soon is within five days of an explicit simulation date in tests. | These values should be named, tested business rules rather than scattered literals. |
| Supplied data, [`seed_data-1.py`](mod_03_assignment/seed_data-1.py) | The seed contains 5 recipes, 14 inventory records, 5 orders, 5 restock records, and 5 status records. | These counts support baseline connectivity tests, not full requirement coverage. |

## My Takeaway

I should treat AI-generated code as a draft produced by a fast collaborator with limited context. My advantage comes from directing it with explicit requirements and small tasks, then applying the same engineering controls I would use for human-authored code: review, independent tests, traceable decisions, configuration of business rules, and cleanup. For the assignment, the strongest evidence of learning will not be the amount of generated code. It will be a clear requirement audit, focused corrections, meaningful tests, an accurate project specification, and an AI usage log that records what I accepted, changed, or rejected.

## Glossary of Module Terms

| Term | Plain-language definition | Source |
| --- | --- | --- |
| **AI-assisted coding** | A development approach in which I describe intent and constraints, an AI generates or modifies code, and I direct, inspect, test, and decide whether to accept the result. | [Vibe Coding, PDF pp. 5 and 17](Vibe%20Coding.pdf#page=5) |
| **Vibe coding** | In this module, guiding code generation through natural language, examples, feedback, and iteration while retaining human review and control. | [Lecture 1, mental-model discussion](mod_03_lectures/V1%20AI%20Assisted%20Coding%20Complete_Captions_English%20%28United%20States%29.txt) |
| **Probabilistic generator** | A model that predicts plausible next tokens from learned patterns; it does not independently establish that code is correct. | [Vibe Coding, PDF p. 7](Vibe%20Coding.pdf#page=7) |
| **Navigator** | The human role that sets direction, defines the goal, divides the work, and keeps the whole project in view. | [Vibe Coding, PDF p. 9](Vibe%20Coding.pdf#page=9) |
| **Reviewer** | The human role that reads generated output and checks it for errors, gaps, assumptions, and drift from the request. | [Vibe Coding, PDF p. 9](Vibe%20Coding.pdf#page=9) |
| **Decision-maker** | The human role that accepts, rejects, revises, or redirects AI output and remains accountable for final quality. | [Vibe Coding, PDF p. 9](Vibe%20Coding.pdf#page=9) |
| **Monolithic prompt** | A large request that asks the AI to plan and implement many features at once, creating a broad and difficult review surface. | [Vibe Coding, PDF p. 23](Vibe%20Coding.pdf#page=23) |
| **Staged prompting workflow** | The sequence of asking for a plan, refining requirements, breaking components into tasks, and implementing one task at a time. | [Vibe Coding, PDF p. 24](Vibe%20Coding.pdf#page=24) |
| **Iterative development loop** | The repeated Build → Test → Inspect → Refine cycle used for each small unit of work. | [Vibe Coding, PDF pp. 26-27](Vibe%20Coding.pdf#page=26) |
| **Scope creep** | Generated work that extends beyond the requested task or changes code outside the agreed boundary. | [Vibe Coding, PDF pp. 31 and 33](Vibe%20Coding.pdf#page=31) |
| **Context drift** | Loss, weakening, or contradiction of earlier goals and constraints as a conversation or project grows. | [Vibe Coding, PDF p. 33](Vibe%20Coding.pdf#page=33) |
| **Unit test** | An executable check of a small piece of code against an expected result, including normal, edge, and failure behavior. | [Vibe Coding, PDF pp. 42-43](Vibe%20Coding.pdf#page=42) |
| **Context window** | The finite amount of information available to the model during generation; older details can lose influence or disappear. | [Vibe Coding, PDF pp. 60-61](Vibe%20Coding.pdf#page=60) |
| **`PROJECT_SPEC.md`** | An external project-memory file that records purpose, component status, decisions, constraints, and current and next tasks. | [Vibe Coding, PDF p. 62](Vibe%20Coding.pdf#page=62) |
| **Stub** | An intentionally incomplete function or placeholder that defines structure and can be tracked as a future implementation task. | [Vibe Coding, PDF pp. 63-64](Vibe%20Coding.pdf#page=63) |
| **Duplication** | Repeated logic that creates more than one source of truth and can lead to inconsistent fixes or behavior. | [Vibe Coding, PDF pp. 65-66](Vibe%20Coding.pdf#page=65) |
| **Validation hook** | An inline comment that exposes an assumption, uncertainty, or incomplete section so a reviewer can verify and resolve it. | [Vibe Coding, PDF pp. 67-68](Vibe%20Coding.pdf#page=67) |
| **Technical debt** | Future maintenance cost created here by unresolved stubs, duplicated logic, unchecked assumptions, and permanent TODOs. | [Vibe Coding, PDF p. 76](Vibe%20Coding.pdf#page=76) |
| **Par level** | The target inventory quantity used to calculate how much stock to order; the assignment sets it at 10,000 grams. | [Assignment overview, Requirement 6](mod_03_assignment/module_03_assignment.md#requirement-6-apply-restock-and-expiry-rules) |
