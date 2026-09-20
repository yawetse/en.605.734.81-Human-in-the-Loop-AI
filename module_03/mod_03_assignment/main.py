"""Cloud kitchen order, inventory, restock, and reporting simulation."""

from copy import deepcopy
from datetime import date, datetime
from html import escape
from pathlib import Path

from seed_data import inventory, orders, recipes, restock, status


LOW_STOCK_THRESHOLD_GRAMS = 1000
PAR_LEVEL_GRAMS = 10000
EXPIRING_SOON_DAYS = 5
ATOMIC_FULFILLMENT = "atomic"
PARTIAL_FULFILLMENT = "partial"
DEFAULT_FORECAST_HORIZON_ORDERS = 5


def _resolve_reference_date(reference_date):
    """Return a reproducible date for expiry calculations."""
    if reference_date is None:
        return date.today()
    if not isinstance(reference_date, date) or isinstance(reference_date, datetime):
        raise TypeError("reference_date must be a datetime.date or None")
    return reference_date


def _expiry_context(item, reference_date):
    """Return expiry status, day offset, and usability for an inventory record."""
    expiry_value = item.get("expiry_date")
    if expiry_value is None or (isinstance(expiry_value, str) and not expiry_value.strip()):
        return "Not provided", None, True
    if not isinstance(expiry_value, str):
        return "Invalid expiry", None, False

    try:
        expiry_date = datetime.strptime(expiry_value, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid expiry", None, False

    days_until_expiry = (expiry_date - reference_date).days
    if days_until_expiry < 0:
        return "Expired", days_until_expiry, False
    if days_until_expiry <= EXPIRING_SOON_DAYS:
        return "Expiring soon", days_until_expiry, True
    return "Valid", days_until_expiry, True


def _append_unique(items, value):
    """Append a value while preserving first-seen order."""
    if value not in items:
        items.append(value)


# @spec CKS-DATA-001
def load_recipes():
    """Return the seeded recipe records for use in the application."""
    return recipes


# @spec CKS-DATA-002
def print_recipes(recipe_data):
    """Print every recipe and its ingredient requirements to the console."""
    print("\n=== Recipes ===")
    for recipe in recipe_data:
        print(f"Recipe ID: {recipe['recipe_id']}")
        print(f"Name: {recipe['name']}")
        print("Ingredients:")
        for ingredient in recipe["ingredients"]:
            print(f"  - {ingredient['name']}: {ingredient['qty_grams']} grams")
        print()


# @spec CKS-DATA-001
def load_inventory():
    """Return the seeded inventory records for the simulation."""
    return inventory


# @spec CKS-DATA-002
def print_inventory(inventory_data):
    """Print every inventory item with quantity and expiry information."""
    print("\n=== Inventory ===")
    for item in inventory_data:
        print(f"Ingredient: {item['ingredient']}")
        print(f"Quantity: {item['qty_grams']} grams")
        print(f"Expiry Date: {item['expiry_date']}")
        print()


# @spec CKS-DATA-001
def load_orders():
    """Return the seeded customer order records."""
    return orders


# @spec CKS-DATA-002
def print_orders(order_data):
    """Print every order, including its brand and requested items."""
    print("\n=== Orders ===")
    for order in order_data:
        print(f"Order ID: {order['order_id']}")
        print(f"Brand: {order['brand']}")
        print("Items:")
        for item in order["items"]:
            print(f"  - {item['item']}: {item['qty']}")
        print()


# @spec CKS-DATA-001
def load_restock():
    """Return the seeded restock recommendations."""
    return restock


# @spec CKS-DATA-002
def print_restock(restock_data):
    """Print every restock item with quantity needed and reason."""
    print("\n=== Restock ===")
    for item in restock_data:
        print(f"Item: {item['item']}")
        if "current_qty_grams" in item:
            print(f"Current Quantity: {item['current_qty_grams']} grams")
        print(f"Quantity Needed: {item['qty_needed_grams']} grams")
        print(f"Reason: {item['reason']}")
        if item.get("expiry_date") is not None:
            print(f"Expiry Date: {item['expiry_date']}")
        if item.get("days_until_expiry") is not None:
            print(f"Days Until Expiry: {item['days_until_expiry']}")
        print()


# @spec CKS-DATA-001
def load_status():
    """Return the seeded delivery status records."""
    return status


# @spec CKS-DATA-002
def print_status(status_data):
    """Print every order status with delivery result and remark."""
    print("\n=== Status ===")
    for entry in status_data:
        print(f"Order ID: {entry['order_id']}")
        print(f"Delivered: {entry['delivered']}")
        print(f"Remark: {entry['remark']}")
        print()


# @spec CKS-RECIPE-001
def find_recipe_by_name(recipe_data, item_name):
    """Return the recipe that matches an order item name, or None if missing."""
    for recipe in recipe_data:
        if recipe["name"] == item_name:
            return recipe
    return None


# @spec CKS-RECIPE-002
def calculate_ingredient_requirements(recipe, quantity):
    """Return the total grams required for each ingredient in an order item."""
    requirements = []

    # Step 2: multiply each recipe ingredient quantity by the ordered item count
    # so we know the total grams needed to prepare that order item.
    for ingredient in recipe["ingredients"]:
        requirements.append(
            {
                "name": ingredient["name"],
                "required_qty_grams": ingredient["qty_grams"] * quantity,
            }
        )

    return requirements


# @spec CKS-INVENTORY-001, CKS-INVENTORY-002, CKS-INVENTORY-003, CKS-INVENTORY-004, CKS-INVENTORY-005
def check_inventory_availability(inventory_data, requirements, reference_date=None):
    """Evaluate required quantities and expiry usability for a complete order."""
    reference_date = _resolve_reference_date(reference_date)
    inventory_lookup = {item["ingredient"]: item for item in inventory_data}
    availability_results = []

    for requirement in requirements:
        ingredient_name = requirement["name"]
        required_qty = requirement["required_qty_grams"]
        inventory_item = inventory_lookup.get(ingredient_name)

        if inventory_item is None:
            availability_results.append(
                {
                    "ingredient": ingredient_name,
                    "required_qty_grams": required_qty,
                    "available_qty_grams": 0,
                    "quantity_sufficient": False,
                    "expiry_status": "Not provided",
                    "is_usable": False,
                    "is_available": False,
                    "reason": "Missing from inventory",
                }
            )
            continue

        available_qty = inventory_item["qty_grams"]
        quantity_sufficient = available_qty >= required_qty
        expiry_status, _, is_usable = _expiry_context(inventory_item, reference_date)
        reasons = []
        if not quantity_sufficient:
            reasons.append("Insufficient quantity")
        if expiry_status in ("Expired", "Invalid expiry"):
            reasons.append(expiry_status)

        is_available = quantity_sufficient and is_usable
        availability_results.append(
            {
                "ingredient": ingredient_name,
                "required_qty_grams": required_qty,
                "available_qty_grams": available_qty,
                "quantity_sufficient": quantity_sufficient,
                "expiry_status": expiry_status,
                "is_usable": is_usable,
                "is_available": is_available,
                "reason": "; ".join(reasons),
            }
        )

    return {
        "all_available": all(detail["is_available"] for detail in availability_results),
        "details": availability_results,
    }


# @spec CKS-RECIPE-002
def combine_requirements(requirement_groups):
    """Merge repeated ingredient requirements into a single total per ingredient."""
    combined_requirements = {}

    # Step 2: combine ingredient demand across all items in the same order so
    # fulfillment is checked against the total grams needed for the entire order.
    for requirements in requirement_groups:
        for requirement in requirements:
            ingredient_name = requirement["name"]
            combined_requirements.setdefault(ingredient_name, 0)
            combined_requirements[ingredient_name] += requirement["required_qty_grams"]

    return [
        {"name": ingredient_name, "required_qty_grams": required_qty}
        for ingredient_name, required_qty in combined_requirements.items()
    ]


def deduct_inventory(inventory_data, requirements):
    """Subtract the used ingredient grams from inventory after a successful order."""
    inventory_lookup = {item["ingredient"]: item for item in inventory_data}
    for requirement in requirements:
        inventory_lookup[requirement["name"]]["qty_grams"] -= requirement["required_qty_grams"]


def apply_final_inventory_snapshot(inventory_data, final_inventory_data):
    """Copy the final cumulative inventory quantities back into the main table."""
    final_inventory_lookup = {
        item["ingredient"]: item["qty_grams"] for item in final_inventory_data
    }

    # Step 6: update the final inventory table only after all orders have been
    # processed so the printed inventory reflects the true remaining stock.
    for item in inventory_data:
        if item["ingredient"] in final_inventory_lookup:
            item["qty_grams"] = final_inventory_lookup[item["ingredient"]]


def update_status_entry(status_data, order_id, delivered, remark):
    """Update or create a status-table entry for a processed order."""
    for entry in status_data:
        if entry["order_id"] == order_id:
            entry["delivered"] = delivered
            entry["remark"] = remark
            return

    status_data.append({"order_id": order_id, "delivered": delivered, "remark": remark})


# @spec CKS-RESTOCK-001, CKS-RESTOCK-002, CKS-RESTOCK-003, CKS-RESTOCK-004, CKS-RESTOCK-005
def calculate_restock_needs(inventory_data, reference_date=None, shortage_reasons=None):
    """Build one consolidated recommendation per affected ingredient."""
    reference_date = _resolve_reference_date(reference_date)
    shortage_reasons = shortage_reasons or {}
    inventory_lookup = {item["ingredient"]: item for item in inventory_data}
    ingredient_order = [item["ingredient"] for item in inventory_data]
    for ingredient_name in shortage_reasons:
        if ingredient_name not in inventory_lookup:
            ingredient_order.append(ingredient_name)

    recommendations = []
    for ingredient_name in ingredient_order:
        item = inventory_lookup.get(ingredient_name)
        current_qty = item["qty_grams"] if item is not None else 0
        expiry_value = item.get("expiry_date") if item is not None else None
        expiry_status, days_until_expiry, _ = (
            _expiry_context(item, reference_date)
            if item is not None
            else ("Not provided", None, False)
        )

        reasons = []
        if current_qty <= 0:
            reasons.append("Out of stock")
        elif current_qty <= LOW_STOCK_THRESHOLD_GRAMS:
            reasons.append("Running low on stock")

        if expiry_status in ("Expired", "Expiring soon", "Invalid expiry"):
            reasons.append(expiry_status)

        for reason in shortage_reasons.get(ingredient_name, []):
            _append_unique(reasons, reason)

        if not reasons:
            continue

        unusable_stock = item is None or expiry_status in ("Expired", "Invalid expiry")
        qty_needed = PAR_LEVEL_GRAMS if unusable_stock else max(PAR_LEVEL_GRAMS - max(current_qty, 0), 0)
        recommendations.append(
            {
                "item": ingredient_name,
                "current_qty_grams": current_qty,
                "qty_needed_grams": qty_needed,
                "reason": "; ".join(reasons),
                "expiry_date": expiry_value,
                "days_until_expiry": days_until_expiry,
            }
        )

    return recommendations


# @spec CKS-RESTOCK-006
def refresh_restock_table(
    restock_data,
    inventory_data,
    reference_date=None,
    shortage_reasons=None,
):
    """Replace the live restock table with consolidated final recommendations."""
    restock_data.clear()
    restock_data.extend(
        calculate_restock_needs(inventory_data, reference_date, shortage_reasons)
    )


def _record_shortage_reasons(unavailable_ingredients, shortage_reasons, inventory_names):
    """Merge failed availability reasons into the final restock inputs."""
    for detail in unavailable_ingredients:
        ingredient_name = detail["ingredient"]
        reasons = shortage_reasons.setdefault(ingredient_name, [])
        if ingredient_name not in inventory_names:
            _append_unique(reasons, "Missing from inventory")
        elif not detail["quantity_sufficient"]:
            _append_unique(reasons, "Insufficient for order")


def _consumption_records(requirements):
    """Convert requirement records into actual-consumption records."""
    return [
        {"name": item["name"], "qty_grams": item["required_qty_grams"]}
        for item in requirements
    ]


def _format_unavailable_ingredients(unavailable_ingredients):
    """Return deterministic ingredient failure text."""
    return ", ".join(
        f"{detail['ingredient']} ({detail['reason']})"
        for detail in unavailable_ingredients
    )


# @spec CKS-RECIPE-003, CKS-FULFILL-001, CKS-FULFILL-002, CKS-FULFILL-003, CKS-FULFILL-004, CKS-RESTOCK-004, CKS-PARTIAL-001, CKS-PARTIAL-002, CKS-PARTIAL-003
def process_orders(
    recipe_data,
    inventory_data,
    order_data,
    status_data,
    restock_data,
    reference_date=None,
    fulfillment_policy=ATOMIC_FULFILLMENT,
):
    """Process orders against cumulative inventory under an explicit policy."""
    reference_date = _resolve_reference_date(reference_date)
    if fulfillment_policy not in (ATOMIC_FULFILLMENT, PARTIAL_FULFILLMENT):
        raise ValueError("fulfillment_policy must be 'atomic' or 'partial'")

    processed_orders = []
    working_inventory = deepcopy(inventory_data)
    shortage_reasons = {}
    inventory_names = {item["ingredient"] for item in working_inventory}

    for order in order_data:
        order_result = {
            "order_id": order["order_id"],
            "brand": order["brand"],
            "items": [],
            "order_requirements": [],
            "inventory_check": None,
            "fulfilled": False,
            "fulfillment_status": "Not Delivered",
            "reason": "",
            "actual_consumption": [],
        }

        if fulfillment_policy == PARTIAL_FULFILLMENT:
            requirement_groups = []
            inventory_details = []
            consumption_groups = []

            if not order["items"]:
                order_result["inventory_check"] = {"all_available": False, "details": []}
                order_result["reason"] = "Invalid order: order has no items"
                update_status_entry(
                    status_data, order["order_id"], False, order_result["reason"]
                )
                processed_orders.append(order_result)
                continue

            for item in order["items"]:
                recipe = find_recipe_by_name(recipe_data, item["item"])
                quantity = item.get("qty")
                valid_quantity = type(quantity) is int and quantity > 0
                item_result = {
                    "item": item["item"],
                    "qty": quantity,
                    "recipe_found": recipe is not None,
                    "valid_quantity": valid_quantity,
                    "requirements": [],
                    "inventory_check": None,
                    "delivered": False,
                    "reason": "",
                }

                issues = []
                if not valid_quantity:
                    issues.append(f"Invalid quantity {quantity!r}")
                if recipe is None:
                    issues.append("No matching recipe")
                if issues:
                    item_result["reason"] = "; ".join(issues)
                    order_result["items"].append(item_result)
                    continue

                requirements = calculate_ingredient_requirements(recipe, quantity)
                requirement_groups.append(requirements)
                item_result["requirements"] = requirements
                inventory_check = check_inventory_availability(
                    working_inventory, requirements, reference_date
                )
                item_result["inventory_check"] = inventory_check
                inventory_details.extend(inventory_check["details"])
                unavailable = [
                    detail
                    for detail in inventory_check["details"]
                    if not detail["is_available"]
                ]

                if unavailable:
                    item_result["reason"] = _format_unavailable_ingredients(unavailable)
                    _record_shortage_reasons(
                        unavailable, shortage_reasons, inventory_names
                    )
                else:
                    deduct_inventory(working_inventory, requirements)
                    item_result["delivered"] = True
                    item_result["reason"] = "Delivered"
                    consumption_groups.append(requirements)

                order_result["items"].append(item_result)

            order_result["order_requirements"] = combine_requirements(requirement_groups)
            order_result["inventory_check"] = {
                "all_available": all(item["delivered"] for item in order_result["items"]),
                "details": inventory_details,
            }
            actual_requirements = combine_requirements(consumption_groups)
            order_result["actual_consumption"] = _consumption_records(actual_requirements)

            delivered_items = [
                item for item in order_result["items"] if item["delivered"]
            ]
            rejected_items = [
                item for item in order_result["items"] if not item["delivered"]
            ]
            if delivered_items and not rejected_items:
                order_result["fulfilled"] = True
                order_result["fulfillment_status"] = "Delivered"
                order_result["reason"] = "Delivered"
            elif delivered_items:
                delivered_text = ", ".join(item["item"] for item in delivered_items)
                rejected_text = ", ".join(
                    f"{item['item']} ({item['reason']})" for item in rejected_items
                )
                order_result["fulfillment_status"] = "Partially Delivered"
                order_result["reason"] = (
                    f"Partially Delivered: {delivered_text} | "
                    f"Not Delivered: {rejected_text}"
                )
            else:
                rejected_text = ", ".join(
                    f"{item['item']} ({item['reason']})" for item in rejected_items
                )
                order_result["reason"] = f"Not Delivered: {rejected_text}"

            update_status_entry(
                status_data,
                order["order_id"],
                order_result["fulfilled"],
                order_result["reason"],
            )
            processed_orders.append(order_result)
            continue

        requirement_groups = []
        missing_recipe_items = []
        invalid_order_issues = []

        if not order["items"]:
            invalid_order_issues.append("order has no items")

        for item in order["items"]:
            recipe = find_recipe_by_name(recipe_data, item["item"])
            quantity = item.get("qty")
            valid_quantity = type(quantity) is int and quantity > 0

            if not valid_quantity:
                invalid_order_issues.append(
                    f"{item['item']} has invalid quantity {quantity!r}"
                )

            if recipe is None:
                missing_recipe_items.append(item["item"])

            if recipe is None or not valid_quantity:
                order_result["items"].append(
                    {
                        "item": item["item"],
                        "qty": quantity,
                        "recipe_found": recipe is not None,
                        "valid_quantity": valid_quantity,
                        "requirements": [],
                        "inventory_check": None,
                        "delivered": False,
                        "reason": (
                            "No matching recipe"
                            if recipe is None
                            else f"Invalid quantity {quantity!r}"
                        ),
                    }
                )
                continue

            requirements = calculate_ingredient_requirements(recipe, quantity)
            requirement_groups.append(requirements)
            order_result["items"].append(
                {
                    "item": item["item"],
                    "qty": quantity,
                    "recipe_found": True,
                    "valid_quantity": True,
                    "requirements": requirements,
                    "inventory_check": None,
                    "delivered": False,
                    "reason": "",
                }
            )

        order_requirements = combine_requirements(requirement_groups)
        order_result["order_requirements"] = order_requirements

        inventory_check = check_inventory_availability(
            working_inventory,
            order_requirements,
            reference_date,
        )
        order_result["inventory_check"] = inventory_check
        unavailable_ingredients = [
            detail for detail in inventory_check["details"] if not detail["is_available"]
        ]

        reason_parts = []
        if invalid_order_issues:
            reason_parts.append("Invalid order: " + ", ".join(invalid_order_issues))
        if missing_recipe_items:
            reason_parts.append(
                "No matching recipe for item(s): " + ", ".join(missing_recipe_items)
            )
        if unavailable_ingredients:
            reason_parts.append(
                "Unavailable ingredients: "
                + ", ".join(
                    f"{detail['ingredient']} ({detail['reason']})"
                    for detail in unavailable_ingredients
                )
            )

            _record_shortage_reasons(
                unavailable_ingredients, shortage_reasons, inventory_names
            )

        if reason_parts:
            order_result["fulfilled"] = False
            order_result["reason"] = " | ".join(reason_parts)
            for item in order_result["items"]:
                if not item["reason"]:
                    item["reason"] = "Order rejected by atomic fulfillment policy"
            update_status_entry(status_data, order["order_id"], False, order_result["reason"])
        else:
            deduct_inventory(working_inventory, order_requirements)
            order_result["fulfilled"] = True
            order_result["fulfillment_status"] = "Delivered"
            order_result["reason"] = "Delivered"
            order_result["actual_consumption"] = _consumption_records(order_requirements)
            for item in order_result["items"]:
                item["delivered"] = True
                item["reason"] = "Delivered"
            update_status_entry(status_data, order["order_id"], True, "Delivered")

        processed_orders.append(order_result)

    apply_final_inventory_snapshot(inventory_data, working_inventory)
    refresh_restock_table(
        restock_data,
        inventory_data,
        reference_date,
        shortage_reasons,
    )

    return processed_orders


# @spec CKS-FORECAST-001, CKS-FORECAST-002, CKS-FORECAST-003
def predict_stockouts(inventory_data, processed_orders, horizon_orders=DEFAULT_FORECAST_HORIZON_ORDERS):
    """Estimate stockouts from actual fulfilled consumption per observed order."""
    if type(horizon_orders) is not int or horizon_orders <= 0:
        raise ValueError("horizon_orders must be a positive integer")

    observed_orders = len(processed_orders)
    if observed_orders == 0:
        return []

    consumption = {}
    for order in processed_orders:
        for item in order.get("actual_consumption", []):
            consumption.setdefault(item["name"], 0)
            consumption[item["name"]] += item["qty_grams"]

    alerts = []
    for inventory_item in inventory_data:
        ingredient = inventory_item["ingredient"]
        observed = consumption.get(ingredient, 0)
        if observed <= 0:
            continue
        average = observed / observed_orders
        current_qty = inventory_item["qty_grams"]
        estimated_orders_remaining = current_qty / average
        if estimated_orders_remaining > horizon_orders:
            continue
        alerts.append(
            {
                "ingredient": ingredient,
                "current_qty_grams": current_qty,
                "observed_consumption_grams": observed,
                "average_consumption_per_order": round(average, 2),
                "forecast_horizon_orders": horizon_orders,
                "projected_qty_grams": round(current_qty - average * horizon_orders, 2),
                "estimated_orders_remaining": round(estimated_orders_remaining, 2),
            }
        )
    return alerts


# @spec CKS-MENU-001, CKS-MENU-002
def identify_unavailable_menu_items(recipe_data, inventory_data, reference_date=None):
    """Return menu items that cannot produce one serving from usable stock."""
    reference_date = _resolve_reference_date(reference_date)
    inventory_lookup = {item["ingredient"]: item for item in inventory_data}
    unavailable_items = []

    for recipe in recipe_data:
        blocking_ingredients = []
        for requirement in recipe["ingredients"]:
            ingredient = requirement["name"]
            required_qty = requirement["qty_grams"]
            inventory_item = inventory_lookup.get(ingredient)
            if inventory_item is None:
                reason = "Missing from inventory"
            else:
                current_qty = inventory_item["qty_grams"]
                expiry_status, _, is_usable = _expiry_context(
                    inventory_item, reference_date
                )
                if not is_usable:
                    reason = expiry_status
                elif current_qty <= 0:
                    reason = "Out of stock"
                elif current_qty < required_qty:
                    reason = "Insufficient for one serving"
                else:
                    continue
            blocking_ingredients.append(
                {"ingredient": ingredient, "reason": reason}
            )

        if blocking_ingredients:
            unavailable_items.append(
                {
                    "item": recipe["name"],
                    "blocking_ingredients": blocking_ingredients,
                }
            )

    return unavailable_items


def print_order_processing_results(processed_orders):
    """Print recipe lookup, ingredient demand, inventory checks, and fulfillment."""
    print("\n=== Order Processing ===")
    for order in processed_orders:
        print(f"Order ID: {order['order_id']}")
        print(f"Brand: {order['brand']}")

        for item in order["items"]:
            print(f"Item: {item['item']}")
            print(f"Quantity Ordered: {item['qty']}")
            print(f"Recipe Found: {item['recipe_found']}")

            if not item["recipe_found"]:
                print("Inventory Check: Skipped because the recipe was not found.")
                print()
                continue

            print("Required Ingredients:")
            for requirement in item["requirements"]:
                print(
                    f"  - {requirement['name']}: "
                    f"{requirement['required_qty_grams']} grams required"
                )

            print()

        print("Combined Order Requirements:")
        for requirement in order["order_requirements"]:
            print(f"  - {requirement['name']}: {requirement['required_qty_grams']} grams required")

        print(f"All Ingredients Available: {order['inventory_check']['all_available']}")
        print("Inventory Details:")
        for detail in order["inventory_check"]["details"]:
            print(
                f"  - {detail['ingredient']}: "
                f"required={detail['required_qty_grams']} grams, "
                f"available={detail['available_qty_grams']} grams, "
                f"enough={detail['is_available']}"
            )

        print(f"Fulfilled: {order['fulfilled']}")
        print(f"Reason: {order['reason']}")
        print()


# @spec CKS-REPORT-001, CKS-REPORT-003
def build_business_summary(
    processed_orders,
    inventory_data,
    restock_data,
    reference_date=None,
    stockout_alerts=None,
    unavailable_menu_items=None,
    forecast_horizon_orders=None,
):
    """Return the final simulation outcome in a testable business structure."""
    reference_date = _resolve_reference_date(reference_date)
    delivered_orders = [
        order
        for order in processed_orders
        if order.get("fulfillment_status", "Delivered" if order["fulfilled"] else "Not Delivered")
        == "Delivered"
    ]
    partially_delivered_orders = [
        order
        for order in processed_orders
        if order.get("fulfillment_status") == "Partially Delivered"
    ]
    not_delivered_orders = [
        order
        for order in processed_orders
        if order.get("fulfillment_status", "Delivered" if order["fulfilled"] else "Not Delivered")
        == "Not Delivered"
    ]
    expiry_concerns = []

    for item in inventory_data:
        expiry_status, days_until_expiry, _ = _expiry_context(item, reference_date)
        if expiry_status in ("Expired", "Expiring soon", "Invalid expiry"):
            expiry_concerns.append(
                {
                    "ingredient": item["ingredient"],
                    "expiry_date": item.get("expiry_date"),
                    "days_until_expiry": days_until_expiry,
                    "status": expiry_status,
                }
            )

    return {
        "delivered_count": len(delivered_orders),
        "partially_delivered_count": len(partially_delivered_orders),
        "not_delivered_count": len(not_delivered_orders),
        "delivered_order_ids": [order["order_id"] for order in delivered_orders],
        "partially_delivered_orders": [
            {
                "order_id": order["order_id"],
                "reason": order["reason"],
                "items": deepcopy(order.get("items", [])),
            }
            for order in partially_delivered_orders
        ],
        "not_delivered_orders": [
            {"order_id": order["order_id"], "reason": order["reason"]}
            for order in not_delivered_orders
        ],
        "final_inventory": deepcopy(inventory_data),
        "restock_recommendations": deepcopy(restock_data),
        "expiry_concerns": expiry_concerns,
        "stockout_alerts": deepcopy(stockout_alerts or []),
        "unavailable_menu_items": deepcopy(unavailable_menu_items or []),
        "forecast_horizon_orders": forecast_horizon_orders,
    }


# @spec CKS-REPORT-002, CKS-REPORT-004
def print_business_summary(summary):
    """Print the final simulation result for a non-technical kitchen manager."""
    print("\n=== Business Summary ===")
    print(f"Orders Delivered: {summary['delivered_count']}")
    print(f"Orders Partially Delivered: {summary.get('partially_delivered_count', 0)}")
    print(f"Orders Not Delivered: {summary['not_delivered_count']}")

    print("\nDelivered Order IDs:")
    if summary["delivered_order_ids"]:
        print("  " + ", ".join(str(order_id) for order_id in summary["delivered_order_ids"]))
    else:
        print("  None")

    print("\nOrders Partially Delivered:")
    if summary.get("partially_delivered_orders"):
        for order in summary["partially_delivered_orders"]:
            print(f"  Order {order['order_id']}: {order['reason']}")
    else:
        print("  None")

    print("\nOrders Not Delivered:")
    if summary["not_delivered_orders"]:
        for order in summary["not_delivered_orders"]:
            print(f"  Order {order['order_id']}: {order['reason']}")
    else:
        print("  None")

    print("\nFinal Inventory:")
    for item in summary["final_inventory"]:
        print(f"  {item['ingredient']}: {item['qty_grams']} grams")

    print("\nRestock Recommendations:")
    if summary["restock_recommendations"]:
        for item in summary["restock_recommendations"]:
            print(
                f"  {item['item']}: order {item['qty_needed_grams']} grams "
                f"({item['reason']})"
            )
    else:
        print("  None")

    print("\nExpiry Concerns:")
    if summary["expiry_concerns"]:
        for item in summary["expiry_concerns"]:
            print(
                f"  {item['ingredient']}: {item['status']} "
                f"(expiry: {item['expiry_date']})"
            )
    else:
        print("  None")

    print("\nPredictive Stockout Alerts:")
    if summary.get("stockout_alerts"):
        for item in summary["stockout_alerts"]:
            print(
                f"  {item['ingredient']}: approximately "
                f"{item['estimated_orders_remaining']} orders remaining "
                f"at {item['average_consumption_per_order']} grams per order"
            )
    else:
        print("  None")

    print("\nUnavailable Menu Items:")
    if summary.get("unavailable_menu_items"):
        for menu_item in summary["unavailable_menu_items"]:
            blockers = ", ".join(
                f"{item['ingredient']} ({item['reason']})"
                for item in menu_item["blocking_ingredients"]
            )
            print(f"  {menu_item['item']}: {blockers}")
    else:
        print("  None")


def _markdown_table(headers, rows):
    """Render a compact Markdown table, including an empty-state row."""
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if rows:
        lines.extend("| " + " | ".join(cell(value) for value in row) + " |" for row in rows)
    else:
        lines.append("| " + " | ".join(["None"] + [""] * (len(headers) - 1)) + " |")
    return lines


# @spec CKS-REPORT-005
def generate_markdown_report(summary, output_path, reference_date=None):
    """Replace a Markdown file with a polished report from structured results."""
    reference_date = _resolve_reference_date(reference_date)
    output_path = Path(output_path)
    lines = [
        "# Cloud Kitchen Business Report",
        "",
        f"**Simulation date:** {reference_date.isoformat()}",
        "",
        "## Executive Summary",
        "",
        f"- Orders delivered: {summary['delivered_count']}",
        f"- Orders partially delivered: {summary.get('partially_delivered_count', 0)}",
        f"- Orders not delivered: {summary['not_delivered_count']}",
        f"- Predictive stockout alerts: {len(summary.get('stockout_alerts', []))}",
        f"- Unavailable menu items: {len(summary.get('unavailable_menu_items', []))}",
        "",
        "## Order Outcomes",
        "",
    ]

    order_rows = [
        (order_id, "Delivered", "Delivered")
        for order_id in summary["delivered_order_ids"]
    ]
    order_rows.extend(
        (order["order_id"], "Partially Delivered", order["reason"])
        for order in summary.get("partially_delivered_orders", [])
    )
    order_rows.extend(
        (order["order_id"], "Not Delivered", order["reason"])
        for order in summary["not_delivered_orders"]
    )
    lines.extend(_markdown_table(["Order", "Status", "Details"], order_rows))

    lines.extend(["", "## Predictive Stockout Alerts", ""])
    alert_rows = [
        (
            item["ingredient"],
            item["current_qty_grams"],
            item["average_consumption_per_order"],
            item["forecast_horizon_orders"],
            item["projected_qty_grams"],
            item["estimated_orders_remaining"],
        )
        for item in summary.get("stockout_alerts", [])
    ]
    lines.extend(
        _markdown_table(
            ["Ingredient", "Current g", "Avg g/order", "Horizon", "Projected g", "Orders remaining"],
            alert_rows,
        )
    )

    lines.extend(["", "## Unavailable Menu Items", ""])
    menu_rows = [
        (
            item["item"],
            "; ".join(
                f"{blocker['ingredient']}: {blocker['reason']}"
                for blocker in item["blocking_ingredients"]
            ),
        )
        for item in summary.get("unavailable_menu_items", [])
    ]
    lines.extend(_markdown_table(["Menu item", "Blocking ingredients"], menu_rows))

    lines.extend(["", "## Final Inventory", ""])
    lines.extend(
        _markdown_table(
            ["Ingredient", "Quantity g", "Expiry date"],
            [
                (item["ingredient"], item["qty_grams"], item.get("expiry_date", ""))
                for item in summary["final_inventory"]
            ],
        )
    )

    lines.extend(["", "## Restock Recommendations", ""])
    lines.extend(
        _markdown_table(
            ["Ingredient", "Current g", "Order g", "Reason"],
            [
                (
                    item["item"],
                    item.get("current_qty_grams", ""),
                    item["qty_needed_grams"],
                    item["reason"],
                )
                for item in summary["restock_recommendations"]
            ],
        )
    )

    lines.extend(["", "## Expiry Concerns", ""])
    lines.extend(
        _markdown_table(
            ["Ingredient", "Status", "Expiry date", "Days"],
            [
                (
                    item["ingredient"],
                    item["status"],
                    item.get("expiry_date", ""),
                    item.get("days_until_expiry", ""),
                )
                for item in summary["expiry_concerns"]
            ],
        )
    )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def _html_table(headers, rows):
    """Render an escaped HTML table with an explicit empty state."""
    header_html = "".join(f"<th>{escape(str(header))}</th>" for header in headers)
    if rows:
        body_html = "".join(
            "<tr>"
            + "".join(f"<td>{escape(str(value))}</td>" for value in row)
            + "</tr>"
            for row in rows
        )
    else:
        body_html = (
            f'<tr><td colspan="{len(headers)}" class="empty">None</td></tr>'
        )
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + header_html
        + "</tr></thead><tbody>"
        + body_html
        + "</tbody></table></div>"
    )


