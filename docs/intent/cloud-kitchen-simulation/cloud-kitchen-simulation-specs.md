# Cloud Kitchen Simulation Requirements

## Project Data

- [x] **CKS-DATA-001**: The cloud kitchen simulation shall import `recipes`, `inventory`, `orders`, `restock`, and `status` from `seed_data.py` and expose each table through its loader as a non-empty list.
- [x] **CKS-DATA-002**: When a table display function is called with its corresponding cloud kitchen records, the simulation shall print the identifying fields and business values for every record.

## Recipe Demand

- [x] **CKS-RECIPE-001**: When an order line names a recipe in the supplied recipe table, the simulation shall return that recipe, and when no recipe matches, the simulation shall return no recipe without raising an error.
- [x] **CKS-RECIPE-002**: When calculating demand for a complete order, the simulation shall multiply every recipe ingredient by the ordered item quantity and combine repeated ingredients across all order lines before checking inventory.
- [x] **CKS-RECIPE-003**: If an order is empty or an order line has a non-integer quantity or a quantity at or below zero, then the simulation shall mark the complete order not delivered, record the invalid-order reason, and leave inventory unchanged for that order.

## Inventory Availability

- [x] **CKS-INVENTORY-001**: When checking a complete order's combined requirements, the simulation shall report each ingredient's required grams, available grams, quantity sufficiency, usability, final availability, and any failure reason.
- [x] **CKS-INVENTORY-002**: If a required ingredient is absent or has fewer grams than the complete order requires, then the simulation shall mark that ingredient unavailable and identify it as missing or insufficient.
- [x] **CKS-INVENTORY-003**: If a required ingredient's expiry date is before the inventory check reference date, then the simulation shall mark that ingredient expired, unusable, and unavailable.
- [x] **CKS-INVENTORY-004**: When a required ingredient expires from zero through five days after the inventory check reference date, the simulation shall mark it expiring soon but usable when its quantity is sufficient.
- [x] **CKS-INVENTORY-005**: If a required ingredient has an invalid expiry value, then the simulation shall mark it unusable and unavailable, and if expiry data is absent, the simulation shall evaluate availability from existence and quantity.

## Fulfillment

- [x] **CKS-FULFILL-001**: When every order line has a recipe and every combined ingredient requirement is available and usable, the simulation shall mark the complete order delivered and deduct each required quantity exactly once.
- [x] **CKS-FULFILL-002**: If any order line lacks a recipe or any required ingredient is missing, insufficient, expired, or otherwise unusable, then the simulation shall mark the complete order not delivered, record the reasons, and leave inventory unchanged for that order.
- [x] **CKS-FULFILL-003**: When processing multiple orders, the simulation shall evaluate each order against inventory remaining after all earlier delivered orders and shall expose the final cumulative inventory to the caller.
- [x] **CKS-FULFILL-004**: When fulfillment is decided, the simulation shall update an existing status record for the order or append one when the order has no status record.

## Restocking

- [x] **CKS-RESTOCK-001**: After order processing, the simulation shall recommend restocking for ingredients with zero stock or stock at or below 1,000 grams and shall calculate the nonnegative quantity needed to reach the 10,000 gram par level.
- [x] **CKS-RESTOCK-002**: After order processing, the simulation shall recommend a full par-level replacement for expired inventory and shall identify usable inventory expiring within five days of the reference date.
- [x] **CKS-RESTOCK-003**: When an ingredient qualifies for more than one restock reason, the simulation shall preserve every applicable reason in a stable combined reason string.
- [x] **CKS-RESTOCK-004**: When an order fails because an ingredient is absent, insufficient, expired, or otherwise unusable, the simulation shall include that ingredient and the order-shortage reason in the final restock recommendations.
- [x] **CKS-RESTOCK-005**: Each calculated restock recommendation shall include the ingredient name, current grams, quantity needed, reason, expiry date when available, and days until expiry when calculable.
- [x] **CKS-RESTOCK-006**: After all orders are processed, the simulation shall replace the live restock table with at most one consolidated record per ingredient, without duplicate reasons, in first inventory or shortage appearance order.

