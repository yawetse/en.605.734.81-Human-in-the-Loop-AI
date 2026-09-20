# Cloud Kitchen Business Report

**Simulation date:** 2026-09-20

## Executive Summary

- Orders delivered: 1
- Orders partially delivered: 1
- Orders not delivered: 3
- Predictive stockout alerts: 1
- Unavailable menu items: 4

## Order Outcomes

| Order | Status | Details |
| --- | --- | --- |
| 2 | Delivered | Delivered |
| 5 | Partially Delivered | Partially Delivered: Chicken Burger \| Not Delivered: Caesar Salad (Romaine Lettuce (Expired)) |
| 1 | Not Delivered | Not Delivered: Margherita Pizza (Flour (Expired)), Caesar Salad (Romaine Lettuce (Expired)) |
| 3 | Not Delivered | Not Delivered: Pasta Alfredo (Fettuccine Pasta (Expired)), Chocolate Cake (Flour (Expired), Chocolate (Expired), Sugar (Expired)) |
| 4 | Not Delivered | Not Delivered: Margherita Pizza (Flour (Expired)) |

## Predictive Stockout Alerts

| Ingredient | Current g | Avg g/order | Horizon | Projected g | Orders remaining |
| --- | --- | --- | --- | --- | --- |
| Chicken Breast | 800 | 1840.0 | 5 | -8400.0 | 0.43 |

## Unavailable Menu Items

| Menu item | Blocking ingredients |
| --- | --- |
| Margherita Pizza | Flour: Expired |
| Caesar Salad | Romaine Lettuce: Expired |
| Pasta Alfredo | Fettuccine Pasta: Expired |
| Chocolate Cake | Flour: Expired; Chocolate: Expired; Sugar: Expired |

## Final Inventory

| Ingredient | Quantity g | Expiry date |
| --- | --- | --- |
| Flour | 10000 | 2026-05-12 |
| Tomato Sauce | 10000 | 2026-11-15 |
| Mozzarella Cheese | 10000 | 2026-10-20 |
| Chicken Breast | 800 | 2026-10-10 |
| Romaine Lettuce | 10000 | 2026-05-12 |
| Caesar Dressing | 10000 | 2026-10-15 |
| Croutons | 10000 | 2026-10-18 |
| Bun | 5400 | 2026-10-09 |
| Lettuce | 7700 | 2026-10-09 |
| Fettuccine Pasta | 10000 | 2026-01-31 |
| Cream | 10000 | 2026-10-12 |
| Parmesan Cheese | 10000 | 2026-10-15 |
| Chocolate | 10000 | 2026-01-15 |
| Sugar | 10000 | 2026-05-12 |

## Restock Recommendations

| Ingredient | Current g | Order g | Reason |
| --- | --- | --- | --- |
| Flour | 10000 | 10000 | Expired |
| Chicken Breast | 800 | 9200 | Running low on stock |
| Romaine Lettuce | 10000 | 10000 | Expired |
| Fettuccine Pasta | 10000 | 10000 | Expired |
| Chocolate | 10000 | 10000 | Expired |
| Sugar | 10000 | 10000 | Expired |

## Expiry Concerns

| Ingredient | Status | Expiry date | Days |
| --- | --- | --- | --- |
| Flour | Expired | 2026-05-12 | -131 |
| Romaine Lettuce | Expired | 2026-05-12 | -131 |
| Fettuccine Pasta | Expired | 2026-01-31 | -232 |
| Chocolate | Expired | 2026-01-15 | -248 |
| Sugar | Expired | 2026-05-12 | -131 |
