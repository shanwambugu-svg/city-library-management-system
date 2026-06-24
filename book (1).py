"""
book.py
-------
Defines the Book class for the City Library Management System.
Each Book object represents a physical book in the library collection.

Author: Student Submission
Course: B100 Introduction to Computer Programming with Python
"""


class Book:
    """Represents a book in the library collection."""

    def __init__(self, book_id, title, author, genre, year, copies=1):
        """
        Initialise a Book instance.

        Args:
            book_id (str): Unique identifier for the book.
            title (str): Title of the book.
            author (str): Author's full name.
            genre (str): Genre or subject category.
            year (int): Publication year.
            copies (int): Total number of copies held. Defaults to 1.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.total_copies = copies
        self.available_copies = copies

    def check_out(self):
        """
        Reduce available copies by one when a book is borrowed.

        Returns:
            bool: True if successful, False if no copies available.
        """
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def return_copy(self):
        """
        Increase available copies by one when a book is returned.

        Returns:
            bool: True if successful, False if all copies already in.
        """
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False

    def is_available(self):
        """
        Check whether at least one copy is available.

        Returns:
            bool: True if one or more copies available.
        """
        return self.available_copies > 0

    def get_details(self):
        """
        Return a formatted string with book details.

        Returns:
            str: Human-readable summary of the book.
        """
        status = "Available" if self.is_available() else "All copies checked out"
        return (
            f"[{self.book_id}] '{self.title}' by {self.author} "
            f"({self.year}) | Genre: {self.genre} | "
            f"Copies: {self.available_copies}/{self.total_copies} | {status}"
        )

    def __str__(self):
        return self.get_details()
