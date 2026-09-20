---
parent: high-level-design
prefix: CKS
---

# Cloud Kitchen Simulation

## Context and Design Philosophy

The cloud kitchen simulation audits and completes a supplied procedural Python program. It uses lists of dictionaries from `seed_data.py` to evaluate orders against shared inventory, update delivery status, calculate restocking needs, and produce a manager-facing summary.

The design keeps the starter structure recognizable. Focused functions own business rules, while `process_orders` coordinates the cumulative, all-or-nothing order flow. Tests use controlled inputs and explicit dates so each business rule can be verified independently.

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
| Processed order | `order_id`, `brand`, `items`, `order_requirements`, `inventory_check`, `fulfilled`, `reason` |
| Expiry concern | `ingredient`, `expiry_date`, `days_until_expiry`, `status` |
| Summary | `delivered_count`, `not_delivered_count`, `delivered_order_ids`, `not_delivered_orders`, `final_inventory`, `restock_recommendations`, `expiry_concerns` |

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

## Fulfillment and Cumulative State

Orders are evaluated sequentially against a working inventory snapshot. An order succeeds only when every order line has a recipe and every combined ingredient requirement is available and usable.

For a delivered order, the simulation deducts all combined requirements and records `Delivered` in the status table. For a failed order, it records `Not Delivered` with the missing-recipe, missing-inventory, insufficient-stock, invalid-expiry, or expired-ingredient reasons. A failed order makes no inventory change.

Failure reasons are deterministic. Invalid order and missing-recipe issues follow order-line order. Unavailable ingredients follow their first appearance in the combined requirements. Categories are joined with ` | `, and names inside a category are joined with `, ` without duplicates.

After all orders are evaluated, the working quantities are copied to the caller's inventory table. Later orders therefore use inventory remaining after earlier delivered orders.

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

## Error Handling and Boundaries

The program treats an unknown recipe, missing inventory record, invalid expiry date, expired ingredient, and insufficient quantity as business failures rather than uncaught exceptions during order processing. It does not silently substitute ingredients, partially fulfill orders, or deduct stock after a failed check.

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
| Summary interface | Return structured data and print a manager-facing view | Console-only output or report file | A returned structure is testable and still supports the required console output without adding an optional reporting format. |

## Open Questions & Future Decisions

### Resolved

1. The Markdown assignment controls when it conflicts with the reference PDF.
2. The base simulation uses all-or-nothing fulfillment.
3. Expiry-sensitive tests use an explicit reference date.
4. Optional enhancements remain outside the base implementation.
5. Empty orders and invalid item quantities fail the complete order without deduction.
6. Restock output is consolidated to one record per ingredient with deterministic reason ordering.

### Deferred

1. Ingredient-name normalization and aliases are deferred because the supplied schema uses exact matching.
2. Persistence, concurrency control, and external inventory updates are deferred because this is an in-memory assignment simulation.
3. Duplicate identifiers and ingredient records are deferred because the supplied tables use unique keys.
4. Numeric validation beyond order-line quantity and floating-point rounding policy are deferred because the supplied data uses nonnegative integral grams.

## References

- `docs/high-level-design.md`
- `module_03/mod_03_assignment/module_03_assignment.md`
- `module_03/mod_03_assignment/AI-Assisted Cloud Kitchen Inventory Simulation.pdf`
- `module_03/module_03_learning_summary.md`
