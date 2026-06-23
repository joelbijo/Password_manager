
import json
import os
from getpass import getpass
import string
import random

passwords = {}

if os.path.exists("passwords.json"):
    with open("passwords.json", "r", encoding="utf-8") as json_file:
        try:
            passwords = json.load(json_file)
        except json.JSONDecodeError:
            passwords = {}

def save_data():
    with open("passwords.json", "w", encoding="utf-8") as f:
        json.dump(passwords, f, indent=4)

def show(site, data):
    print("-" * 20)
    print(f"Website: {site}")
    print(f"Username: {data['username']}")
    print(f"Password: {data['password']}")

def generate_password(length):
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password.extend(
        random.choice(characters)
        for _ in range(length - 4)
    )

    random.shuffle(password)

    return "".join(password)

def check_password_strength(password):
    score=0
    issues=[]
    if len(password) >= 8:
        score += 20
    else:
        issues.append("Password should be at least 8 characters long")

    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10

    if any(c.isupper() for c in password):
        score += 15
    else:
        issues.append("Add at least one uppercase letter")

    if any(c.islower() for c in password):
        score += 15
    else:
        issues.append("Add at least one lowercase letter")

    if any(c.isdigit() for c in password):
        score += 15
    else:
        issues.append("Add at least one number")

    if any(c in string.punctuation for c in password): #special char
        score += 15
    else:
        issues.append("Add at least one special character")

    if score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, issues

def get_password(prompt="Add password: "):
    while True:
        print("\n1. Enter password manually")
        print("2. Generate random password")

        try:
            method = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a number!")
            continue

        if method == 1:
            password = getpass(prompt, echo_char="*")

        elif method == 2:
            try:
                length = int(input("Password length: "))
            except ValueError:
                print("Please enter a valid number!")
                continue

            if length < 8:
                print("Password length should be at least 8.")
                continue

            password = generate_password(length)

            while True:
                print("\nGenerated Password:", password)
                print("1. Use this password")
                print("2. Generate another")

                try:
                    choi = int(input("Enter choice: "))
                except ValueError:
                    print("Please enter a number!")
                    continue

                if choi == 1:
                    break
                elif choi == 2:
                    password = generate_password(length)

                else:
                    print("Invalid choice!")

        else:
            print("Invalid choice!")
            continue

        strength, issues = check_password_strength(password)
        print("\nPassword Strength:", strength)

        if issues:
            print("\nSuggestions:")
            for issue in issues:
                print("-", issue)

        if strength == "Weak":
            while True:
                print("\nThis password is weak.")
                print("1. Use this password anyway")
                print("2. Enter a stronger password")

                try:
                    choice = int(input("Enter choice: "))
                except ValueError:
                    print("Please enter a number!")
                    continue

                if choice == 1:
                    break
                elif choice == 2:
                    password = None
                    break
                else:
                    print("Invalid choice!")

            if password is None:
                continue

        while True:
            print("\n1. Continue")
            print("2. Show password")
            print("3. Re-enter password")

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("Please enter a number!")
                continue

            if choice == 1:
                return password

            elif choice == 2:
                print("Password:", password)

            elif choice == 3:
                break
            else:
                print("Invalid choice!")

        if choice == 3:
            continue

def menu():
    while True:
        print("\n1. Add account\n2. View all accounts\n3. Search account")
        print("4. Update account\n5. Delete account\n6. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a number!")
            continue

        if choice == 1:
            website = input("\nAdd website: ").lower()
            username = input("Add username: ")
            password = get_password()

            passwords[website] = {
                "username": username,
                "password": password
            }

            save_data()
            print("Account added successfully!")

        elif choice == 2:
            if not passwords:
                print("No accounts stored yet.")
                continue

            for site, data in passwords.items():
                show(site, data)
                print("-" * 20)

        elif choice == 3:
            if not passwords:
                print("No accounts stored yet.")
                continue

            website = input("Enter website to search: ").lower()
            found = False

            for site, data in passwords.items():
                if website in site.lower():
                    show(site, data)
                    found = True

            if not found:
                print("No matching websites found!")

        elif choice == 4:
            if not passwords:
                print("No accounts stored yet.")
                continue

            website = input("Enter website to update: ").lower()

            if website in passwords:

                print("\nCurrent details:")
                print("Username:", passwords[website]["username"])
                print("Password: [hidden]")

                show_password = input(
                    "Show current password? (y/n): "
                ).strip().lower()

                if show_password == "y":
                    print("Password:", passwords[website]["password"])

                print("\nWhat do you want to update?")
                print("1. Username")
                print("2. Password")
                print("3. Both\n")

                try:
                    ch = int(input("Enter choice: "))
                except ValueError:
                    print("Invalid input!")
                    continue

                updated = False

                if ch == 1:
                    new_username = input("Enter new username: ")
                    passwords[website]["username"] = new_username
                    updated = True

                elif ch == 2:
                    new_password = get_password("Enter new password: ")
                    passwords[website]["password"] = new_password
                    updated = True

                elif ch == 3:
                    new_username = input("Enter new username: ")
                    new_password = get_password("Enter new password: ")

                    passwords[website]["username"] = new_username
                    passwords[website]["password"] = new_password
                    updated = True

                else:
                    print("Invalid choice!")

                if updated:
                    save_data()
                    print("Updated successfully!")

            else:
                print("Website not found!")

        elif choice == 5:
            if not passwords:
                print("No accounts stored yet.")
                continue

            print("\nBe sure, you want to delete the account, you won't get the details back!\n")
            website = input("Enter website to delete: ").lower()

            if website in passwords:
                confirm = input(f"Are you sure you want to delete '{website}'? (y/n): ").strip().lower()
                if confirm == "y":
                    del passwords[website]
                    save_data()
                    print("Deleted successfully!")
                else:
                    print("Deletion cancelled.")

            else:
                print("Website not found!")

        elif choice == 6:
            print("Exiting...\n")
            break

        else:
            print("Invalid choice!\n")

menu()