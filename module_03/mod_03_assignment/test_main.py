"""Unit tests for the cloud kitchen inventory simulation."""

from copy import deepcopy
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
import unittest

from main import (
    build_business_summary,
    calculate_ingredient_requirements,
    calculate_restock_needs,
    check_inventory_availability,
    combine_requirements,
    find_recipe_by_name,
    load_inventory,
    load_orders,
    load_recipes,
    load_restock,
    load_status,
    print_business_summary,
    print_inventory,
    print_orders,
    print_recipes,
    print_restock,
    print_status,
    process_orders,
)


REFERENCE_DATE = date(2026, 6, 3)


class TestLoadAndDisplayFunctions(unittest.TestCase):
    """Verify the supplied tables are accessible and displayable."""

    # @spec CKS-DATA-001
    def test_loads_all_five_tables_successfully(self):
        loaders = (load_recipes, load_inventory, load_orders, load_restock, load_status)
        for loader in loaders:
            loaded = loader()
            self.assertIsInstance(loaded, list)
            self.assertGreater(len(loaded), 0)

    # @spec CKS-DATA-001
    def test_record_counts_match_seed_data(self):
        self.assertEqual(len(load_recipes()), 5)
        self.assertEqual(len(load_inventory()), 14)
        self.assertEqual(len(load_orders()), 5)
        self.assertEqual(len(load_restock()), 5)
        self.assertEqual(len(load_status()), 5)

    # @spec CKS-DATA-001
    def test_core_record_field_types_match_supplied_schema(self):
        recipe = load_recipes()[0]
        inventory_item = load_inventory()[0]
        order = load_orders()[0]
        restock_item = load_restock()[0]
        status_item = load_status()[0]
        self.assertIsInstance(recipe["recipe_id"], int)
        self.assertIsInstance(recipe["ingredients"], list)
        self.assertIsInstance(inventory_item["qty_grams"], (int, float))
        self.assertIsInstance(inventory_item["expiry_date"], str)
        self.assertIsInstance(order["items"], list)
        self.assertIsInstance(restock_item["reason"], str)
        self.assertIsInstance(status_item["delivered"], bool)

    # @spec CKS-DATA-002
    def test_display_functions_show_each_table(self):
        output = StringIO()
        with redirect_stdout(output):
            print_recipes(load_recipes())
            print_inventory(load_inventory())
            print_orders(load_orders())
            print_restock(load_restock())
            print_status(load_status())
        displayed = output.getvalue()
        for heading in ("Recipes", "Inventory", "Orders", "Restock", "Status"):
            self.assertIn(heading, displayed)
        for recipe in load_recipes():
            self.assertIn(recipe["name"], displayed)
        for item in load_inventory():
            self.assertIn(item["ingredient"], displayed)
        for order in load_orders():
            self.assertIn(f"Order ID: {order['order_id']}", displayed)
        for item in load_restock():
            self.assertIn(item["item"], displayed)
        for entry in load_status():
            self.assertIn(f"Remark: {entry['remark']}", displayed)


class TestRecipeDemand(unittest.TestCase):
    """Verify recipe lookup and complete-order demand calculation."""

    # @spec CKS-RECIPE-001
    def test_recipe_lookup_handles_known_and_unknown_items(self):
        recipe = find_recipe_by_name(load_recipes(), "Chicken Burger")
        self.assertEqual(recipe["recipe_id"], 2)
        self.assertIsNone(find_recipe_by_name(load_recipes(), "Paneer Wrap"))

    # @spec CKS-RECIPE-002
    def test_quantity_scaling_and_combining_repeated_ingredients(self):
        pizza = find_recipe_by_name(load_recipes(), "Margherita Pizza")
        cake = find_recipe_by_name(load_recipes(), "Chocolate Cake")
        combined = combine_requirements(
            [
                calculate_ingredient_requirements(pizza, 2),
                calculate_ingredient_requirements(cake, 1),
            ]
        )
        self.assertEqual(
            combined,
            [
                {"name": "Flour", "required_qty_grams": 850},
                {"name": "Tomato Sauce", "required_qty_grams": 200},
                {"name": "Mozzarella Cheese", "required_qty_grams": 300},
                {"name": "Chocolate", "required_qty_grams": 150},
                {"name": "Sugar", "required_qty_grams": 100},
            ],
        )

    # @spec CKS-RECIPE-003
    def test_empty_order_and_invalid_quantities_fail_without_deduction(self):
        cases = [
            {"order_id": 10, "brand": "Test", "items": []},
            {"order_id": 11, "brand": "Test", "items": [{"item": "Chicken Burger", "qty": 0}]},
            {"order_id": 12, "brand": "Test", "items": [{"item": "Chicken Burger", "qty": 1.5}]},
        ]
        for order in cases:
            with self.subTest(order_id=order["order_id"]):
                inventory_data = deepcopy(load_inventory())
                original_inventory = deepcopy(inventory_data)
                status_data = []
                processed = process_orders(
                    deepcopy(load_recipes()), inventory_data, [order], status_data, [], REFERENCE_DATE
                )
                self.assertFalse(processed[0]["fulfilled"])
                self.assertIn("Invalid order", processed[0]["reason"])
                self.assertEqual(inventory_data, original_inventory)
                self.assertFalse(status_data[0]["delivered"])