# @spec CKS-REPORT-006
def generate_html_report(summary, output_path, reference_date=None):
    """Replace an HTML file with a self-contained report from structured results."""
    reference_date = _resolve_reference_date(reference_date)
    output_path = Path(output_path)
    order_rows = [
        (order_id, "Delivered", "Delivered")
        for order_id in summary["delivered_order_ids"]
    ]
    order_rows.extend(
        (order["order_id"], "Partially Delivered", order["reason"])
        for order in summary.get("partially_delivered_orders", [])
    )
    order_rows.extend(
        (order["order_id"], "Not Delivered", order["reason"])
        for order in summary["not_delivered_orders"]
    )
    alert_rows = [
        (
            item["ingredient"],
            item["current_qty_grams"],
            item["average_consumption_per_order"],
            item["forecast_horizon_orders"],
            item["projected_qty_grams"],
            item["estimated_orders_remaining"],
        )
        for item in summary.get("stockout_alerts", [])
    ]
    menu_rows = [
        (
            item["item"],
            "; ".join(
                f"{blocker['ingredient']}: {blocker['reason']}"
                for blocker in item["blocking_ingredients"]
            ),
        )
        for item in summary.get("unavailable_menu_items", [])
    ]
    inventory_rows = [
        (item["ingredient"], item["qty_grams"], item.get("expiry_date", ""))
        for item in summary["final_inventory"]
    ]
    restock_rows = [
        (
            item["item"],
            item.get("current_qty_grams", ""),
            item["qty_needed_grams"],
            item["reason"],
        )
        for item in summary["restock_recommendations"]
    ]
    expiry_rows = [
        (
            item["ingredient"],
            item["status"],
            item.get("expiry_date", ""),
            item.get("days_until_expiry", ""),
        )
        for item in summary["expiry_concerns"]
    ]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cloud Kitchen Business Report</title>
  <style>
    :root {{ color-scheme: light; --ink: #172033; --muted: #5c667a; --line: #d9deea; --panel: #f6f8fc; --accent: #1f5fbf; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #eef2f8; color: var(--ink); font: 15px/1.5 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    main {{ width: min(1120px, calc(100% - 32px)); margin: 32px auto; background: white; border: 1px solid var(--line); border-radius: 14px; padding: 32px; box-shadow: 0 16px 40px rgba(23, 32, 51, .08); }}
    h1 {{ margin: 0 0 4px; font-size: clamp(26px, 4vw, 40px); }}
    h2 {{ margin: 32px 0 12px; border-bottom: 2px solid var(--accent); padding-bottom: 7px; font-size: 20px; }}
    .date {{ color: var(--muted); }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-top: 20px; }}
    .metric {{ background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 14px; }}
    .metric strong {{ display: block; font-size: 24px; }}
    .metric span {{ color: var(--muted); }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 620px; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: var(--panel); font-size: 13px; text-transform: uppercase; letter-spacing: .04em; }}
    tbody tr:last-child td {{ border-bottom: 0; }}
    .empty {{ color: var(--muted); text-align: center; }}
  </style>
