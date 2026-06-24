"""
main.py
-------
Entry point for the City Library Management System.
Provides an interactive, menu-driven command-line interface.

Run:
    python main.py

Author: Student Submission
Course: B100 Introduction to Computer Programming with Python
"""

from library import Library


def print_menu():
    """Display the main menu options to the user."""
    print("\n" + "=" * 45)
    print("     CITY LIBRARY MANAGEMENT SYSTEM")
    print("=" * 45)
    print("  1. List all books")
    print("  2. Search for a book")
    print("  3. Add a new book")
    print("  4. List all members")
    print("  5. Register a new member")
    print("  6. Check out a book")
    print("  7. Return a book")
    print("  8. View overdue loans")
    print("  9. Save data")
    print("  0. Exit")
    print("=" * 45)


def handle_add_book(lib):
    """Prompt the user for book details and add to the catalogue."""
    print("\n--- Add New Book ---")
    book_id = input("Enter Book ID (e.g. B001): ").strip()
    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()
    genre = input("Enter Genre: ").strip()

    # Validate year input with exception handling
    while True:
        try:
            year = int(input("Enter Publication Year: ").strip())
            break
        except ValueError:
            print("Invalid year. Please enter a 4-digit number.")

    # Validate copies input with exception handling
    while True:
        try:
            copies = int(input("Number of Copies (default 1): ").strip() or "1")
            if copies < 1:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive whole number.")

    lib.add_book(book_id, title, author, genre, year, copies)


def handle_search(lib):
    """Prompt the user for a search query and display results."""
    print("\n--- Search Books ---")
    query = input("Enter title, author, or genre to search: ").strip()
    if not query:
        print("Search query cannot be empty.")
        return
    results = lib.search_books(query)
    if results:
        print(f"\n{len(results)} result(s) found:")
        for book in results:
            print(book)
    else:
        print("No matching books found.")


def handle_register_member(lib):
    """Prompt for member details and register in the system."""
    print("\n--- Register New Member ---")
    member_id = input("Enter Member ID (e.g. M001): ").strip()
    name = input("Enter Full Name: ").strip()
    email = input("Enter Email Address: ").strip()
    lib.register_member(member_id, name, email)


def handle_checkout(lib):
    """Process a book checkout for a member."""
    print("\n--- Check Out a Book ---")
    member_id = input("Enter Member ID: ").strip()
    book_id = input("Enter Book ID: ").strip()
    lib.checkout_book(member_id, book_id)


def handle_return(lib):
    """Process a book return from a member."""
    print("\n--- Return a Book ---")
    member_id = input("Enter Member ID: ").strip()
    book_id = input("Enter Book ID: ").strip()
    lib.return_book(member_id, book_id)


def main():
    """
    Main program loop.
    Instantiates the Library and runs the interactive menu.
    """
    print("\nWelcome to the City Library Management System")
    lib = Library(name="City Library", data_dir="data")

    while True:
        print_menu()
        choice = input("Select an option (0-9): ").strip()

        if choice == "1":
            lib.list_all_books()
        elif choice == "2":
            handle_search(lib)
        elif choice == "3":
            handle_add_book(lib)
        elif choice == "4":
            lib.list_all_members()
        elif choice == "5":
            handle_register_member(lib)
        elif choice == "6":
            handle_checkout(lib)
        elif choice == "7":
            handle_return(lib)
        elif choice == "8":
            lib.list_overdue_loans()
        elif choice == "9":
            lib.save_all_data()
        elif choice == "0":
            lib.save_all_data()
            print("\nThank you for using the City Library System. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 0 and 9.")


if __name__ == "__main__":
    main()