class TestInventoryAvailability(unittest.TestCase):
    """Verify quantity and expiry decisions are reported clearly."""

    # @spec CKS-INVENTORY-001
    def test_availability_detail_contains_required_decision_fields(self):
        result = check_inventory_availability(
            [{"ingredient": "Flour", "qty_grams": 500, "expiry_date": "2026-12-31"}],
            [{"name": "Flour", "required_qty_grams": 400}],
            REFERENCE_DATE,
        )
        self.assertTrue(result["all_available"])
        self.assertEqual(
            set(result["details"][0]),
            {
                "ingredient", "required_qty_grams", "available_qty_grams",
                "quantity_sufficient", "expiry_status", "is_usable",
                "is_available", "reason",
            },
        )

    # @spec CKS-INVENTORY-002
    def test_missing_and_insufficient_ingredients_are_distinguished(self):
        result = check_inventory_availability(
            [{"ingredient": "Flour", "qty_grams": 200, "expiry_date": "2026-12-31"}],
            [
                {"name": "Flour", "required_qty_grams": 300},
                {"name": "Cheese", "required_qty_grams": 100},
            ],
            REFERENCE_DATE,
        )
        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["reason"], "Insufficient quantity")
        self.assertEqual(result["details"][1]["reason"], "Missing from inventory")

    # @spec CKS-INVENTORY-003
    def test_expired_ingredient_is_unusable(self):
        result = check_inventory_availability(
            [{"ingredient": "Cream", "qty_grams": 5000, "expiry_date": "2026-06-02"}],
            [{"name": "Cream", "required_qty_grams": 100}],
            REFERENCE_DATE,
        )
        detail = result["details"][0]
        self.assertFalse(result["all_available"])
        self.assertEqual(detail["expiry_status"], "Expired")
        self.assertFalse(detail["is_usable"])
        self.assertIn("Expired", detail["reason"])

    # @spec CKS-INVENTORY-004
    def test_expiring_today_and_in_five_days_remain_usable(self):
        for expiry in ("2026-06-03", "2026-06-08"):
            with self.subTest(expiry=expiry):
                result = check_inventory_availability(
                    [{"ingredient": "Cream", "qty_grams": 5000, "expiry_date": expiry}],
                    [{"name": "Cream", "required_qty_grams": 100}],
                    REFERENCE_DATE,
                )
                self.assertTrue(result["all_available"])
                self.assertEqual(result["details"][0]["expiry_status"], "Expiring soon")
                self.assertTrue(result["details"][0]["is_usable"])

    # @spec CKS-INVENTORY-005
    def test_invalid_expiry_fails_closed_but_missing_expiry_uses_quantity(self):
        invalid = check_inventory_availability(
            [{"ingredient": "Cream", "qty_grams": 5000, "expiry_date": "not-a-date"}],
            [{"name": "Cream", "required_qty_grams": 100}], REFERENCE_DATE,
        )
        missing = check_inventory_availability(
            [{"ingredient": "Cream", "qty_grams": 5000}],
            [{"name": "Cream", "required_qty_grams": 100}], REFERENCE_DATE,
        )
        self.assertFalse(invalid["all_available"])
        self.assertEqual(invalid["details"][0]["expiry_status"], "Invalid expiry")
        self.assertTrue(missing["all_available"])
        self.assertEqual(missing["details"][0]["expiry_status"], "Not provided")