</head>
<body>
<main>
  <h1>Cloud Kitchen Business Report</h1>
  <p class="date">Simulation date: {escape(reference_date.isoformat())}</p>
  <h2>Executive Summary</h2>
  <div class="metrics">
    <div class="metric"><strong>{summary['delivered_count']}</strong><span>Delivered</span></div>
    <div class="metric"><strong>{summary.get('partially_delivered_count', 0)}</strong><span>Partially delivered</span></div>
    <div class="metric"><strong>{summary['not_delivered_count']}</strong><span>Not delivered</span></div>
    <div class="metric"><strong>{len(summary.get('stockout_alerts', []))}</strong><span>Stockout alerts</span></div>
    <div class="metric"><strong>{len(summary.get('unavailable_menu_items', []))}</strong><span>Unavailable menu items</span></div>
  </div>
  <h2>Order Outcomes</h2>
  {_html_table(['Order', 'Status', 'Details'], order_rows)}
  <h2>Predictive Stockout Alerts</h2>
  {_html_table(['Ingredient', 'Current g', 'Avg g/order', 'Horizon', 'Projected g', 'Orders remaining'], alert_rows)}
  <h2>Unavailable Menu Items</h2>
  {_html_table(['Menu item', 'Blocking ingredients'], menu_rows)}
  <h2>Final Inventory</h2>
  {_html_table(['Ingredient', 'Quantity g', 'Expiry date'], inventory_rows)}
  <h2>Restock Recommendations</h2>
  {_html_table(['Ingredient', 'Current g', 'Order g', 'Reason'], restock_rows)}
  <h2>Expiry Concerns</h2>
  {_html_table(['Ingredient', 'Status', 'Expiry date', 'Days'], expiry_rows)}
