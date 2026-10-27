expenses =[] #create a empty list
budget = 0
def add_expense():
    name = input("enter expense name:")
    category = input("enter category:")
    amount = float(input("enter amount:"))

#creating dictionary expense
    expense = {
        "name" : name,
        "category":category,
        "amount":amount
    }
    expenses.append(expense)
    print("added expense")


def view_expenses():
    if len(expenses) ==0: #checks whether expenses is empty
        print("no expenses")
        return  #stop function here

    print("\n----- Transaction History -----")

    for i, expense in enumerate(expenses):  #give number and expense one by one
        print(f"{i + 1}. {expense['name']} | {expense['amount']} Rs. | {expense['category']}")

def update_expense():
    view_expenses()

    if len(expenses) == 0:
        return

    number = int(input("Enter transaction number to update: "))

    if number < 1 or number > len(expenses):
        print("Invalid transaction number.")
        return

    expense = expenses[number - 1] #user ley 2 enter garo vane index wise ..2-1=1 so out-> 1 ko

    expense["name"] = input("Enter new expense name: ")
    expense["category"] = input("Enter new category: ")
    expense["amount"] = float(input("Enter new amount: "))

    print("Expense updated successfully!")

def delete_expense():
        view_expenses()

        if len(expenses) == 0: #len(expense)..how many expenses are in the list
            return

        number = int(input("Enter transaction number to delete: "))

        if number < 1 or number > len(expenses): #Is the number greater than the number of expenses?
            print("Invalid transaction number.")
            return

        expenses.pop(number - 1)

        print("Expense deleted successfully!")


def total_spending():
    total = 0 #variable to store value

    for expense in expenses:   #the loop takes one expense at a time(
        total += expense["amount"] # 0+expense amount

    print("Total spending: Rs.", total)


def category_summary():

    if len(expenses) == 0:
        print("No expenses found.")
        return

    summary = {} #empty dictionary then we gradually add information to it.

    for expense in expenses:  #Go through each expense, one at a time.
        category = expense["category"]  #taking category value from dictionary
        amount = expense["amount"]

        summary[category] = summary.get(category, 0) + amount #Look for this category in summary.
                                                        # If it doesn't exist, give me 0.

    print("\n----- Category Summary -----")

    for category, amount in summary.items(): #This takes each pair and puts them into two variables:
                                             # summary.items ->gets both the key and value from the dictionary.
        print(f"{category}: Rs. {amount}")

def set_budget():
    budget = float(input("Enter your budget: "))
    print("Budget set to Rs.", budget)
    return budget


def budget_alert(budget):
    total = 0

    for expense in expenses:
        total += expense["amount"]

    if budget == 0:
        print("Please set a budget first.")
        return

    print("\n----- Budget Alert -----")
    print("Budget: Rs.", budget)
    print("Spent: Rs.", total)
    print("Remaining: Rs.", budget - total)

    if total > budget:
        print("ALERT: You have exceeded your budget!")
    elif total == budget:
        print("You have reached your budget.")
    else:
        print("You are within your budget.")

while True:

    print("\n========== EXPENSE TRACKER ==========")
    print("1. Add Expense")
    print("2. View Expenses")
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
        budget = set_budget()

    elif choice == "8":
        budget_alert(budget)

    elif choice == "9":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice. Please try again.")