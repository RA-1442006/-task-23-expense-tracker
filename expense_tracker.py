import csv
from datetime import datetime
import os

# -----------------------------------------
# Storage functions
# -----------------------------------------

def load_expenses(filename):
    expenses = []
    
    # if the file does not exist, create it with headers
    if not os.path.exists(filename):
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "category", "description", "amount"])
        except IOError as e:
            print(f"Error creating file {filename}: {e}")
        return expenses

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    amount = float(row["amount"])
                    expenses.append({
                        "date": row["date"],
                        "category": row["category"],
                        "description": row["description"],
                        "amount": amount
                    })
                except (ValueError, KeyError):
                    # skip rows with bad or missing values
                    continue
    except IOError as e:
        print(f"Error reading file {filename}: {e}")

    return expenses


def save_expense(filename, expense):
    # append one expense to the csv file
    try:
        with open(filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                expense["date"],
                expense["category"],
                expense["description"],
                f"{expense['amount']:.2f}"
            ])
    except IOError as e:
        print(f"Error saving expense: {e}")


def save_all_expenses(filename, expenses):
    # rewrite the whole file (used when an expense is deleted)
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "description", "amount"])
            for exp in expenses:
                writer.writerow([
                    exp["date"],
                    exp["category"],
                    exp["description"],
                    f"{exp['amount']:.2f}"
                ])
    except IOError as e:
        print(f"Error saving file: {e}")


# -----------------------------------------
# Calculation functions
# -----------------------------------------

def total_spending(expenses):
    total = 0.0
    for item in expenses:
        total += item["amount"]
    return total


def summary_by_category(expenses):
    summary = {}
    for item in expenses:
        cat = item["category"]
        if cat in summary:
            summary[cat] += item["amount"]
        else:
            summary[cat] = item["amount"]
    return summary


def filter_by_month(expenses, year_month):
    filtered = []
    for item in expenses:
        if item["date"].startswith(year_month):
            filtered.append(item)
    return filtered


# -----------------------------------------
# Input validation helpers
# -----------------------------------------

def get_valid_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD format (e.g. 2026-10-15).")


def get_valid_amount(prompt):
    while True:
        value = input(prompt).strip()
        try:
            amount = float(value)
            if amount > 0:
                return round(amount, 2)
            else:
                print("Amount must be a positive number greater than 0.")
        except ValueError:
            print("Invalid number. Please enter a valid amount (e.g. 24.50).")


def get_non_empty_text(prompt, field_name):
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print(f"{field_name} cannot be empty. Please enter a value.")


# -----------------------------------------
# User interaction / UI functions
# -----------------------------------------

def display_expense_table(expenses, show_index=False):
    if not expenses:
        print("No expenses to display.")
        return

    if show_index:
        print(f"{'#':<4} {'Date':<12} {'Category':<15} {'Description':<28} {'Amount':>10}")
        print("-" * 73)
        for idx, item in enumerate(expenses, start=1):
            print(f"{idx:<4} {item['date']:<12} {item['category']:<15} {item['description']:<28} ${item['amount']:>9.2f}")
    else:
        print(f"{'Date':<12} {'Category':<15} {'Description':<28} {'Amount':>10}")
        print("-" * 68)
        for item in expenses:
            print(f"{item['date']:<12} {item['category']:<15} {item['description']:<28} ${item['amount']:>9.2f}")


def add_expense_view(expenses, filename):
    print("\n--- Add New Expense ---")
    date_str = get_valid_date("Enter date (YYYY-MM-DD): ")
    category = get_non_empty_text("Enter category: ", "Category")
    description = get_non_empty_text("Enter description: ", "Description")
    amount = get_valid_amount("Enter amount: ")

    new_expense = {
        "date": date_str,
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(new_expense)
    save_expense(filename, new_expense)
    print(f"Expense of ${amount:.2f} for '{description}' added successfully!")


def view_all_expenses_view(expenses):
    print("\n--- All Recorded Expenses ---")
    display_expense_table(expenses)
    print(f"\nTotal records: {len(expenses)}")


def category_summary_view(expenses):
    print("\n--- Category-Wise Spending Summary ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = summary_by_category(expenses)
    print(f"{'Category':<18} {'Total Spent':>12}")
    print("-" * 32)
    for cat, amt in summary.items():
        print(f"{cat:<18} ${amt:>11.2f}")

    overall = total_spending(expenses)
    print("-" * 32)
    print(f"{'Total':<18} ${overall:>11.2f}")


def total_spending_view(expenses):
    print("\n--- Total Spending Report ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = total_spending(expenses)
    count = len(expenses)
    average = total / count if count > 0 else 0.0

    print(f"Number of expenses: {count}")
    print(f"Total spending:     ${total:.2f}")
    print(f"Average per item:   ${average:.2f}")


def filter_by_month_view(expenses):
    print("\n--- Filter Expenses by Month ---")
    while True:
        month_input = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month_input, "%Y-%m")
            break
        except ValueError:
            print("Invalid month format. Please use YYYY-MM (e.g. 2026-09).")

    matched = filter_by_month(expenses, month_input)
    print(f"\nExpenses for {month_input}:")
    if not matched:
        print(f"No expenses found for {month_input}.")
        return

    display_expense_table(matched)
    month_total = total_spending(matched)
    print("-" * 68)
    print(f"{'Month Total:':<57} ${month_total:>9.2f}")


def delete_expense_view(expenses, filename):
    print("\n--- Delete an Expense ---")
    if not expenses:
        print("No expenses to delete.")
        return

    display_expense_table(expenses, show_index=True)
    print()

    while True:
        choice = input("Enter the item # to delete (or press Enter to cancel): ").strip()
        if choice == "":
            print("Deletion cancelled.")
            return

        try:
            item_num = int(choice)
            if 1 <= item_num <= len(expenses):
                removed = expenses.pop(item_num - 1)
                save_all_expenses(filename, expenses)
                print(f"Removed: {removed['date']} - {removed['category']} - {removed['description']} (${removed['amount']:.2f})")
                return
            else:
                print(f"Please enter a number between 1 and {len(expenses)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# -----------------------------------------
# Main loop
# -----------------------------------------

def main():
    # keep data file in the same folder as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "expenses.csv")
    expenses = load_expenses(filename)

    while True:
        print("\n==============================")
        print("    Simple Expense Tracker")
        print("==============================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category Summary")
        print("4. Total Spending Report")
        print("5. Filter by Month")
        print("6. Delete an Expense")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            add_expense_view(expenses, filename)
        elif choice == "2":
            view_all_expenses_view(expenses)
        elif choice == "3":
            category_summary_view(expenses)
        elif choice == "4":
            total_spending_view(expenses)
        elif choice == "5":
            filter_by_month_view(expenses)
        elif choice == "6":
            delete_expense_view(expenses, filename)
        elif choice == "7":
            print("\nGoodbye! Have a great day.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