## Business Summary

- [x] **CKS-REPORT-001**: When the simulation builds its final business summary, it shall return delivered and undelivered counts, delivered order identifiers, undelivered order reasons, final inventory, restock recommendations, and expiry concerns.
- [x] **CKS-REPORT-002**: When the command-line simulation completes, it shall print a manager-facing summary containing delivery counts, failed-order reasons, final inventory, restock recommendations, and expiry concerns.

## Partial Fulfillment

- [x] **CKS-PARTIAL-001**: When partial fulfillment is selected, the simulation shall evaluate order lines sequentially against cumulative inventory and shall deduct the full requested quantity for each available and usable line without deducting inventory for a rejected line.
- [x] **CKS-PARTIAL-002**: When partial fulfillment delivers at least one but not every order line, the simulation shall mark the order `Partially Delivered`, identify delivered and rejected lines with reasons, and keep the status-table delivered flag false.
- [x] **CKS-PARTIAL-003**: When atomic fulfillment is selected or omitted, the simulation shall preserve complete-order all-or-nothing behavior.

## Predictive Stockout Alerts

- [x] **CKS-FORECAST-001**: When forecasting stockouts, the simulation shall calculate each ingredient's average consumption per observed order from quantities actually deducted for delivered order lines and shall exclude rejected demand.
- [x] **CKS-FORECAST-002**: When an ingredient's estimated orders remaining is less than or equal to the configured positive integer forecast horizon, the simulation shall emit an alert containing current quantity, observed consumption, average consumption per order, projected quantity, horizon, and estimated orders remaining.
- [x] **CKS-FORECAST-003**: If the forecast horizon is not a positive integer, then the simulation shall reject it with a clear error.

## Dynamic Menu Availability

- [x] **CKS-MENU-001**: After order processing, the simulation shall identify each recipe that cannot produce one complete serving because an ingredient is missing, insufficient, depleted, expired, or has an invalid expiry value.
- [x] **CKS-MENU-002**: When a menu item is unavailable, the simulation shall report every blocking ingredient with a clear reason while treating expiring-soon inventory as usable.

## Improved Reporting

- [x] **CKS-REPORT-003**: When optional enhancement results are supplied, the structured business summary shall include partial-delivery counts and line outcomes, predictive stockout alerts, unavailable menu items, and the forecast horizon without removing required base fields.
- [x] **CKS-REPORT-004**: When the enhanced business summary is printed, the console output shall include partial deliveries, predictive stockout alerts, and unavailable menu items.
- [x] **CKS-REPORT-005**: When a Markdown report path is supplied, the simulation shall replace that file with a business-readable report containing an executive summary, order outcomes, stockout alerts, unavailable menu items, final inventory, restock recommendations, and expiry concerns.
- [x] **CKS-REPORT-006**: When an HTML report path is supplied, the simulation shall replace that file with a self-contained, escaped, browser-readable report containing the same business sections as the Markdown report.

## Verification Evidence

- [x] **CKS-VERIFY-001**: When the verification harness runs, it shall execute the real command-line program and save its standard output and standard error to `terminal_output.txt`.
- [x] **CKS-VERIFY-002**: When the verification harness runs, it shall execute the complete unit-test suite and save its standard output and standard error to `unit_test_output.txt`.
- [x] **CKS-VERIFY-003**: When the verification harness completes its commands, it shall copy the generated HTML report into the verification directory and write `requirements_sanity_check.md` with requirement IDs, evidence sources, observed evidence, and pass or fail results.
- [x] **CKS-VERIFY-004**: If any command fails, expected runtime evidence is absent, any EARS requirement is unchecked, or any EARS requirement lacks a test annotation, then the verification harness shall report an overall failure and exit nonzero.
- [x] **CKS-VERIFY-005**: When the verification harness is rerun for a selected output directory, it shall replace only the stable verification artifact filenames and shall report an overall pass when every sanity check succeeds.
