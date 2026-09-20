---
parent: high-level-design
prefix: CKS
---

# Cloud Kitchen Simulation

## Context and Design Philosophy

The cloud kitchen simulation audits and extends a supplied procedural Python program. It uses lists of dictionaries from `seed_data.py` to evaluate orders against shared inventory, update delivery status, calculate restocking needs, forecast stockouts, identify unavailable menu items, and produce manager-facing console, Markdown, and HTML reports. A verification harness captures live outputs and checks them against the requirement set.

The design keeps the starter structure recognizable. Focused functions own business rules, while `process_orders` coordinates cumulative atomic and partial order flow. Tests use controlled inputs and explicit dates so each business rule can be verified independently.

## Data Contracts

The simulation preserves the five supplied table shapes:

| Table | Required fields |
| --- | --- |
| Recipes | `recipe_id`, `name`, `ingredients`; each ingredient has `name` and `qty_grams` |
| Inventory | `ingredient`, `qty_grams`, `expiry_date` |
| Orders | `order_id`, `brand`, `items`; each line has `item` and `qty` |
| Restock | `item`, `qty_needed_grams`, `reason`; calculated records also expose current quantity and expiry context |
| Status | `order_id`, `delivered`, `remark` |

Loader functions return the supplied tables, and display functions show every table. Processing operates on copies in the command-line entry point so importing and running the program does not alter `seed_data.py` module values.

Recipe and inventory ingredient names are exact-match keys. The supplied schema is expected to contain unique recipe names, inventory ingredient names, and order identifiers.

Calculated interfaces use these stable shapes:

| Result | Required fields |
| --- | --- |
| Availability detail | `ingredient`, `required_qty_grams`, `available_qty_grams`, `quantity_sufficient`, `expiry_status`, `is_usable`, `is_available`, `reason` |
| Processed order | `order_id`, `brand`, `items`, `order_requirements`, `inventory_check`, `fulfilled`, `fulfillment_status`, `reason`, `actual_consumption` |
| Processed item | `item`, `qty`, `recipe_found`, `valid_quantity`, `requirements`, `inventory_check`, `delivered`, `reason` |
| Expiry concern | `ingredient`, `expiry_date`, `days_until_expiry`, `status` |
| Stockout alert | `ingredient`, `current_qty_grams`, `observed_consumption_grams`, `average_consumption_per_order`, `forecast_horizon_orders`, `projected_qty_grams`, `estimated_orders_remaining` |
| Unavailable menu item | `item`, `blocking_ingredients` with ingredient and reason details |
| Summary | Base fulfillment, inventory, restock, and expiry fields plus `partially_delivered_count`, `partially_delivered_orders`, `stockout_alerts`, `unavailable_menu_items`, and `forecast_horizon_orders` |

## Recipe Resolution and Demand Calculation

Each order line is resolved by exact recipe name. A found recipe produces one requirement per ingredient, with recipe grams multiplied by the ordered quantity. Requirements from all order lines are combined by ingredient before inventory is checked. This prevents two menu items in one order from independently passing against the same stock.

An unknown recipe is recorded on the processed order and causes the complete order to fail without inventory deduction. No ingredient substitution is inferred.

An empty order, a non-integer quantity, or a quantity at or below zero is an invalid order. The simulation records the invalid line or empty-order reason, fails the complete order, and makes no deduction. Missing recipe names and invalid quantities are reported in order-line order.

## Inventory Usability

Availability is determined from existence, quantity, and expiry:

- A missing inventory record is unavailable with zero available grams.
- A record with fewer grams than required is insufficient.
- A record whose expiry date is before the reference date is expired and unusable.
- A record expiring from zero through five days after the reference date remains usable but carries an expiring-soon status.
- A record with a non-empty expiry value outside the `YYYY-MM-DD` format is unusable because the program cannot establish its safety.
- A record whose expiry key is absent or whose expiry value is `None` or blank is evaluated by quantity because expiry checking is conditional on expiry data being supplied.

Each availability detail includes the required and available quantities, quantity sufficiency, expiry status, usability, final availability, and a clear reason when unavailable.

`reference_date` accepts a `datetime.date` or `None`. `None` resolves once to `date.today()` for an interactive run. Unit tests and reproducible simulations pass a date explicitly.

## Fulfillment Policies and Cumulative State

Orders are evaluated sequentially against a working inventory snapshot. The caller selects `atomic` or `partial`; the function default remains `atomic` so the required base behavior remains available.

For a delivered order, the simulation deducts all combined requirements and records `Delivered` in the status table. For a failed order, it records `Not Delivered` with the missing-recipe, missing-inventory, insufficient-stock, invalid-expiry, or expired-ingredient reasons. A failed order makes no inventory change.

Failure reasons are deterministic. Invalid order and missing-recipe issues follow order-line order. Unavailable ingredients follow their first appearance in the combined requirements. Categories are joined with ` | `, and names inside a category are joined with `, ` without duplicates.

After all orders are evaluated, the working quantities are copied to the caller's inventory table. Later orders therefore use inventory remaining after earlier delivered orders.

