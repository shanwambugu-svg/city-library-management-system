# City Library Management System

A command-line Python application for managing a public library's books, members, and loan transactions.

---

## Project Purpose

This system allows library staff to:
- Maintain a catalogue of books with availability tracking
- Register and manage library members
- Process book checkouts and returns
- Monitor overdue loans
- Persist all data to CSV files across sessions

---

## Installation

**Requirements:** Python 3.8 or higher. No third-party packages are needed — only Python standard library modules are used (`csv`, `os`, `datetime`).

```bash
# Clone or download the repository
git clone https://github.com/yourusername/library-system.git
cd library-system
```

---

## Running the Application

```bash
python main.py
```

The system will load existing data from the `data/` folder automatically. Sample data is included.

---

## Example Usage

```
Welcome to the City Library Management System

=============================================
     CITY LIBRARY MANAGEMENT SYSTEM
=============================================
  1. List all books
  2. Search for a book
  3. Add a new book
  4. List all members
  5. Register a new member
  6. Check out a book
  7. Return a book
  8. View overdue loans
  9. Save data
  0. Exit
=============================================
Select an option (0-9): 2

--- Search Books ---
Enter title, author, or genre to search: python
1 result(s) found:
[B009] 'Python Crash Course' by Eric Matthes (2023) | Genre: Technology | Copies: 3/3 | Available
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| Book catalogue | Add, search, and list all books with copy tracking |
| Member management | Register members; enforce a 5-book loan limit |
| Loan processing | Checkout and return books with automatic due-date calculation |
| Overdue detection | Flags loans past their 14-day return window |
| CSV persistence | All data saved to and loaded from `data/*.csv` |
| Exception handling | Invalid input (non-numeric year, empty fields) is caught gracefully |

---

## File Structure

```
library-system/
├── main.py          # Entry point — interactive menu
├── library.py       # Library class — central controller + file I/O
├── book.py          # Book class — catalogue item
├── member.py        # Member class — patron account
├── loan.py          # Loan class — borrow/return transaction
├── data/
│   ├── books.csv    # Persisted book catalogue
│   ├── members.csv  # Persisted member records
│   └── loans.csv    # Persisted loan history
└── README.md
```

---

## Data Files

All data is stored in plain CSV format in the `data/` directory. Sample data is provided. Files are updated every time the user selects **Save (option 9)** or **Exit (option 0)**.
