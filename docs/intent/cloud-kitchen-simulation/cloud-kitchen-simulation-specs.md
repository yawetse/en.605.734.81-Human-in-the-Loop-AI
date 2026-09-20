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
