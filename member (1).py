"""
member.py
---------
Defines the Member class for the City Library Management System.
Each Member object represents a registered library patron.

Author: Student Submission
Course: B100 Introduction to Computer Programming with Python
"""

from datetime import date


class Member:
    """Represents a registered library member (patron)."""

    MAX_LOANS = 5  # Maximum books a member may borrow at once

    def __init__(self, member_id, name, email, join_date=None):
        """
        Initialise a Member instance.

        Args:
            member_id (str): Unique membership number.
            name (str): Full name of the member.
            email (str): Contact email address.
            join_date (str, optional): ISO date string (YYYY-MM-DD).
                                       Defaults to today's date.
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.join_date = join_date if join_date else str(date.today())
        self.borrowed_books = []  # List of book_ids currently on loan

    def borrow_book(self, book_id):
        """
        Record that this member has borrowed a book.

        Args:
            book_id (str): ID of the book being borrowed.

        Returns:
            bool: True if recorded, False if loan limit reached or
                  book already on loan to this member.
        """
        if len(self.borrowed_books) >= self.MAX_LOANS:
            return False
        if book_id in self.borrowed_books:
            return False
        self.borrowed_books.append(book_id)
        return True

    def return_book(self, book_id):
        """
        Remove a book from this member's active loan list.

        Args:
            book_id (str): ID of the book being returned.

        Returns:
            bool: True if removed, False if book was not on loan.
        """
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False

    def get_loan_count(self):
        """
        Return the number of books currently on loan.

        Returns:
            int: Count of active loans.
        """
        return len(self.borrowed_books)

    def get_details(self):
        """
        Return a formatted summary of the member's account.

        Returns:
            str: Human-readable member profile.
        """
        loans = ", ".join(self.borrowed_books) if self.borrowed_books else "None"
        return (
            f"[{self.member_id}] {self.name} | Email: {self.email} | "
            f"Member since: {self.join_date} | "
            f"Books on loan ({self.get_loan_count()}/{self.MAX_LOANS}): {loans}"
        )

    def __str__(self):
        return self.get_details()
