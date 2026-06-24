"""
library.py
----------
Defines the Library class for the City Library Management System.
The Library acts as the central controller, managing Books, Members,
and Loans, and handling all file I/O operations.

Author: Student Submission
Course: B100 Introduction to Computer Programming with Python
"""

import csv
import os
from book import Book
from member import Member
from loan import Loan


class Library:
    """
    Central management class for the City Library System.

    Attributes:
        name (str): Name of the library.
        books (dict): Mapping of book_id -> Book objects.
        members (dict): Mapping of member_id -> Member objects.
        loans (dict): Mapping of loan_id -> Loan objects.
        data_dir (str): Directory path for CSV data files.
    """

    def __init__(self, name="City Library", data_dir="data"):
        """
        Initialise the Library and load existing data from CSV files.

        Args:
            name (str): Display name of the library.
            data_dir (str): Folder containing CSV data files.
        """
        self.name = name
        self.data_dir = data_dir
        self.books = {}
        self.members = {}
        self.loans = {}
        os.makedirs(self.data_dir, exist_ok=True)
        self._load_all_data()

    # ------------------------------------------------------------------ #
    #  DATA PERSISTENCE – File I/O                                         #
    # ------------------------------------------------------------------ #

    def _load_all_data(self):
        """Load books, members, and loans from their respective CSV files."""
        self._load_books()
        self._load_members()
        self._load_loans()

    def _load_books(self):
        """Read books from books.csv and populate self.books."""
        path = os.path.join(self.data_dir, "books.csv")
        if not os.path.exists(path):
            return
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    book = Book(
                        book_id=row["book_id"],
                        title=row["title"],
                        author=row["author"],
                        genre=row["genre"],
                        year=int(row["year"]),
                        copies=int(row["total_copies"]),
                    )
                    book.available_copies = int(row["available_copies"])
                    self.books[book.book_id] = book
        except FileNotFoundError:
            print(f"Warning: {path} not found. Starting with empty catalogue.")
        except KeyError as e:
            print(f"Error: Missing column {e} in books.csv.")

    def _load_members(self):
        """Read members from members.csv and populate self.members."""
        path = os.path.join(self.data_dir, "members.csv")
        if not os.path.exists(path):
            return
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    member = Member(
                        member_id=row["member_id"],
                        name=row["name"],
                        email=row["email"],
                        join_date=row["join_date"],
                    )
                    # Restore borrowed book list
                    if row["borrowed_books"].strip():
                        member.borrowed_books = row["borrowed_books"].split("|")
                    self.members[member.member_id] = member
        except FileNotFoundError:
            print(f"Warning: {path} not found. Starting with no members.")
        except KeyError as e:
            print(f"Error: Missing column {e} in members.csv.")

    def _load_loans(self):
        """Read loans from loans.csv and populate self.loans."""
        path = os.path.join(self.data_dir, "loans.csv")
        if not os.path.exists(path):
            return
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    loan = Loan(
                        loan_id=row["loan_id"],
                        member_id=row["member_id"],
                        book_id=row["book_id"],
                        loan_date=row["loan_date"],
                    )
                    loan.due_date = row["due_date"]
                    loan.return_date = row["return_date"] if row["return_date"] else None
                    loan.is_active = row["is_active"].lower() == "true"
                    self.loans[loan.loan_id] = loan
        except FileNotFoundError:
            print(f"Warning: {path} not found. Starting with no loans.")
        except KeyError as e:
            print(f"Error: Missing column {e} in loans.csv.")

    def save_all_data(self):
        """Persist all in-memory data back to CSV files."""
        self._save_books()
        self._save_members()
        self._save_loans()
        print("All data saved successfully.")

    def _save_books(self):
        """Write current books dictionary to books.csv."""
        path = os.path.join(self.data_dir, "books.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["book_id", "title", "author", "genre",
                          "year", "total_copies", "available_copies"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for book in self.books.values():
                writer.writerow({
                    "book_id": book.book_id,
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "year": book.year,
                    "total_copies": book.total_copies,
                    "available_copies": book.available_copies,
                })

    def _save_members(self):
        """Write current members dictionary to members.csv."""
        path = os.path.join(self.data_dir, "members.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["member_id", "name", "email",
                          "join_date", "borrowed_books"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for member in self.members.values():
                writer.writerow({
                    "member_id": member.member_id,
                    "name": member.name,
                    "email": member.email,
                    "join_date": member.join_date,
                    "borrowed_books": "|".join(member.borrowed_books),
                })

    def _save_loans(self):
        """Write current loans dictionary to loans.csv."""
        path = os.path.join(self.data_dir, "loans.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["loan_id", "member_id", "book_id",
                          "loan_date", "due_date", "return_date", "is_active"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for loan in self.loans.values():
                writer.writerow({
                    "loan_id": loan.loan_id,
                    "member_id": loan.member_id,
                    "book_id": loan.book_id,
                    "loan_date": loan.loan_date,
                    "due_date": loan.due_date,
                    "return_date": loan.return_date if loan.return_date else "",
                    "is_active": loan.is_active,
                })

    # ------------------------------------------------------------------ #
    #  BOOK OPERATIONS                                                      #
    # ------------------------------------------------------------------ #

    def add_book(self, book_id, title, author, genre, year, copies=1):
        """
        Add a new book to the library catalogue.

        Args:
            book_id (str): Unique book identifier.
            title (str): Book title.
            author (str): Author name.
            genre (str): Genre category.
            year (int): Publication year.
            copies (int): Number of copies. Defaults to 1.

        Returns:
            bool: True if added, False if ID already exists.
        """
        if book_id in self.books:
            print(f"Error: Book ID '{book_id}' already exists.")
            return False
        self.books[book_id] = Book(book_id, title, author, genre, year, copies)
        print(f"Book '{title}' added to catalogue.")
        return True

    def search_books(self, query):
        """
        Search books by title, author, or genre (case-insensitive).

        Args:
            query (str): Search term.

        Returns:
            list: List of matching Book objects.
        """
        query_lower = query.lower()
        results = [
            book for book in self.books.values()
            if query_lower in book.title.lower()
            or query_lower in book.author.lower()
            or query_lower in book.genre.lower()
        ]
        return results

    def list_all_books(self):
        """Print all books in the catalogue."""
        if not self.books:
            print("The catalogue is empty.")
            return
        print(f"\n{'='*60}")
        print(f"  {self.name} — Book Catalogue ({len(self.books)} titles)")
        print(f"{'='*60}")
        for book in self.books.values():
            print(book)
        print(f"{'='*60}\n")

    # ------------------------------------------------------------------ #
    #  MEMBER OPERATIONS                                                    #
    # ------------------------------------------------------------------ #

    def register_member(self, member_id, name, email):
        """
        Register a new library member.

        Args:
            member_id (str): Unique membership number.
            name (str): Member's full name.
            email (str): Member's email address.

        Returns:
            bool: True if registered, False if ID already taken.
        """
        if member_id in self.members:
            print(f"Error: Member ID '{member_id}' already exists.")
            return False
        self.members[member_id] = Member(member_id, name, email)
        print(f"Member '{name}' registered successfully.")
        return True

    def find_member(self, member_id):
        """
        Retrieve a member by their ID.

        Args:
            member_id (str): Membership number to look up.

        Returns:
            Member or None: The Member object, or None if not found.
        """
        return self.members.get(member_id)

    def list_all_members(self):
        """Print all registered members."""
        if not self.members:
            print("No members registered.")
            return
        print(f"\n{'='*60}")
        print(f"  Registered Members ({len(self.members)})")
        print(f"{'='*60}")
        for member in self.members.values():
            print(member)
        print(f"{'='*60}\n")

    # ------------------------------------------------------------------ #
    #  LOAN OPERATIONS                                                      #
    # ------------------------------------------------------------------ #

    def checkout_book(self, member_id, book_id):
        """
        Process a book loan for a member.

        Args:
            member_id (str): ID of the borrowing member.
            book_id (str): ID of the book to borrow.

        Returns:
            bool: True if checkout succeeded, False otherwise.
        """
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member:
            print(f"Error: Member '{member_id}' not found.")
            return False
        if not book:
            print(f"Error: Book '{book_id}' not found in catalogue.")
            return False
        if not book.is_available():
            print(f"Error: No copies of '{book.title}' currently available.")
            return False

        if not member.borrow_book(book_id):
            print(
                f"Error: Member '{member.name}' cannot borrow more books "
                f"(limit: {member.MAX_LOANS}) or already has this book."
            )
            return False

        book.check_out()
        loan_id = f"L{len(self.loans) + 1:04d}"
        new_loan = Loan(loan_id, member_id, book_id)
        self.loans[loan_id] = new_loan
        print(
            f"Checkout successful! '{book.title}' lent to {member.name}. "
            f"Due: {new_loan.due_date}"
        )
        return True

    def return_book(self, member_id, book_id):
        """
        Process the return of a borrowed book.

        Args:
            member_id (str): ID of the returning member.
            book_id (str): ID of the book being returned.

        Returns:
            bool: True if return succeeded, False otherwise.
        """
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member:
            print(f"Error: Member '{member_id}' not found.")
            return False
        if not book:
            print(f"Error: Book '{book_id}' not found.")
            return False
        if not member.return_book(book_id):
            print(f"Error: Member '{member.name}' does not have '{book.title}' on loan.")
            return False

        book.return_copy()

        # Close the active loan record
        for loan in self.loans.values():
            if loan.member_id == member_id and loan.book_id == book_id and loan.is_active:
                loan.close_loan()
                if loan.is_overdue():
                    print(f"Note: This book was overdue by {loan.days_overdue()} days.")
                break

        print(f"Return successful! '{book.title}' returned by {member.name}.")
        return True

    def list_overdue_loans(self):
        """Print all active loans that are past their due date."""
        overdue = [loan for loan in self.loans.values() if loan.is_overdue()]
        if not overdue:
            print("No overdue loans.")
            return
        print(f"\n{'='*60}")
        print(f"  OVERDUE LOANS ({len(overdue)})")
        print(f"{'='*60}")
        for loan in overdue:
            print(loan)
        print(f"{'='*60}\n")
