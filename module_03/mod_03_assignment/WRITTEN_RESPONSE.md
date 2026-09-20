# Module 3 Assignment Written Response

## Project Setup

The instructor provided `main.py`, `test_main.py`, and `seed_data-1.py`. I renamed the data file to the required `seed_data.py` and created `PROJECT_SPEC.md`, `AI_USAGE_LOG.md`, and this written response. Before the rename, both the program and test discovery failed with `ModuleNotFoundError`. After the rename, `main.py` ran and all 20 supplied tests passed.

From the assignment directory, I run the program with `python main.py` and the tests with `python -m unittest -v`.

## Data Loading and Audit

I verified that the five supplied tables are non-empty lists and retained their dictionary schemas. The loaders and display functions already worked once the filename matched the import. I kept that behavior and added a test that exercises all five display functions.

## Recipe Lookup Audit

The starter correctly used exact recipe-name matching, returned `None` for an unknown recipe, multiplied ingredient grams by item quantity, and combined shared ingredients across an order. I retained those functions and added a combined multi-item test. I also made empty orders and invalid quantities fail without changing inventory.

## Inventory Availability

The starter compared quantities but ignored expiry. I added one availability result per required ingredient with required grams, available grams, quantity sufficiency, expiry status, usability, final availability, and a failure reason. Expired and invalid-expiry inventory is unusable. Inventory expiring today or within five days remains usable but is reported as an expiry concern.

## Order Fulfillment

Fulfillment remains all-or-nothing. A complete order is delivered only when every item has a recipe and every combined ingredient requirement is available and usable. A failed order records deterministic reasons and deducts nothing. Existing status rows are updated, and missing status rows are appended.

## Cumulative Processing

The simulation processes orders sequentially against a working inventory copy. Each delivered order reduces the stock used for the next order. At the end, the final quantities are copied into the caller's inventory table. A test confirms that an earlier delivery can cause a later order to fail.

## Restock and Expiry Logic

I replaced the single-priority `elif` logic with consolidated reasons. The rules use constants for the 1,000 gram low-stock threshold, 10,000 gram par level, and five-day expiry window. One ingredient can retain low-stock, expiry, and failed-order reasons. Restock output now includes current quantity, quantity needed, expiry date, and days until expiry.

## Business Summary

The program now returns and prints a manager-facing summary with delivery counts, delivered IDs, failed orders and reasons, final inventory, restock recommendations, and expiry concerns. In the September 20, 2026 verification run, the supplied simulation delivered one order and rejected four because required ingredients were expired.

## Refactoring Notes

I made two main refactoring improvements. First, I replaced repeated numeric literals with named constants for stock and expiry rules. Second, I centralized expiry parsing and classification so availability, restocking, and reporting use the same boundary decisions. I also consolidated restock construction to prevent duplicate ingredient records and removed resolved assumption comments.

## AI Usage Summary

I used AI to inspect the starter code, compare it with the assignment, draft requirement-linked tests, identify edge cases, and propose focused corrections. I accepted changes only after reviewing the rule and running the tests. The detailed interaction record and disclosure reference are in `AI_USAGE_LOG.md`.

## Reflection

AI helped me move faster by turning a long assignment into a sequence of specific checks. It compared the starter functions with the written requirements, identified missing test cases, and suggested a structure for keeping the work traceable. That let me spend more time evaluating business rules instead of searching through the same files repeatedly. The project specification also gave the interaction a stable reference for decisions about expiry, all-or-nothing fulfillment, and restocking.

The AI and starter code both made assumptions that needed review. The largest problem was that the existing inventory check treated sufficient quantity as the complete availability decision. It did not prevent expired inventory from fulfilling an order. The restock function also used an `elif` chain, so one reason could hide another. An early assumption treated expiring-soon inventory as requiring a full 10,000 gram replacement. I rejected that interpretation because the assignment asks for the quantity needed to reach par, and expiring-soon stock remains usable.

Testing gave me evidence for deciding which suggestions to keep. The original 20 tests passed after the filename correction, but that result did not show that the assignment was complete. Those tests did not cover expired fulfillment, invalid expiry values, simultaneous restock reasons, missing inventory rows, or the final summary. I added tests for those gaps before changing the implementation. The expanded suite first failed because the planned summary interface did not exist, which confirmed that the tests could detect missing behavior. After implementation, all 27 tests passed.

I kept the AI suggestions that preserved the starter structure and made rules explicit. These included named constants, one expiry-classification helper, structured availability details, consolidated restock output, and a summary dictionary that can be tested before it is printed. I rejected broader module splitting and an object-oriented rewrite. Those options could be reasonable for a larger application, but they would add review work and weaken the assignment's focus on auditing the supplied code.

`PROJECT_SPEC.md` helped maintain context by separating current requirements from conversational suggestions. It records what the starter already did, what changed, the business-rule boundaries, current verification evidence, and deferred work. When the implementation decision became ambiguous, I could compare it with that record instead of relying on the AI's previous wording.

In a future AI-assisted project, I would establish the executable baseline and requirement-to-test map even earlier. I would also ask for edge cases before accepting an interface, then calculate a few expected results independently. AI is useful for generating candidate code and tests, but I need external specifications, small changes, and executable evidence to decide whether its output is correct.
