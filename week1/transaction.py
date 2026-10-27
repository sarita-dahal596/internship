expenses = []
budget = 0


def add_expense():
    name = input("Enter expense name: ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))

    expense = {
        "name": name,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)

    print("Expense added successfully!")


def view_expenses():
    if len(expenses) == 0:
        print("No expenses found.")
        return

    print("\n----- Transaction History -----")

    for i, expense in enumerate(expenses):
        print(
            i + 1,
            "|",
            expense["name"],
            "|",
            expense["category"],
            "| Rs.",
            expense["amount"]
        )
        # print(f"{i+1}{expenses[0]['name']} | {expenses[0]['amount']} Rs. {expenses[0]['category']}")

def update_expense():
    view_expenses()

    if len(expenses) == 0:
        return

    number = int(input("Enter transaction number to update: "))

    if number < 1 or number > len(expenses):
        print("Invalid transaction number.")
        return

    expense = expenses[number - 1]

    expense["name"] = input("Enter new expense name: ")
    expense["category"] = input("Enter new category: ")
    expense["amount"] = float(input("Enter new amount: "))

    print("Expense updated successfully!")


def delete_expense():
    view_expenses()

    if len(expenses) == 0:
        return

    number = int(input("Enter transaction number to delete: "))

    if number < 1 or number > len(expenses):
        print("Invalid transaction number.")
        return

    expenses.pop(number - 1)

    print("Expense deleted successfully!")


def total_spending():
    total = 0

    for expense in expenses:
        total += expense["amount"]

    print("Total spending: Rs.", total)


def category_summary():
    if len(expenses) == 0:
        print("No expenses found.")
        return

    summary = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount

    print("\n----- Category Summary -----")

    for category, amount in summary.items():
        print(category, ": Rs.", amount)


def set_budget():
    global budget

    budget = float(input("Enter your budget: "))

    print("Budget set to Rs.", budget)


def budget_alert():
    total = 0

    for expense in expenses:
        total += expense["amount"]

    if budget == 0:
        print("Please set a budget first.")
        return

    print("Budget: Rs.", budget)
    print("Spent: Rs.", total)
    print("Remaining: Rs.", budget - total)

    if total > budget:
        print("⚠️ ALERT: You have exceeded your budget!")
    elif total == budget:
        print("⚠️ You have reached your budget.")
    else:
        print("You are within your budget.")


while True:

    print("\n========== EXPENSE TRACKER ==========")
    print("1. Add Expense")
    print("2. View Transaction History")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Total Spending")
    print("6. Category Summary")
    print("7. Set Budget")
    print("8. Budget Alert")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        update_expense()

    elif choice == "4":
        delete_expense()

    elif choice == "5":
        total_spending()

    elif choice == "6":
        category_summary()

    elif choice == "7":
        set_budget()

    elif choice == "8":
        budget_alert()

    elif choice == "9":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice. Please try again.")