In partial mode, each order line is the smallest fulfillment unit. A valid line is checked against inventory remaining after prior delivered lines. The complete requested quantity for that line is delivered and deducted, or the complete line is rejected without deduction. Unknown recipes, invalid quantities, and unavailable ingredients reject only their own line. An empty order remains not delivered. An order is `Delivered` when every line is delivered, `Partially Delivered` when at least one but not all lines are delivered, and `Not Delivered` when no line is delivered.

The supplied status table keeps its boolean field. It is `True` only for a fully delivered order and `False` for partial or failed orders; the remark carries the three-state result and line details. Each processed order also records the actual ingredient quantities deducted so forecasts can use observed consumption without reconstructing it from final inventory.

`process_orders` mutates the caller's inventory to the cumulative ending quantities, updates an existing status record by order ID or appends a new record, and replaces the caller's restock table with the final consolidated recommendations. Calling it again continues from the inventory passed to that call. A successful status uses boolean `True` and remark `Delivered`; a failed status uses boolean `False` and the same deterministic reason stored on the processed order.

## Restock and Expiry Evaluation

Restock evaluation uses named constants:

- Low-stock threshold: 1,000 grams
- Par level: 10,000 grams
- Expiring-soon window: five days

An inventory item can retain more than one applicable reason. Reasons use this stable order: `Out of stock` or `Running low on stock`, then `Expired`, `Expiring soon`, or `Invalid expiry`, then `Missing from inventory` or `Insufficient for order`. Reasons are joined with `; ` and are not duplicated. The `reason` field remains a string to preserve the supplied schema.

`Out of stock` applies at zero or negative quantity. `Running low on stock` applies when quantity is greater than zero and at or below 1,000 grams. For usable stock, quantity needed is the amount required to reach the 10,000 gram par level, with a minimum of zero. Expired or invalid-expiry stock is treated as zero usable stock and requires a full par-level replacement. A missing ingredient referenced by an unfulfilled order receives a restock record with zero current stock and a full par-level quantity. A large-order shortfall can produce an `Insufficient for order` recommendation with zero quantity needed when current usable stock is already at or above par.

Calculated restock records include `current_qty_grams`, `expiry_date`, and `days_until_expiry` so a manager can interpret the recommendation. A failure shortage is merged with stock and expiry rules rather than replacing them.

Restock is calculated once after all orders. It contains at most one record per ingredient, merges shortages from every failed order, and preserves first inventory or first shortage appearance order.

## Business Summary

The simulation returns a summary dictionary and prints it in plain language. The summary includes:

- delivered and undelivered order counts;
- delivered order identifiers;
- undelivered order identifiers and reasons;
- final inventory levels and expiry dates;
- restock recommendations with all reasons; and
- expiry concerns for expired and expiring-soon ingredients.

The returned structure supports direct unit testing. Console formatting remains a presentation layer over that structure.

## Predictive Stockout Alerts

The forecast aggregates `actual_consumption` from processed orders and divides by the number of observed orders. Rejected demand is excluded because it did not consume inventory. For each ingredient with positive observed consumption, the simulation projects final quantity after a caller-provided positive integer horizon. It emits an alert when estimated orders remaining are less than or equal to that horizon. Results preserve final-inventory order and include the observation totals, average rate, projected quantity, and estimated orders remaining.

The forecast is a simple simulation estimate, not a procurement prediction. It assumes the observed average remains constant and does not infer seasonality, delivery timing, or demand changes from five supplied orders.

## Dynamic Menu Availability

Menu availability is evaluated against final inventory and one serving of each recipe. A menu item is unavailable when any recipe ingredient is missing, has less than one-serving quantity, is at or below zero, is expired, or has an invalid expiry value. Expiring-soon ingredients remain usable. The result includes every blocking ingredient and reason so a manager can understand why the item should be disabled.

## Markdown and HTML Reports

The Markdown and HTML reports are rendered from the same structured summary used by console output. Both contain an executive summary, order outcomes including delivered and rejected lines, predictive stockout alerts, unavailable menu items, final inventory, restock recommendations, and expiry concerns. The caller supplies each output path; existing content at that exact path is replaced so a new simulation produces one current report. The HTML file is self-contained, escapes business values, and requires no external assets.

## Verification Evidence Bundle

`verify_outputs.py` runs `main.py` and the complete `unittest` suite as subprocesses from the assignment directory. It records standard output and standard error, preserves each command's exit result in the sanity report, and copies the generated HTML into a dedicated `verification/` folder.

The sanity comparison checks runtime evidence for data display, partial fulfillment, cumulative deduction, restocking and expiry, predictive stockouts, dynamic menu availability, and both report formats. It also checks that every EARS requirement is marked implemented and has a `@spec` annotation in the test suite. Each check records its requirement IDs, evidence source, observed evidence, and pass or fail result. The harness writes `requirements_sanity_check.md` and exits nonzero when any check fails.

