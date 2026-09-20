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

## Interaction 6: Optional Enhancements

**Task:** Implement partial fulfillment, predictive stockout alerts, dynamic menu-item disabling, and improved reporting.

**Prompt:** "Can you implement all the optional requirements? Option A: Partial Fulfillment. Option B: Predictive Stockout Alert. Option C: Dynamic Menu Item Disabling. Option D: Improved Reporting."

**AI response summary:** The AI compared three implementation structures and recommended extending the existing functional pipeline. It revised the design and requirements, added failing tests first, then implemented explicit atomic and partial policies, actual-consumption forecasting, one-serving menu availability, and Markdown report generation.

**My decision:** I accepted the functional extension because it preserves the supplied structure and the required atomic baseline. I accepted complete order lines as the smallest partial-delivery unit, actual deductions as the forecast input, a five-order default horizon, one-serving menu checks, and Markdown as the report format. I rejected a module split and class-based rewrite because they would add structure beyond the assignment need.

**Issues found:** The first report implementation placed three console sections after a return statement, so the base summary test failed. I kept the test failure as evidence, moved the sections back into the console function, escaped pipe characters in Markdown table cells, and reran the full suite.

## Interaction 7: Output Verification Artifact

**Task:** Create a final artifact that captures terminal and HTML output and compares the evidence with the requirements.

**Prompt:** "Can you create an artifact that is the output of running the program that tests how it works like logging the terminal output and html outputs to files and then comparing that output to the requirements as a last sanity check to make sure things are working as expected"

**AI response summary:** The AI added a self-contained HTML report and a verification harness. The harness runs the actual program and unit-test commands, captures both logs, copies the generated HTML, checks output expectations and EARS-to-test traceability, and writes a requirement comparison with an overall pass or fail result.

**My decision:** I accepted a generated evidence directory with stable filenames because it can be rerun before submission and reviewed without relying on conversational claims. I accepted subprocess execution because it validates the same commands a reviewer would run. I kept browser automation outside scope because the HTML structure, required sections, and escaping are directly tested.

**Issues found:** The initial evaluator fixture omitted restock and forecast text expected by the sanity rules. The failed test exposed that mismatch. I corrected the fixture, reran the suite, and then generated a passing evidence bundle from the real program.

## Verification

- Initial environment result: import failure caused by the supplied filename mismatch.
- Post-setup baseline: 20 supplied tests passed.
- Tests-first result: expected import failure for the planned summary interface.
- Base result: 27 tests passed.
- Enhanced tests-first result: expected import failure for the planned Markdown reporting interface.
- Enhancement result: 39 tests passed.
- Final result: 42 tests passed and the generated requirement sanity report returned PASS.
- `main.py` ran successfully, printed the enhanced business summary, and generated Markdown and HTML reports.
- `verify_outputs.py` generated terminal, test, HTML, and requirement-comparison artifacts.
- `main.py`, `seed_data.py`, and `test_main.py` passed Python compilation checks.

## What I Must Be Able to Explain

I remain responsible for the submission. Before submitting, I need to be able to explain the expiry boundary, atomic and partial fulfillment rules, cumulative inventory flow, restock quantity calculation, forecast assumptions, menu disabling rule, report generation, verification evidence, and why passing the original test suite was not enough evidence.
