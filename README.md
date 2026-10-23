# Simple Expense Tracker

A lightweight, menu-driven command-line expense tracker built in pure Python using only standard library modules. It tracks personal expenses with dates, categories, descriptions, and amounts, persists records to a CSV file, and provides spending summaries and monthly filters.

---

## Approach & Architecture

The application is structured around a clean **separation of concerns** without unnecessary complexity or classes:
- **Storage Layer (`load_expenses`, `save_expense`, `save_all_expenses`):** Handles reading and writing to `expenses.csv` using Python's built-in `csv` module. Auto-generates the file and header row if it is missing.
- **Calculation Layer (`total_spending`, `summary_by_category`, `filter_by_month`):** Pure calculation functions that operate strictly on data in memory without printing or touching files.
- **User Interface Layer (`add_expense_view`, `view_all_expenses_view`, `category_summary_view`, etc.):** Handles user inputs, displays formatted tables, and re-prompts on invalid inputs.
- **Main Control Loop (`main`):** Keeps the program running in a loop until the user selects Exit.

---

## Project Structure

```
expense_tracker/
├── expense_tracker.py   # Main Python script with menu interface
├── expenses.csv         # Persistent CSV storage with sample records
├── sample_output.txt    # Real terminal output from running the program
└── README.md            # Documentation and technical explanations
```

---

## How to Run

Ensure Python 3 is installed. Navigate to the project directory and run:

```bash
python expense_tracker.py
```

No external packages are required (uses only standard library: `csv`, `datetime`, `os`).

---

## Features

1. **Add an Expense:** Prompts for date (`YYYY-MM-DD`), category, description, and amount. Input validation ensures non-empty text, valid dates, and positive numbers.
2. **View All Expenses:** Displays all saved expenses in a formatted, aligned table with total record count.
3. **Category Spending Summary:** Calculates and prints total spending broken down by category, along with an overall grand total.
4. **Total Spending Report:** Reports the total number of transactions, total expenditure, and the average spending per item.
5. **Monthly Filtering:** Allows the user to enter a month (`YYYY-MM`) and view only expenses for that month along with the month's total spending.
6. **Delete an Expense:** Lists all expenses with index numbers and lets the user remove an entry, automatically updating the CSV file.
7. **Menu-Driven CLI:** Interactive loop allowing continuous operations until choosing option 7 (Exit).

---

## File Format (`expenses.csv`)

The data is saved in standard comma-separated values (CSV) format with the following header:

```csv
date,category,description,amount
2026-08-01,Rent,Monthly apartment rent,1200.00
2026-08-05,Food,Weekly grocery haul,85.50
2026-08-12,Bills,Water and electric utility,92.40
...
```

The bundled `expenses.csv` contains 12 realistic sample records across 6 categories (`Food`, `Travel`, `Rent`, `Shopping`, `Bills`, `Entertainment`) spanning 3 months (August, September, and October 2026).

---

## Interview Questions & Answers

### 1. How should expense records be stored in memory and on disk?
- **In Memory:** A list of dictionaries (e.g. `[{"date": "2026-09-01", "category": "Rent", "description": "...", "amount": 1200.0}, ...]`). A list preserves chronological and insertion order, making indexing and table iteration straightforward. Dictionaries allow clean, readable key-based access (`expense["amount"]`, `expense["category"]`) without needing rigid class definitions or error-prone tuple indexing.
- **On Disk:** A flat CSV file (`expenses.csv`) with a defined header row (`date,category,description,amount`). CSV is human-readable, easily inspectable in text editors and spreadsheet applications (Excel, Google Sheets), and natively supported in Python via the `csv` module with zero external dependencies.

### 2. Why should data be persisted to a file?
- In-memory variables only exist in volatile RAM while the Python process is actively executing. Once the script finishes or the machine restarts, all in-memory data is permanently erased.
- Persisting data to a non-volatile medium like `expenses.csv` guarantees data durability across program runs. When the program boots, `load_expenses()` reads the existing dataset from disk; whenever new records are created or deleted, changes are synced directly to the CSV file.

### 3. How is monthly filtering implemented?
- Because expense dates are stored in standard ISO format (`YYYY-MM-DD`), the first seven characters always represent `YYYY-MM`.
- When the user provides a target month (validated using `datetime.strptime(user_input, "%Y-%m")`), the `filter_by_month()` function iterates through the in-memory list and filters items using `item["date"].startswith(year_month)`.
- The resulting subset is then passed to `display_expense_table()` and `total_spending()` to compute that month's total expenditure, keeping the calculation reusable and completely isolated from the full dataset.

---

## Outcome

A clean, beginner-to-intermediate level Python project demonstrating practical programming fundamentals: clean code separation, robust user input validation with `try/except`, file I/O with Python's `csv` module, and an intuitive terminal user experience.
