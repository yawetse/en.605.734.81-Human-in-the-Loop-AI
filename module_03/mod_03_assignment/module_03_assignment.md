---
{
  "id": "file_x69c6jnd",
  "filetype": "document",
  "filename": "module_03_assignment",
  "created_at": "2026-09-20T12:21:48.908Z",
  "updated_at": "2026-09-20T12:22:02.978Z",
  "meta": {
    "location": "/",
    "tags": [],
    "categories": [],
    "description": "",
    "source": "markdown"
  }
}
---
# Module 3 Assignment: AI-Assisted Coding for a Cloud Kitchen Inventory Simulation

- **Due** Sunday by 11:59pm
- **Points** 100
- **Submitting** a file upload

## Overview

In this assignment, you will use AI as a coding assistant to audit, test, debug, refine, and complete a Python-based inventory simulation for a cloud kitchen.

A cloud kitchen is a delivery-only food business where multiple virtual restaurant brands share the same kitchen, staff, equipment, and ingredients. This creates operational challenges because the same ingredients may be used across many menu items and brands. If one ingredient runs out or expires, several menu items may become unavailable at the same time.

You are starting from a provided, mostly working implementation. Your task is to compare the starter code against the requirements, verify what already works, identify gaps or incorrect assumptions, and make targeted changes so the final simulation processes customer orders, checks recipe-linked inventory, updates delivery status, deducts ingredient quantities, tracks expiry risk, and creates a restock plan.

The purpose of this assignment is not to rewrite code that already works. You must demonstrate that you can inspect existing and AI-assisted code critically, test it, identify missing or incorrect behavior, make focused improvements, and document your decisions.

## Files Provided

You will receive the following files from your instructor:

- [<u>AI-Assisted Cloud Kitchen Inventory Simulation.pdf</u>](https://jhu.instructure.com/courses/134608/files/18914494?wrap=1)
- [<u>seed_data-1.py</u>](https://jhu.instructure.com/courses/134608/files/18914498?wrap=1)[Download seed_data-1.py](https://jhu.instructure.com/courses/134608/files/18914498/download?download_frd=1)
- [<u>main.py</u>](https://jhu.instructure.com/courses/134608/files/18914360?wrap=1)[Download main.py](https://jhu.instructure.com/courses/134608/files/18914360/download?download_frd=1)
- [<u>test_main.py</u>](https://jhu.instructure.com/courses/134608/files/18914358?wrap=1)[Download test_main.py](https://jhu.instructure.com/courses/134608/files/18914358/download?download_frd=1)

You will need to create your own files,

- `PROJECT_SPEC.md`
- `AI_USAGE_LOG.md`

## Learning Objectives

By completing this assignment, you will be able to:

- Use AI tools to review, test, debug, and improve an existing Python program.
- Compare an existing implementation against written software requirements.
- Maintain a project specification file to reduce context drift when using AI.
- Evaluate starter and AI-generated code instead of accepting it uncritically.
- Run and expand unit tests to verify existing and modified functions.
- Implement or correct rule-based business logic in Python.
- Explain the difference between AI-assisted coding and autonomous AI decision-making.
- Reflect on the strengths and limitations of using AI as a programming partner.

## Business Scenario

A cloud kitchen operates multiple virtual brands from one shared kitchen. Each menu item is linked to a recipe, and each recipe consumes ingredients from a shared inventory.

The kitchen faces several operational problems:

- Ingredients may run out mid-shift.
- Orders may be accepted for menu items the kitchen cannot fulfill.
- Expired or soon-to-expire ingredients may create waste or quality risk.
- Restocking may be inefficient if the kitchen lacks visibility into ingredient usage.
- Manual menu and inventory updates can cause errors.

You will audit and complete a Python simulation that models these problems and creates a more reliable inventory workflow.

## Role of AI in This Assignment

You are expected to use AI as a coding assistant while reviewing and improving the provided starter implementation, but you are responsible for the final result.  Treat the starter code the way you would treat work from a fast but unreliable junior developer: it gives you a useful head start, but it may contain assumptions, incomplete logic, weak tests, or requirements that have not yet been implemented. Throughout the assignment, you will play three roles:

1. **Navigator**\
   You compare the requirements with the current code, decide what needs attention, and choose what to ask the AI to do.
2. **Reviewer**\
   You inspect provided and AI-generated code, identify assumptions, check outputs, run tests, and look for gaps or errors.
3. **Decision-Maker**\
   You decide what to keep, change, reject, test, or refactor, and you are responsible for understanding the final code.

You may use AI to explain existing code, identify gaps, generate targeted changes, suggest tests, debug failures, and improve explanations. Do not replace working code merely to show that you wrote it.

## How to Use the Provided Starter Code

The provided main.py and test_main.py files are starter files, not examples to discard and not complete solutions.

Begin by running the provided program and the provided test suite to establish a baseline before making changes.

1. Keep and modify the provided main.py. Add or change code only where needed to satisfy a requirement.
2. Keep and expand the provided test_main.py. Add or update tests for behavior you change or discover is not covered.
3. Use seed_data.py as the supplied data source and schema. Do not redesign the data simply to make the code easier.
4. Compare the existing implementation against each requirement and task before deciding whether code needs to change.
5. Do not assume that a passing provided test suite means the assignment is complete. The starter tests are a baseline, not complete coverage.
6. For each change, use an incremental workflow: plan, make one focused change, review it, test it, and debug before moving on.
7. Add or revise unit tests for every requirement you implement, correct, or find insufficiently tested.
8. Update PROJECT_SPEC.md and AI_USAGE_LOG.md as you work so your decisions and AI-assisted process are documented.

You are graded on review, testing, corrections, documentation, and understanding - not on rewriting code that already works. If the reference PDF conflicts with this Assignment Overview, follow this Assignment Overview.

## Required Project Files

Your working project folder should include:

```
main.py
seed_data.py
test_main.py
PROJECT_SPEC.md
AI_USAGE_LOG.md
```

You may add additional files if useful.

### `main.py`

This is the provided starter implementation. Keep it and modify or add functions only as needed to satisfy the assignment requirements.

### `seed_data.py`

This is the provided source data for recipes, inventory, orders, restock records, and delivery status. Use its existing structure as the source of truth unless your instructor tells you otherwise.

### `test_main.py`

This is the provided baseline unit test suite. Run it first, then add or modify tests so all required behavior is meaningfully tested.

### `PROJECT_SPEC.md`

You will create this file as the project's external memory. It should summarize:

- What the project is supposed to do
- What the starter code already appears to implement and its current status
- Important design decisions and changes you make
- Business rules
- Constraints
- Current task, next task, and verification status
- Known issues or assumptions

### `AI_USAGE_LOG.md`

You will create this file to document how you used AI. For each major interaction, include:

- The task you were working on
- The prompt you gave the AI
- A short summary of the AI’s response
- What you accepted, changed, or rejected
- Any issues you found in the AI output

You do not need to include every minor prompt, but your log should provide enough evidence to show that you reviewed the starter code and used AI thoughtfully and critically rather than replacing the project wholesale.

## Core Data Structures

Your simulation will use five core data structures from `seed_data.py`:

```
Recipes
Inventory
Orders
Restock
Status
```

Inspect and use the exact structures provided in seed_data.py rather than assuming a different schema or redesigning the data to fit a new solution.

## Functional Requirements

The final version of your program must satisfy all of the following functionality. Some requirements are already partially or fully implemented in the starter code; verify them before rewriting anything.

### Requirement 1: Load and Display Data

Inspect the existing functions that import and display the major data structures from `seed_data.py`. Modify them only if necessary to satisfy this requirement.

Your program should be able to show:

- Recipes
- Inventory
- Orders
- Restock records
- Delivery status records

Use the existing code and tests to confirm that the program can access all required data. If this already works correctly, document that verification and move on.

### Requirement 2: Process Orders Against Recipes

Verify that, for each order, your final program can:

- Identify the menu item or items ordered.
- Look up the corresponding recipe.
- Calculate the total ingredient quantity required.
- Handle item quantities correctly.
- Handle missing or unknown recipes gracefully.

For example, if an order contains quantity 2 of a menu item, the required ingredient quantities should be doubled.

### Requirement 3: Check Inventory Availability

Inspect the existing inventory check and modify it as needed so the required ingredients are both available in sufficient quantity and usable.

The check should account for:

- Ingredient name
- Quantity required
- Quantity available
- Expiry status, if expiry dates are included in the inventory data

The final inventory check should return clear information about whether the order can be fulfilled and, if not, what is missing, insufficient, expired, or otherwise unavailable.

### Requirement 4: Fulfill Orders and Deduct Inventory

If all required ingredients are available, your program should:

- Mark the order as `Delivered`
- Deduct the used ingredient quantities from inventory

If required ingredients are missing or unavailable, your program should:

- Mark the order as `Not Delivered`
- Record the reason
- Add missing or unavailable ingredients to the restock list

The base assignment uses all-or-nothing fulfillment: a failed order should not deduct partial inventory. Partial fulfillment is an optional enhancement only.

### Requirement 5: Make Inventory Deduction Cumulative

Inventory deduction must be cumulative.

This means:

- Order 1 consumes inventory.
- Order 2 checks against the inventory remaining after Order 1.
- Order 3 checks against the inventory remaining after Orders 1 and 2.
- The final inventory table should reflect all delivered orders.

Do not reset inventory between orders unless you are running a separate test case.

### Requirement 6: Apply Restock and Expiry Rules

After processing orders, apply restock logic.

Your program should identify ingredients that meet any of the following conditions:

- Ingredient is out of stock.
- Ingredient is running low.
- Ingredient is expired or expiring soon.

Unless your instructor provides different values, use these rules:

```
Running low threshold: quantity ≤ 1,000g
Par level: 10,000g
Expiring soon window: within 5 days of the simulation date. Use an explicit reference date in unit tests so results are reproducible.
```

Your restock output should include:

- Ingredient name
- Current quantity
- Reason for restock
- Quantity needed to reach par level
- Any relevant expiry information

If an ingredient qualifies for more than one reason, your code should preserve all relevant reasons instead of silently overwriting them.

### Requirement 7: Produce a Business-Friendly Summary

At the end of the simulation, produce a clear summary that includes:

- Number of orders delivered
- Number of orders not delivered
- Final inventory levels
- Restock recommendations
- Any ingredients that are low, out of stock, expired, or expiring soon
- Any orders that could not be fulfilled and why

This output should be understandable to a non-technical kitchen manager.

## Required AI Prompt Templates

Use the following prompt patterns during the assignment.

### Planning Prompt

Use this before building a major component.

```
I am reviewing [COMPONENT OR FEATURE] in an existing Python project. Before writing any code, give me a high-level plan for comparing the current implementation with these requirements: [PASTE REQUIREMENTS]. Tell me what to inspect first. Do not write code yet.
```

### Task Breakdown Prompt

Use this after you have a plan.

```
Here is component [COMPONENT NAME] from the existing project, along with the requirement it must satisfy. Break only the necessary work into small implementation and testing tasks. Do not rewrite working behavior without a reason.
```

### Implementation Prompt

Use this for one task at a time.

```
Modify Task [N]: [DESCRIPTION]. Start from the existing Python code. Change only what is necessary to meet the requirement, keep the code simple, and add comments where useful. Do not rewrite unrelated working functions.
```

### Validation Hook Prompt

Use this after AI generates code.

```
After generating the code, add inline comments or notes that identify:
1. Any assumptions you made that I should verify
2. What existing behavior or tests could be affected by the change
3. Any sections that are incomplete or require follow-up
```

### Debugging Prompt

Use this when code fails or results are unexpected.

```
Here is the relevant current code and the error or unexpected result: [PASTE CODE] / [PASTE ERROR OR OUTPUT]. Explain the root cause, then provide the smallest reasonable correction with comments explaining what changed and why.
```

## Required Tasks

### Task 1: Set Up the Project

Organize the provided starter files and create the two required documentation files:

```
main.py
seed_data.py
test_main.py
PROJECT_SPEC.md
AI_USAGE_LOG.md
```

Run main.py and the complete provided test suite before changing code. Record whether they run successfully and note any failures or setup issues.

In your written response, explain:

- Which files were provided and which files you created.
- How to run your program.
- How to run your tests.

What the baseline test result was and any setup issues you encountered.

### Task 2: Create `PROJECT_SPEC.md`

Create a project specification file that documents your current understanding of the project and the current state of the starter code.

It should include:

- Project purpose
- Data structures
- Business rules
- What appears to be already implemented and what still needs verification or work
- Testing plan, including gaps you identify in the starter test suite
- Open questions or assumptions

Update this file throughout the assignment as you verify, change, or complete components.

### Task 3: Audit Data Loading and Seed Data

Inspect the existing loading and display functions rather than rewriting them automatically. Verify that they correctly access the five main data structures and modify them only if needed.

The final code should show that it can access:

- Recipes
- Inventory
- Orders
- Restock
- Status

Run the provided tests and add or update tests as needed to verify:

- All required data structures are present.
- Each data structure has the expected type.
- Each data structure contains records.
- Key fields are present.

### Task 4: Audit Recipe Lookup and Ingredient Calculation

Inspect the existing recipe lookup and ingredient calculation functions. Modify them only if necessary to meet the requirements below.

The final implementation should:

- Accept an item name or order line.
- Return the required ingredients and quantities.
- Handle missing recipes gracefully.

Run the provided tests and add or update tests for:

- A valid item with a matching recipe.
- An invalid item with no matching recipe.

A quantity greater than 1.

### Task 5: Complete the Inventory Availability Check

Inspect the existing availability logic and modify it as needed so it fully determines whether an entire order can be fulfilled.

The final implementation should:

- Compare required ingredients against available stock.
- Identify missing ingredients.
- Identify ingredients with insufficient quantity.
- Identify expired or otherwise unusable ingredients when expiry data is available.

Run the provided tests and add or update tests for:

- All ingredients available.
- One ingredient missing.
- One ingredient with insufficient quantity.

One expired or otherwise unusable ingredient.

### Task 6: Audit and Complete Fulfillment Logic

Inspect the existing order-processing and fulfillment logic. Modify it only as needed so the complete order follows the rules below.

If the order can be fulfilled:

- Mark it as delivered.
- Deduct ingredients from inventory.

If the order cannot be fulfilled:

- Mark it as not delivered.
- Record the reason.
- Add missing or unavailable ingredients to restock recommendations.

Run the provided tests and add or update tests for:

- Successful delivery.
- Failed delivery due to missing stock.
- Correct inventory deduction after delivery.

No unintended deduction after failed delivery.

### Task 7: Verify Cumulative Order Processing

Inspect the existing sequential order-processing logic and verify that inventory is cumulative. Modify it only if testing shows that it does not meet the requirement.

Your function should ensure that each order uses the inventory remaining after previous delivered orders.

Run the provided tests and add or update tests for:

- Two orders consuming the same ingredient.
- An order that fails because an earlier order used the remaining stock.

Final inventory matching expected values.

### Task 8: Complete Restock and Expiry Rules

Inspect the existing restock function and modify it as needed so it satisfies every rule below.

Your logic should account for:

- Out-of-stock ingredients
- Low-stock ingredients
- Expired and expiring-soon ingredients
- Multiple simultaneous restock reasons for the same ingredient

Run the provided tests and add or update tests for:

- Ingredient with zero stock
- Ingredient below or equal to the low-stock threshold
- Ingredient above the threshold
- Ingredient expired and ingredient expiring soon (include both cases in your tests)
- Ingredient with multiple restock reasons

### Task 9: Generate Final Business Summary

Add or create a final output that summarizes the simulation for a business user.

The summary should include:

- Delivered orders
- Not delivered orders
- Reasons for non-delivery
- Final inventory
- Restock recommendations
- Expiry concerns

The output may be printed to the console, returned as a dictionary, or written to a text or Markdown file.

### Task 10: Refactor and Review

After completing the core functionality, review your code for:

- Duplicate logic
- Hard-coded values that should be constants
- Unclear function names
- Missing comments
- Weak error handling
- Functions that do too much

Use AI to help identify possible refactoring opportunities, but you decide what to change.

Document at least two improvements you made during refactoring.

### Task 11: Reflection on AI-Assisted Coding

Write a 400–600 word reflection addressing the following questions:

- How did AI help you move faster?
- Where did AI make mistakes or questionable assumptions?
- How did testing help you evaluate AI-generated code?
- What did you change or reject from the AI’s suggestions?
- How did `PROJECT_SPEC.md` help maintain context?
- What would you do differently in a future AI-assisted coding project?

## Optional Enhancement

Choose one optional enhancement if you want to go beyond the base requirements.

### Option A: Partial Fulfillment

Modify the logic so that if part of an order can be fulfilled, those items are delivered and only unavailable items are marked as not delivered.

### Option B: Predictive Stockout Alert

Estimate which ingredients are likely to run out soon based on observed consumption across orders.

### Option C: Dynamic Menu Item Disabling

Identify menu items that should be marked unavailable because one or more required ingredients are out of stock or unusable.

### Option D: Improved Reporting

Generate a polished business report in Markdown, CSV, or HTML format.

Optional enhancements may earn extra credit if they are working, tested, and clearly documented.

## Deliverables

Submit the following:

1. `main.py`
2. `test_main.py`
3. `PROJECT_SPEC.md`
4. `AI_USAGE_LOG.md`
5. Written reflection
6. Optional: any additional output files or reports

Keep the provided seed_data.py with your working project. Unless your instructor asks for it, you do not need to resubmit an unchanged copy. Do not submit files containing private credentials, API keys, or unrelated personal information.

## Suggested Written Response Structure

Use the following headings:

```
Project Setup
Data Loading and Audit
Recipe Lookup Audit
Inventory Availability
Order Fulfillment
Cumulative Processing
Restock and Expiry Logic
Business Summary
Refactoring Notes
AI Usage Summary
Reflection
```

## Minimum Technical Requirements

Your submission must demonstrate:

- A working final version of the provided main.py, with targeted changes where needed.
- Use of the provided seed_data.py and its existing schema.
- Verified functionality for data loading, recipe lookup, inventory checking, order fulfillment, cumulative processing, restock and expiry logic, and final reporting.
- The provided tests plus meaningful added or updated unit tests for requirements not fully covered by the baseline suite.
- Evidence that the full test suite was run after your changes.
- A maintained `PROJECT_SPEC.md`.
- An `AI_USAGE_LOG.md`.
- A written reflection on AI-assisted coding.

## Grading Rubric

Total: 100 points

### 1. Project Setup and Data Loading — 10 points

Full credit requires a clear project structure, successful import of `seed_data.py`, and working functions to access the five core data structures.

### 2. Recipe Lookup and Ingredient Calculation — 10 points

Full credit requires correct recipe lookup, quantity scaling, and graceful handling of missing recipes.

### 3. Inventory Availability Logic — 10 points

Full credit requires accurate comparison of required ingredients against available inventory, including missing or insufficient ingredients.

### 4. Fulfillment and Status Updates — 15 points

Full credit requires correct delivery status updates, inventory deduction for delivered orders, no unintended deduction for failed orders, meaningful failure reasons, and adherence to the base all-or-nothing rule.

### 5. Cumulative Inventory Processing — 10 points

Full credit requires inventory to be updated across sequential orders so later orders use remaining stock.

### 6. Restock and Expiry Logic — 10 points

Full credit requires correct handling of low stock, out-of-stock, expiring soon, and multiple restock reasons.

### 7. Unit Testing — 15 points

Full credit requires meaningful tests for major functions, including normal cases, edge cases, and failure cases. Tests must be runnable and results must be visible or documented.

### 8. AI-Assisted Development Process — 10 points

Full credit requires a useful `PROJECT_SPEC.md`, meaningful AI usage documentation, evidence of prompt-based iteration, and evidence that the student inspected and improved the starter code rather than blindly replacing or accepting it.

### 9. Code Quality and Refactoring — 5 points

Full credit requires readable, organized code with targeted changes, clear function names, constants for key thresholds, useful comments, and reduced duplication while preserving verified behavior.

### 10. Reflection — 5 points

Full credit requires a thoughtful reflection on the benefits, risks, and limitations of AI-assisted coding.

## Academic Integrity and Responsible AI Use

You are allowed and encouraged to use AI tools in this assignment. The starter code is also provided to you. You are responsible for understanding both unchanged and modified code in your final submission, and your AI use must be documented.

You may use AI to:

- Explain and review existing starter code
- Compare existing code with assignment requirements
- Generate targeted revisions or missing code
- Explain errors
- Suggest tests
- Suggest refactoring

You may not:

- Replace the starter project with AI-generated code you do not understand
- Submit code or AI-generated explanations you cannot explain
- Ignore failed tests or assume the provided test suite is complete
- Hide known defects
- Misrepresent provided starter code or AI-generated changes as work you authored without documenting your process

Your grade is based not only on whether the final program works, but also on how well you verify the starter implementation, identify gaps, test your changes, document your decisions, and demonstrate responsible AI-assisted coding practice.

## Final Checklist Before Submission

Before submitting, confirm that:

- `main.py` runs.
- `test_main.py` runs.
- The program uses `seed_data.py`.
- The final inventory is cumulative.
- Inventory availability and restock logic handle expiry correctly.
- Failed orders include reasons.
- `PROJECT_SPEC.md` is complete and updated.
- `AI_USAGE_LOG.md` documents your AI-assisted process.
- Your reflection answers all required questions.
- You can explain what the starter code already did, what you changed, what you left unchanged, and why.