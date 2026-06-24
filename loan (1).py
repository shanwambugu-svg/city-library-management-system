"""
loan.py
-------
Defines the Loan class for the City Library Management System.
A Loan records the borrowing transaction between a Member and a Book.

Author: Student Submission
Course: B100 Introduction to Computer Programming with Python
"""

from datetime import date, timedelta


class Loan:
    """Represents a single book loan transaction."""

    LOAN_PERIOD_DAYS = 14  # Standard two-week loan period

    def __init__(self, loan_id, member_id, book_id, loan_date=None):
        """
        Initialise a Loan instance.

        Args:
            loan_id (str): Unique identifier for this loan.
            member_id (str): ID of the borrowing member.
            book_id (str): ID of the book being lent.
            loan_date (str, optional): ISO date of loan (YYYY-MM-DD).
                                       Defaults to today.
        """
        self.loan_id = loan_id
        self.member_id = member_id
        self.book_id = book_id
        self.loan_date = loan_date if loan_date else str(date.today())
        self.due_date = str(
            date.fromisoformat(self.loan_date) + timedelta(days=self.LOAN_PERIOD_DAYS)
        )
        self.return_date = None  # Populated when book is returned
        self.is_active = True

    def close_loan(self):
        """
        Mark the loan as returned by setting the return date to today
        and flagging it inactive.
        """
        self.return_date = str(date.today())
        self.is_active = False

    def is_overdue(self):
        """
        Determine whether the loan is overdue.

        Returns:
            bool: True if active and past the due date.
        """
        if not self.is_active:
            return False
        return date.today() > date.fromisoformat(self.due_date)

    def days_overdue(self):
        """
        Calculate the number of days overdue.

        Returns:
            int: Days overdue (0 if not overdue or already returned).
        """
        if not self.is_overdue():
            return 0
        delta = date.today() - date.fromisoformat(self.due_date)
        return delta.days

    def get_details(self):
        """
        Return a formatted summary of this loan.

        Returns:
            str: Human-readable loan record.
        """
        status = "Active" if self.is_active else f"Returned: {self.return_date}"
        overdue_note = f" *** OVERDUE by {self.days_overdue()} days ***" if self.is_overdue() else ""
        return (
            f"Loan [{self.loan_id}] | Member: {self.member_id} | "
            f"Book: {self.book_id} | Lent: {self.loan_date} | "
            f"Due: {self.due_date} | Status: {status}{overdue_note}"
        )

    def __str__(self):
        return self.get_details()
