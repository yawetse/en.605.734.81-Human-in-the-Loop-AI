# Cloud Kitchen Inventory Simulation Project Specification

## Project Purpose

This Python simulation evaluates cloud kitchen orders against shared recipe and inventory data. It determines whether each complete order can be delivered, deducts inventory for delivered orders, records failure reasons for undelivered orders, recommends restocking, identifies expiry concerns, and produces a summary for a kitchen manager.

The project audits and extends the supplied implementation. It preserves working starter behavior and changes only the areas needed to satisfy the assignment.

## Project Files

| File | Source | Purpose |
| --- | --- | --- |
| `main.py` | Provided and updated | Simulation logic, table display, fulfillment, restocking, and business summary |
| `seed_data.py` | Provided as `seed_data-1.py`; renamed to the required filename | Five supplied data tables and their schema |
| `test_main.py` | Provided and expanded | Unit tests for normal, boundary, and failure behavior |
| `PROJECT_SPEC.md` | Created | Current requirements, decisions, status, and verification record |
| `AI_USAGE_LOG.md` | Created | AI prompts, recommendations, review decisions, and corrections |
| `WRITTEN_RESPONSE.md` | Created | Required written response and reflection |

## How to Run

From `module_03/mod_03_assignment`:

```bash
python main.py
python -m unittest -v
```

The direct test command also works:

```bash
python test_main.py
```

## Supplied Data Structures

The program uses the supplied lists of dictionaries without redesigning them:

- `recipes`: recipe ID, menu item name, and ingredient grams.
- `inventory`: ingredient name, available grams, and expiry date.
- `orders`: order ID, brand, menu items, and quantities.
- `restock`: ingredient, quantity needed, and reason.
- `status`: order ID, delivered flag, and remark.

Calculated restock records preserve the supplied keys and add current quantity and expiry context required by the assignment.

## Business Rules

1. Recipe names and ingredient names use exact matching.
2. Order-line demand equals each recipe quantity multiplied by the ordered quantity.
3. Repeated ingredients are combined across the complete order before inventory is checked.
4. Empty orders and non-positive or non-integer quantities fail without deduction.
5. An ingredient is usable only when it exists, has enough stock, and is not expired or marked with an invalid non-empty expiry value.
6. An ingredient expiring today or within five days remains usable but is reported as expiring soon.
7. Fulfillment is all-or-nothing. Any unknown recipe or unavailable ingredient fails the complete order.
8. Delivered orders deduct inventory exactly once. Failed orders deduct nothing.
9. Orders are processed sequentially against inventory remaining after earlier deliveries.
10. Out of stock means quantity at or below zero. Low stock means quantity greater than zero and at or below 1,000 grams.
11. The par level is 10,000 grams.
12. Restock recommendations retain all applicable reasons in a stable string and contain at most one record per ingredient.
13. Expired or invalid-expiry stock is treated as unusable and requires a full par-level replacement.
14. The final summary reports delivered and undelivered orders, failure reasons, final inventory, restocking, and expiry concerns.

## Starter-Code Audit

### Already implemented and retained

- Loaders and console displays for all five supplied tables.
- Exact recipe lookup and graceful `None` result for an unknown recipe.
- Ingredient scaling by item quantity.
- Combining repeated ingredients across an order.
- All-or-nothing inventory deduction.
- Cumulative order processing through a working inventory copy.
- Updating existing status records or appending new ones.
- Basic low-stock, out-of-stock, and expiring-soon calculations.

### Gaps corrected

- The supplied filename did not match the `seed_data` import.
- Availability ignored expiry dates.
- Expired inventory could fulfill orders.
- Invalid expiry values had no controlled behavior.
- Restocking allowed one reason to overwrite another.
- Missing or insufficient ingredients were not always retained in final restock output.
- Restock records omitted current quantity and expiry context.
- Expired inventory was not restocked.
- Empty orders and invalid quantities could produce incorrect results.
- The starter had no structured manager-facing final summary.
- Business thresholds were repeated literals rather than named constants.

## Design Decisions

- Keep focused functions in `main.py` rather than introducing new modules or classes.
- Use explicit reference dates in tests. Interactive execution resolves the date once at startup.
- Treat the printed expiry date as usable through that date. A date before the reference date is expired.
- Fail closed on a non-empty invalid expiry value.
- Preserve simultaneous restock reasons in the supplied string field, separated by `; `.
- Return the business summary as a dictionary and print a plain-language view.

## Testing Plan and Coverage

The 27-test suite covers:

- Access, record counts, field types, and display of all five data tables.
- Known and unknown recipe lookup.
- Quantity scaling and repeated-ingredient combination.
- Empty orders and invalid quantities.
- Complete availability result fields.
- Missing, insufficient, expired, expiring-soon, invalid-expiry, and missing-expiry cases.
- Successful delivery, atomic failure, status updates, and cumulative inventory.
- Zero stock, the 1,000 gram boundary, above-threshold stock, expiry, multiple reasons, shortage-derived restocking, and consolidation.
- Structured and printed business summaries.

Duplicate identifiers, duplicate inventory rows, ingredient aliases, persistence, concurrency, and floating-point rounding are outside the supplied assignment schema and remain deferred.

## Verification Record

| Stage | Result |
| --- | --- |
| Initial `python main.py` | Failed with `ModuleNotFoundError: No module named 'seed_data'` because the provided file was named `seed_data-1.py` |
| Initial test discovery | Failed on the same missing module before functional tests ran |
| After required filename correction | `main.py` exited successfully and all 20 supplied tests passed |
| Tests-first checkpoint | Expanded tests failed on the missing planned `build_business_summary` interface |
| Final verification | 27 tests passed; `main.py` exited successfully; Python compilation checks passed |

## Current Status

The base assignment functionality and required project documents are complete. The implementation contains no optional enhancement. The next step is student review, addition of any required conversation export to the course submission, and upload of the required files.

## Open Assumptions

- The instructor's Markdown assignment remains the controlling source if it conflicts with the reference PDF.
- The supplied table keys and identifier uniqueness remain valid.
- The runtime date is acceptable for the interactive sample run; tests use explicit dates for reproducibility.