</main>
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main():
    """Load seed tables, process fulfillment, and print the updated results."""
    recipe_data = load_recipes()
    inventory_data = deepcopy(load_inventory())
    order_data = load_orders()
    restock_data = []
    status_data = deepcopy(load_status())
    simulation_date = date.today()
    processed_orders = process_orders(
        recipe_data,
        inventory_data,
        order_data,
        status_data,
        restock_data,
        simulation_date,
        fulfillment_policy=PARTIAL_FULFILLMENT,
    )
    stockout_alerts = predict_stockouts(
        inventory_data,
        processed_orders,
        DEFAULT_FORECAST_HORIZON_ORDERS,
    )
    unavailable_menu_items = identify_unavailable_menu_items(
        recipe_data,
        inventory_data,
        simulation_date,
    )
    summary = build_business_summary(
        processed_orders,
        inventory_data,
        restock_data,
        simulation_date,
        stockout_alerts=stockout_alerts,
        unavailable_menu_items=unavailable_menu_items,
        forecast_horizon_orders=DEFAULT_FORECAST_HORIZON_ORDERS,
    )

    print_recipes(recipe_data)
    print_orders(order_data)
    print_order_processing_results(processed_orders)
    print_inventory(inventory_data)
    print_restock(restock_data)
    print_status(status_data)
    print_business_summary(summary)
    report_path = generate_markdown_report(
        summary,
        Path(__file__).with_name("BUSINESS_REPORT.md"),
        simulation_date,
    )
    print(f"\nMarkdown report: {report_path}")
    html_report_path = generate_html_report(
        summary,
        Path(__file__).with_name("BUSINESS_REPORT.html"),
        simulation_date,
    )
    print(f"HTML report: {html_report_path}")


if __name__ == "__main__":
    main()