class TestOrderFulfillment(unittest.TestCase):
    """Verify atomic fulfillment, status updates, and cumulative inventory."""

    # @spec CKS-FULFILL-001
    def test_successful_order_is_delivered_and_deducted_once(self):
        inventory_data = deepcopy(load_inventory())
        status_data = []
        processed = process_orders(
            deepcopy(load_recipes()), inventory_data,
            [{"order_id": 101, "brand": "Test", "items": [{"item": "Margherita Pizza", "qty": 2}]}],
            status_data, [], date(2026, 1, 1),
        )
        quantities = {item["ingredient"]: item["qty_grams"] for item in inventory_data}
        self.assertTrue(processed[0]["fulfilled"])
        self.assertEqual(quantities["Flour"], 9400)
        self.assertEqual(quantities["Tomato Sauce"], 9800)
        self.assertEqual(quantities["Mozzarella Cheese"], 9700)
        self.assertTrue(status_data[0]["delivered"])

    # @spec CKS-FULFILL-002
    def test_failed_complete_order_does_not_deduct_available_items(self):
        recipe_data = [{
            "recipe_id": 1, "name": "Test Wrap",
            "ingredients": [{"name": "Chicken", "qty_grams": 200}, {"name": "Bun", "qty_grams": 100}],
        }]
        inventory_data = [
            {"ingredient": "Chicken", "qty_grams": 500, "expiry_date": "2026-12-31"},
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"},
        ]
        original = deepcopy(inventory_data)
        status_data = []
        processed = process_orders(
            recipe_data, inventory_data,
            [{"order_id": 202, "brand": "Test", "items": [{"item": "Test Wrap", "qty": 1}]}],
            status_data, [], REFERENCE_DATE,
        )
        self.assertFalse(processed[0]["fulfilled"])
        self.assertIn("Bun", processed[0]["reason"])
        self.assertEqual(inventory_data, original)
        self.assertEqual(status_data[0]["remark"], processed[0]["reason"])

    # @spec CKS-FULFILL-002
    def test_expired_ingredient_fails_order_without_deduction(self):
        recipe_data = [{"recipe_id": 1, "name": "Soup", "ingredients": [{"name": "Cream", "qty_grams": 100}]}]
        inventory_data = [{"ingredient": "Cream", "qty_grams": 500, "expiry_date": "2026-06-02"}]
        original = deepcopy(inventory_data)
        processed = process_orders(
            recipe_data, inventory_data,
            [{"order_id": 203, "brand": "Test", "items": [{"item": "Soup", "qty": 1}]}],
            [], [], REFERENCE_DATE,
        )
        self.assertFalse(processed[0]["fulfilled"])
        self.assertIn("Cream (Expired)", processed[0]["reason"])
        self.assertEqual(inventory_data, original)

    # @spec CKS-FULFILL-002
    def test_missing_recipe_fails_complete_order_without_deduction(self):
        inventory_data = deepcopy(load_inventory())
        original = deepcopy(inventory_data)
        processed = process_orders(
            deepcopy(load_recipes()), inventory_data,
            [{"order_id": 204, "brand": "Test", "items": [{"item": "Unknown Dish", "qty": 1}]}],
            [], [], REFERENCE_DATE,
        )
        self.assertFalse(processed[0]["fulfilled"])
        self.assertIn("No matching recipe", processed[0]["reason"])
        self.assertEqual(inventory_data, original)

    # @spec CKS-FULFILL-003
    def test_later_order_uses_inventory_remaining_after_prior_order(self):
        recipe_data = [
            {"recipe_id": 1, "name": "First", "ingredients": [{"name": "Cheese", "qty_grams": 600}]},
            {"recipe_id": 2, "name": "Second", "ingredients": [{"name": "Cheese", "qty_grams": 500}]},
        ]
        inventory_data = [{"ingredient": "Cheese", "qty_grams": 1000, "expiry_date": "2026-12-31"}]
        orders = [
            {"order_id": 301, "brand": "Test", "items": [{"item": "First", "qty": 1}]},
            {"order_id": 302, "brand": "Test", "items": [{"item": "Second", "qty": 1}]},
        ]
        processed = process_orders(recipe_data, inventory_data, orders, [], [], REFERENCE_DATE)
        self.assertTrue(processed[0]["fulfilled"])
        self.assertFalse(processed[1]["fulfilled"])
        self.assertEqual(inventory_data[0]["qty_grams"], 400)

    # @spec CKS-FULFILL-004
    def test_status_updates_existing_record_and_appends_missing_record(self):
        recipe_data = [{"recipe_id": 1, "name": "Dish", "ingredients": [{"name": "Rice", "qty_grams": 100}]}]
        inventory_data = [{"ingredient": "Rice", "qty_grams": 500, "expiry_date": "2026-12-31"}]
        status_data = [{"order_id": 401, "delivered": False, "remark": "Pending"}]
        orders = [
            {"order_id": 401, "brand": "Test", "items": [{"item": "Dish", "qty": 1}]},
            {"order_id": 402, "brand": "Test", "items": [{"item": "Dish", "qty": 1}]},
        ]
        process_orders(recipe_data, inventory_data, orders, status_data, [], REFERENCE_DATE)
        self.assertEqual(len(status_data), 2)
        self.assertEqual(status_data[0], {"order_id": 401, "delivered": True, "remark": "Delivered"})
        self.assertEqual(status_data[1], {"order_id": 402, "delivered": True, "remark": "Delivered"})