The generated bundle uses stable filenames: `terminal_output.txt`, `unit_test_output.txt`, `business_report.html`, and `requirements_sanity_check.md`. Regeneration replaces only those files inside the selected output directory.

## Error Handling and Boundaries

The program treats an unknown recipe, missing inventory record, invalid expiry date, expired ingredient, and insufficient quantity as business failures rather than uncaught exceptions during order processing. It does not silently substitute ingredients or deduct stock for a rejected order or order line. Partial behavior occurs only when the caller selects the partial policy.

Malformed records that omit required non-expiry fields remain outside the simulation contract. Duplicate identifiers, duplicate recipe or inventory names, negative recipe or inventory quantities, and floating-point precision policy are also outside the supplied schema contract. This keeps the assignment focused on the supplied data while handling specified business failures explicitly.

## Decisions & Alternatives

| Decision | Chosen | Alternatives Considered | Rationale |
| --- | --- | --- | --- |
| Implementation boundary | Focused functions in `main.py` coordinated by `process_orders` | New modules or domain classes | The assignment requires targeted improvements to the supplied starter and grades the audit process. |
| Fulfillment policy | Atomic fulfillment for the complete order | Partial fulfillment | The assignment defines partial fulfillment as optional and requires no deduction after a base-case failure. |
| Expiry boundary | An ingredient expires only when its date is before the reference date | Treat the printed expiry date as unusable at the start of that date | The selected rule gives the date its ordinary through-date meaning and makes the zero-day case expiring soon. |
| Invalid expiry data | Fail closed for fulfillment | Ignore the invalid value or raise and stop all processing | A clear order failure avoids using stock whose safety cannot be established while allowing other orders to be evaluated. |
| Multiple restock reasons | Join ordered reasons in the existing string field | Replace the field with a list or keep only one prioritized reason | A joined string preserves the supplied schema and retains all required reasons. |
| Expired restock quantity | Treat expired stock as zero usable stock and request the full par level | Calculate par minus physical quantity | Physical expired stock cannot satisfy the target usable quantity. |
| Expiring-soon restock quantity | Request only par minus current usable quantity | Replace all expiring-soon stock | The assignment asks for quantity needed to reach par, and expiring-soon stock remains usable. |
| Summary interface | Return structured data, print a manager-facing view, and render Markdown from the same data | Independent console and report calculations | One structured source keeps console and report results consistent and directly testable. |
| Partial fulfillment granularity | Complete order line | Split line quantities or complete order only | The enhancement asks for deliverable items, while splitting a requested quantity would introduce a separate allocation rule. |
| Partial status mapping | Boolean `False` with a `Partially Delivered` remark | Boolean `True` or schema replacement | `True` continues to mean the full order was delivered, and the supplied schema remains intact. |
| Forecast denominator | All processed orders | Only fully or partly delivered orders | All processed orders represent the observed order window; rejected demand is already excluded from the numerator. |
| Menu disabling threshold | Enough usable inventory for one serving | Only exactly zero stock | One-serving availability prevents accepting an item the kitchen cannot actually prepare. |
| Improved reports | Markdown and self-contained HTML generated from the same summary | CSV or one report format | Two readable formats provide direct text and browser evidence without adding a third-party dependency. |
| Verification execution | Subprocesses running the actual CLI and unit-test commands | Calling internal functions from the verifier | Subprocess execution proves the user-facing entry points work and captures what a reviewer would see. |
| Sanity comparison | Output checks plus EARS and test-annotation coverage | A log-only bundle | A checked matrix connects runtime evidence to intent and fails visibly when expected evidence is missing. |

## Open Questions & Future Decisions

### Resolved

1. The Markdown assignment controls when it conflicts with the reference PDF.
2. Atomic fulfillment remains the default API policy, and the command-line simulation selects the optional partial policy explicitly.
3. Expiry-sensitive tests use an explicit reference date.
4. Optional enhancements remain outside the base implementation.
5. Empty orders and invalid item quantities fail the complete order without deduction.
6. Restock output is consolidated to one record per ingredient with deterministic reason ordering.

### Deferred

1. Ingredient-name normalization and aliases are deferred because the supplied schema uses exact matching.
2. Persistence, concurrency control, and external inventory updates are deferred because this is an in-memory assignment simulation.
3. Duplicate identifiers and ingredient records are deferred because the supplied tables use unique keys.
4. Numeric validation beyond order-line quantity and floating-point rounding policy are deferred because the supplied data uses nonnegative integral grams.
5. Partial quantity delivery within one order line is deferred because the enhancement is defined at the item-line level.
6. Forecast confidence intervals, seasonality, supplier lead time, and scheduled replenishment are deferred because the supplied data contains one short simulation window.
7. Browser automation and pixel-level visual comparison are deferred because the HTML report is static and its structure and escaped content are tested directly.

## References

- `docs/high-level-design.md`
- `module_03/mod_03_assignment/module_03_assignment.md`
- `module_03/mod_03_assignment/AI-Assisted Cloud Kitchen Inventory Simulation.pdf`
- `module_03/module_03_learning_summary.md`
