# Cloud Kitchen Inventory Simulation Project Specification

## Project Purpose

This Python simulation evaluates cloud kitchen orders against shared recipe and inventory data. It supports required atomic fulfillment and optional item-level partial fulfillment, deducts inventory for delivered work, records failure reasons, recommends restocking, forecasts stockouts, identifies unavailable menu items, and produces console and Markdown reports for a kitchen manager.

The project audits and extends the supplied implementation. It preserves working starter behavior and changes only the areas needed to satisfy the assignment.

## Project Files

| File | Source | Purpose |
| --- | --- | --- |
| `main.py` | Provided and updated | Simulation logic, fulfillment policies, restocking, forecasts, menu availability, and reporting |
| `seed_data.py` | Provided as `seed_data-1.py`; renamed to the required filename | Five supplied data tables and their schema |
| `test_main.py` | Provided and expanded | Unit tests for normal, boundary, and failure behavior |
| `PROJECT_SPEC.md` | Created | Current requirements, decisions, status, and verification record |
| `AI_USAGE_LOG.md` | Created | AI prompts, recommendations, review decisions, and corrections |
| `WRITTEN_RESPONSE.md` | Created | Required written response and reflection |
| `BUSINESS_REPORT.md` | Generated | Improved Markdown report from the latest simulation run |
| `BUSINESS_REPORT.html` | Generated | Self-contained browser-readable report from the latest simulation run |
| `verify_outputs.py` | Created | Runs the program and tests, captures evidence, and evaluates requirements |
| `verification/` | Generated | Terminal log, unit-test log, HTML copy, and requirements sanity report |

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

Regenerate the complete verification evidence bundle with:

```bash
python verify_outputs.py
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
3. Atomic mode combines repeated ingredients across the complete order before inventory is checked. Partial mode checks each complete order line against inventory remaining after earlier delivered lines.
4. Empty orders fail without deduction. Non-positive or non-integer quantities reject their order in atomic mode and reject their line in partial mode.
5. An ingredient is usable only when it exists, has enough stock, and is not expired or marked with an invalid non-empty expiry value.
6. An ingredient expiring today or within five days remains usable but is reported as expiring soon.
7. Atomic fulfillment remains the default function policy. Any unknown recipe or unavailable ingredient fails the complete order without deduction.
8. Partial fulfillment evaluates complete order lines sequentially. It delivers the full requested quantity for an available line and rejects an unavailable line without splitting its quantity.
9. An order is delivered when every line succeeds, partially delivered when some lines succeed, and not delivered when no lines succeed. The supplied status boolean is true only for full delivery.
10. Orders and partial-delivery lines use cumulative inventory remaining after earlier deductions.
11. Out of stock means quantity at or below zero. Low stock means quantity greater than zero and at or below 1,000 grams.
12. The par level is 10,000 grams.
13. Restock recommendations retain all applicable reasons in a stable string and contain at most one record per ingredient.
14. Expired or invalid-expiry stock is treated as unusable and requires a full par-level replacement.
15. Stockout forecasts use actual fulfilled consumption divided by all observed orders and a five-order default horizon.
16. A menu item is unavailable when final inventory cannot produce one serving because an ingredient is missing, insufficient, depleted, expired, or has invalid expiry data.
17. The final summary, Markdown report, and HTML report include full, partial, and failed orders; inventory; restocking; expiry; stockout alerts; and unavailable menu items.
18. The verification harness runs the real program and test commands, captures their outputs, checks runtime evidence and EARS traceability, and returns a nonzero exit status if any check fails.

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
- Preserve atomic fulfillment as the default and select partial fulfillment explicitly in the command-line simulation.
- Treat a complete order line as the smallest partial-fulfillment unit.
- Forecast from actual deductions rather than requested or rejected demand.
- Generate `BUSINESS_REPORT.md` from the same structured summary used by the console.
- Generate a self-contained, escaped `BUSINESS_REPORT.html` from the same summary.
- Keep final verification reproducible through stable filenames under `verification/`.

## Testing Plan and Coverage

The 42-test suite covers:

- Access, record counts, field types, and display of all five data tables.
- Known and unknown recipe lookup.
- Quantity scaling and repeated-ingredient combination.
- Empty orders and invalid quantities.
- Complete availability result fields.
- Missing, insufficient, expired, expiring-soon, invalid-expiry, and missing-expiry cases.
- Successful delivery, atomic failure, status updates, and cumulative inventory.
- Zero stock, the 1,000 gram boundary, above-threshold stock, expiry, multiple reasons, shortage-derived restocking, and consolidation.
- Structured and printed business summaries.
- Atomic-policy preservation and partial fulfillment across available, unavailable, invalid, and competing order lines.
- Consumption-based stockout calculations, non-alert cases, and invalid forecast horizons.
- Missing, insufficient, depleted, expired, invalid-expiry, and expiring-soon menu availability.
- Enhanced summary fields, console sections, and a complete Markdown report.
- HTML structure, required sections, content escaping, and stale-file replacement.
- Passing and failing requirement-evidence comparisons, EARS completion, and test traceability.

Duplicate identifiers, duplicate inventory rows, ingredient aliases, persistence, concurrency, and floating-point rounding are outside the supplied assignment schema and remain deferred.

## Verification Record

| Stage | Result |
| --- | --- |
| Initial `python main.py` | Failed with `ModuleNotFoundError: No module named 'seed_data'` because the provided file was named `seed_data-1.py` |
| Initial test discovery | Failed on the same missing module before functional tests ran |
| After required filename correction | `main.py` exited successfully and all 20 supplied tests passed |
| Tests-first checkpoint | Expanded tests failed on the missing planned `build_business_summary` interface |
| Final verification | 27 tests passed; `main.py` exited successfully; Python compilation checks passed |
| Optional-enhancement tests-first checkpoint | Test discovery failed on the planned `generate_markdown_report` interface before implementation |
| Enhanced final verification | 39 tests passed; `main.py` generated `BUSINESS_REPORT.md`; Python compilation checks passed |
| Verification-artifact run | 42 tests passed; program and tests exited successfully; HTML report generated; all 12 sanity checks passed |

## Current Status

The base assignment, all four optional enhancements, and the final verification bundle are implemented. The generated `requirements_sanity_check.md` reports PASS. The next step is student review, addition of the required conversation export or link, and upload of the required files plus the report and verification artifacts selected for submission.

## Open Assumptions

- The instructor's Markdown assignment remains the controlling source if it conflicts with the reference PDF.
- The supplied table keys and identifier uniqueness remain valid.
- The runtime date is acceptable for the interactive sample run; tests use explicit dates for reproducibility.