class TestRestockRules(unittest.TestCase):
    """Verify stock, expiry, and consolidation rules."""

    # @spec CKS-RESTOCK-001
    def test_zero_low_threshold_and_above_threshold_boundaries(self):
        inventory_data = [
            {"ingredient": "Zero", "qty_grams": 0, "expiry_date": "2026-12-31"},
            {"ingredient": "Threshold", "qty_grams": 1000, "expiry_date": "2026-12-31"},
            {"ingredient": "Above", "qty_grams": 1001, "expiry_date": "2026-12-31"},
        ]
        by_item = {item["item"]: item for item in calculate_restock_needs(inventory_data, REFERENCE_DATE)}
        self.assertEqual(by_item["Zero"]["qty_needed_grams"], 10000)
        self.assertEqual(by_item["Threshold"]["qty_needed_grams"], 9000)
        self.assertNotIn("Above", by_item)

    # @spec CKS-RESTOCK-002
    def test_expired_and_expiring_soon_have_correct_restock_quantities(self):
        inventory_data = [
            {"ingredient": "Expired", "qty_grams": 7000, "expiry_date": "2026-06-02"},
            {"ingredient": "Soon", "qty_grams": 7000, "expiry_date": "2026-06-06"},
        ]
        by_item = {item["item"]: item for item in calculate_restock_needs(inventory_data, REFERENCE_DATE)}
        self.assertEqual(by_item["Expired"]["qty_needed_grams"], 10000)
        self.assertIn("Expired", by_item["Expired"]["reason"])
        self.assertEqual(by_item["Soon"]["qty_needed_grams"], 3000)
        self.assertIn("Expiring soon", by_item["Soon"]["reason"])

    # @spec CKS-RESTOCK-003
    def test_multiple_restock_reasons_are_preserved_in_stable_order(self):
        inventory_data = [{"ingredient": "Cream", "qty_grams": 500, "expiry_date": "2026-06-02"}]
        result = calculate_restock_needs(
            inventory_data, REFERENCE_DATE,
            {"Cream": ["Insufficient for order", "Insufficient for order"]},
        )
        self.assertEqual(result[0]["reason"], "Running low on stock; Expired; Insufficient for order")

    # @spec CKS-RESTOCK-004
    def test_failed_missing_and_insufficient_ingredients_reach_final_restock(self):
        recipe_data = [{
            "recipe_id": 1, "name": "Combo",
            "ingredients": [{"name": "Rice", "qty_grams": 12000}, {"name": "Spice", "qty_grams": 50}],
        }]
        inventory_data = [{"ingredient": "Rice", "qty_grams": 11000, "expiry_date": "2026-12-31"}]
        restock_data = []
        process_orders(
            recipe_data, inventory_data,
            [{"order_id": 501, "brand": "Test", "items": [{"item": "Combo", "qty": 1}]}],
            [], restock_data, REFERENCE_DATE,
        )
        by_item = {item["item"]: item for item in restock_data}
        self.assertEqual(by_item["Rice"]["qty_needed_grams"], 0)
        self.assertIn("Insufficient for order", by_item["Rice"]["reason"])
        self.assertEqual(by_item["Spice"]["qty_needed_grams"], 10000)
        self.assertIn("Missing from inventory", by_item["Spice"]["reason"])

    # @spec CKS-RESTOCK-005
    def test_restock_record_includes_quantity_and_expiry_context(self):
        result = calculate_restock_needs(
            [{"ingredient": "Cream", "qty_grams": 500, "expiry_date": "2026-06-06"}], REFERENCE_DATE
        )
        self.assertEqual(
            set(result[0]),
            {"item", "current_qty_grams", "qty_needed_grams", "reason", "expiry_date", "days_until_expiry"},
        )
        self.assertEqual(result[0]["days_until_expiry"], 3)

    # @spec CKS-RESTOCK-002, CKS-RESTOCK-005
    def test_invalid_expiry_requests_full_replacement(self):
        result = calculate_restock_needs(
            [{"ingredient": "Cream", "qty_grams": 7000, "expiry_date": "invalid"}], REFERENCE_DATE
        )
        self.assertEqual(result[0]["qty_needed_grams"], 10000)
        self.assertEqual(result[0]["reason"], "Invalid expiry")
        self.assertEqual(result[0]["expiry_date"], "invalid")
        self.assertIsNone(result[0]["days_until_expiry"])

    # @spec CKS-RESTOCK-006
    def test_restock_table_is_replaced_and_consolidated_per_ingredient(self):
        inventory_data = [{"ingredient": "Rice", "qty_grams": 500, "expiry_date": "2026-12-31"}]
        restock_data = [{"item": "Old", "qty_needed_grams": 1, "reason": "Old"}]
        recipe_data = [{"recipe_id": 1, "name": "Rice Bowl", "ingredients": [{"name": "Rice", "qty_grams": 600}]}]
        orders = [
            {"order_id": 601, "brand": "Test", "items": [{"item": "Rice Bowl", "qty": 1}]},
            {"order_id": 602, "brand": "Test", "items": [{"item": "Rice Bowl", "qty": 1}]},
        ]
        process_orders(recipe_data, inventory_data, orders, [], restock_data, REFERENCE_DATE)
        self.assertEqual(len(restock_data), 1)
        self.assertEqual(restock_data[0]["item"], "Rice")
        self.assertNotIn("Old", [item["item"] for item in restock_data])
        self.assertEqual(restock_data[0]["reason"].count("Insufficient for order"), 1)


