"""Cloud kitchen order, inventory, restock, and reporting simulation."""

from copy import deepcopy
from datetime import date, datetime

from seed_data import inventory, orders, recipes, restock, status


LOW_STOCK_THRESHOLD_GRAMS = 1000
PAR_LEVEL_GRAMS = 10000
EXPIRING_SOON_DAYS = 5


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


# @spec CKS-RECIPE-003, CKS-FULFILL-001, CKS-FULFILL-002, CKS-FULFILL-003, CKS-FULFILL-004, CKS-RESTOCK-004
def process_orders(
    recipe_data,
    inventory_data,
    order_data,
    status_data,
    restock_data,
    reference_date=None,
):
    """Process complete orders atomically against cumulative usable inventory."""
    reference_date = _resolve_reference_date(reference_date)
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
            "reason": "",
        }
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

            for detail in unavailable_ingredients:
                ingredient_name = detail["ingredient"]
                reasons = shortage_reasons.setdefault(ingredient_name, [])
                if ingredient_name not in inventory_names:
                    _append_unique(reasons, "Missing from inventory")
                elif not detail["quantity_sufficient"]:
                    _append_unique(reasons, "Insufficient for order")

        if reason_parts:
            order_result["fulfilled"] = False
            order_result["reason"] = " | ".join(reason_parts)
            update_status_entry(status_data, order["order_id"], False, order_result["reason"])
        else:
            deduct_inventory(working_inventory, order_requirements)
            order_result["fulfilled"] = True
            order_result["reason"] = "Delivered"
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


# @spec CKS-REPORT-001
def build_business_summary(
    processed_orders,
    inventory_data,
    restock_data,
    reference_date=None,
):
    """Return the final simulation outcome in a testable business structure."""
    reference_date = _resolve_reference_date(reference_date)
    delivered_orders = [order for order in processed_orders if order["fulfilled"]]
    not_delivered_orders = [order for order in processed_orders if not order["fulfilled"]]
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
        "not_delivered_count": len(not_delivered_orders),
        "delivered_order_ids": [order["order_id"] for order in delivered_orders],
        "not_delivered_orders": [
            {"order_id": order["order_id"], "reason": order["reason"]}
            for order in not_delivered_orders
        ],
        "final_inventory": deepcopy(inventory_data),
        "restock_recommendations": deepcopy(restock_data),
        "expiry_concerns": expiry_concerns,
    }


# @spec CKS-REPORT-002
def print_business_summary(summary):
    """Print the final simulation result for a non-technical kitchen manager."""
    print("\n=== Business Summary ===")
    print(f"Orders Delivered: {summary['delivered_count']}")
    print(f"Orders Not Delivered: {summary['not_delivered_count']}")

    print("\nDelivered Order IDs:")
    if summary["delivered_order_ids"]:
        print("  " + ", ".join(str(order_id) for order_id in summary["delivered_order_ids"]))
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
    )
    summary = build_business_summary(
        processed_orders,
        inventory_data,
        restock_data,
        simulation_date,
    )

    print_recipes(recipe_data)
    print_orders(order_data)
    print_order_processing_results(processed_orders)
    print_inventory(inventory_data)
    print_restock(restock_data)
    print_status(status_data)
    print_business_summary(summary)


if __name__ == "__main__":
    main()
