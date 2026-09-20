# AI Usage Log

## Disclosure Reference

OpenAI Codex. (2026, September 20). *AI-assisted cloud kitchen inventory simulation review and implementation*. (Yaw Etse, Interviewer).

The course permits generative AI throughout the workflow but requires me to verify the result and disclose the interaction. This log records the major prompts, response summaries, and my review decisions. The submitted conversation export or shared conversation link should accompany this reference if Canvas requires the complete transcript.

## Interaction 1: Planning and Source Review

**Task:** Plan the Module 03 assignment using the supplied assignment, module context, and a structured development workflow.

**Prompt:** "Using linked-intent-dev and context from module_03, let's do module_03_assignment.md."

**AI response summary:** The AI reviewed the assignment, course policy, module summary, starter files, and baseline setup. It proposed three implementation shapes and recommended preserving the supplied procedural program through an audit-first functional pipeline.

**My decision:** I accepted the audit-first option and a scope limited to the Module 03 assignment. I did not select the module-splitting or object-oriented alternatives because they would replace more starter structure than the assignment required.

**Issue found:** The initial program and test suite could not import `seed_data` because the supplied filename was `seed_data-1.py`.

## Interaction 2: High-Level Design

**Task:** Define project boundaries, business goals, non-goals, and verification standards before implementation.

**Prompt:** "Approve."

**AI response summary:** The AI created a high-level design that preserved the supplied schema, selected all-or-nothing fulfillment, required explicit dates in tests, and excluded optional enhancements from the base implementation.

**My decision:** I accepted the design. I kept optional partial fulfillment out of scope because the assignment lists it as an enhancement and makes all-or-nothing fulfillment the base rule.

## Interaction 3: Detailed Audit and Edge Cases

**Task:** Compare the starter implementation with inventory availability, fulfillment, restocking, expiry, and reporting requirements.

**Prompt:** "You have my approval to take the best recommendations and go all the way to implementation and development."

**AI response summary:** The AI identified missing expiry enforcement, single-reason restock behavior, missing restock context, no final summary, unresolved validation comments, and weak handling of invalid quantities. A separate edge probe also identified ambiguous date boundaries, mutation behavior, reason ordering, and empty-order behavior.

**My decision:** I accepted focused corrections for the base requirements. I accepted fail-closed handling for invalid expiry values and rejection of empty or invalid-quantity orders. I deferred aliases, duplicate-key handling, persistence, concurrency, and numeric rounding because the supplied schema does not require them.

**Issues found in the AI or starter assumptions:**

- The starter treated expiry as a restock-only concern and allowed expired inventory to fulfill orders.
- The starter gave expiring-soon stock a full 10,000 gram recommendation even when usable stock remained. I changed this to the amount needed to reach par, as the assignment states.
- A single `elif` chain discarded simultaneous restock reasons. I replaced it with stable reason accumulation.

## Interaction 4: Tests Before Implementation

**Task:** Convert the written requirements into executable normal, boundary, and failure cases.

**Prompt pattern used:** "Review the current cloud kitchen functions against the approved requirements. Add focused unit tests for missing, insufficient, expired, expiring-soon, invalid-expiry, cumulative, atomic-failure, restock, and summary behavior. Do not change implementation logic yet."

**AI response summary:** The AI expanded the supplied suite from 20 to 27 tests and connected each test to a requirement identifier. The first run failed because the planned `build_business_summary` function did not exist.

**My decision:** I accepted tests that directly represented assignment rules. I rejected treating the original green suite as proof of completion because it did not test expiry-based fulfillment, multiple restock reasons, missing inventory records, or the final business summary.

## Interaction 5: Focused Implementation and Refactoring

**Task:** Make the smallest code changes needed to satisfy the expanded suite and improve maintainability.

**Prompt pattern used:** "Implement the approved requirement-linked behavior in the existing main.py. Preserve the supplied schema and procedural structure. Run the full suite and report any failures before refactoring."

**AI response summary:** The AI added named thresholds, centralized expiry evaluation, enriched availability details, atomic failure reasons, consolidated restocking, a structured summary, and manager-facing output. It removed unresolved assumption comments after the decisions were verified.

**My decision:** I accepted the focused functions and constants. I did not split the program into new modules or introduce classes because that would expand scope without improving the assignment evidence.

## Verification

- Initial environment result: import failure caused by the supplied filename mismatch.
- Post-setup baseline: 20 supplied tests passed.
- Tests-first result: expected import failure for the planned summary interface.
- Final result: 27 tests passed.
- `main.py` ran successfully and printed all tables plus the final business summary.
- `main.py`, `seed_data.py`, and `test_main.py` passed Python compilation checks.

## What I Must Be Able to Explain

I remain responsible for the submission. Before submitting, I need to be able to explain the expiry boundary, atomic fulfillment rule, cumulative inventory flow, restock quantity calculation, reason consolidation, and why passing the original test suite was not enough evidence.