class TestBusinessSummary(unittest.TestCase):
    """Verify the structured and printed manager-facing summary."""

    def setUp(self):
        self.inventory_data = [
            {"ingredient": "Rice", "qty_grams": 400, "expiry_date": "2026-12-31"},
            {"ingredient": "Cream", "qty_grams": 7000, "expiry_date": "2026-06-02"},
        ]
        self.restock_data = calculate_restock_needs(self.inventory_data, REFERENCE_DATE)
        self.processed_orders = [
            {"order_id": 1, "fulfilled": True, "reason": "Delivered"},
            {"order_id": 2, "fulfilled": False, "reason": "Rice (Insufficient quantity)"},
        ]

    # @spec CKS-REPORT-001
    def test_summary_contains_all_required_business_results(self):
        summary = build_business_summary(
            self.processed_orders, self.inventory_data, self.restock_data, REFERENCE_DATE
        )
        self.assertEqual(summary["delivered_count"], 1)
        self.assertEqual(summary["not_delivered_count"], 1)
        self.assertEqual(summary["delivered_order_ids"], [1])
        self.assertEqual(summary["not_delivered_orders"], [{"order_id": 2, "reason": "Rice (Insufficient quantity)"}])
        self.assertEqual(summary["final_inventory"], self.inventory_data)
        self.assertEqual(summary["restock_recommendations"], self.restock_data)
        self.assertEqual(summary["expiry_concerns"][0]["ingredient"], "Cream")
        self.assertEqual(summary["expiry_concerns"][0]["status"], "Expired")

    # @spec CKS-REPORT-002
    def test_printed_summary_uses_manager_facing_sections(self):
        summary = build_business_summary(
            self.processed_orders, self.inventory_data, self.restock_data, REFERENCE_DATE
        )
        output = StringIO()
        with redirect_stdout(output):
            print_business_summary(summary)
        displayed = output.getvalue()
        for text in (
            "Business Summary", "Orders Delivered: 1", "Orders Not Delivered: 1",
            "Final Inventory", "Restock Recommendations", "Expiry Concerns",
            "Rice (Insufficient quantity)",
        ):
            self.assertIn(text, displayed)


if __name__ == "__main__":
    unittest.main()
