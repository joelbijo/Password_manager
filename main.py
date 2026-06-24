import json
import os
from getpass import getpass
import string
import secrets  # better than random for security


class PasswordManager:
    def __init__(self):
        self.passwords = {}
        self.load_data()

    def load_data(self):
        if os.path.exists("passwords.json"):
            with open("passwords.json", "r", encoding="utf-8") as json_file:
                try:
                    self.passwords = json.load(json_file)
                except json.JSONDecodeError:
                    self.passwords = {}

    def save_data(self):
        with open("passwords.json", "w", encoding="utf-8") as f:
            json.dump(self.passwords, f, indent=4)

    def show(self, site, data):
        print("-" * 20)
        print(f"Website: {site}")
        print(f"Username: {data['username']}")
        print(f"Password: {data['password']}")

    @staticmethod
    def generate_password(length):
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice(string.punctuation),
        ]
        characters = string.ascii_letters + string.digits + string.punctuation
        password.extend(secrets.choice(characters) for _ in range(length - 4))
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    @staticmethod
    def check_password_strength(password):
        score = 0
        issues = []

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

        if any(c in string.punctuation for c in password):
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

    def get_password(self, prompt="Add password: "):
        while True:
            print("\n1. Enter password manually")
            print("2. Generate random password")

            try:
                method = int(input("Enter choice: "))
            except ValueError:
                print("Please enter a number!")
                continue

            if method == 1:
                password = getpass(prompt)

            elif method == 2:
                try:
                    length = int(input("Password length: "))
                except ValueError:
                    print("Please enter a valid number!")
                    continue

                if length < 8:
                    print("Password length should be at least 8.")
                    continue

                password = self.generate_password(length)

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
                        password = self.generate_password(length)

                    else:
                        print("Invalid choice!")

            else:
                print("Invalid choice!")
                continue

            strength, issues = self.check_password_strength(password)

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

    def add_account(self):
        website = input("\nAdd website: ").lower()
        username = input("Add username: ")
        password = self.get_password()

        self.passwords[website] = {
            "username": username,
            "password": password,
        }

        self.save_data()
        print("Account added successfully!")

    def view_accounts(self):
        if not self.passwords:
            print("No accounts stored yet.")
            return

        for site, data in self.passwords.items():
            self.show(site, data)
            print("-" * 20)

    def search_account(self):
        if not self.passwords:
            print("No accounts stored yet.")
            return

        website = input("Enter website to search: ").lower()
        found = False

        for site, data in self.passwords.items():
            if website in site.lower():
                self.show(site, data)
                found = True

        if not found:
            print("No matching websites found!")

    def update_account(self):
        if not self.passwords:
            print("No accounts stored yet.")
            return

        website = input("Enter website to update: ").lower()

        if website not in self.passwords:
            print("Website not found!")
            return

        print("\nCurrent details:")
        print("Username:", self.passwords[website]["username"])
        print("Password: [hidden]")

        show_password = input("Show current password? (y/n): ").strip().lower()

        if show_password == "y":
            print("Password:", self.passwords[website]["password"])

        print("\nWhat do you want to update?")
        print("1. Username")
        print("2. Password")
        print("3. Both\n")

        try:
            ch = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input!")
            return

        updated = False

        if ch == 1:
            new_username = input("Enter new username: ")
            self.passwords[website]["username"] = new_username
            updated = True

        elif ch == 2:
            new_password = self.get_password("Enter new password: ")
            self.passwords[website]["password"] = new_password
            updated = True

        elif ch == 3:
            new_username = input("Enter new username: ")
            new_password = self.get_password("Enter new password: ")

            self.passwords[website]["username"] = new_username
            self.passwords[website]["password"] = new_password
            updated = True

        else:
            print("Invalid choice!")

        if updated:
            self.save_data()
            print("Updated successfully!")

    def delete_account(self):
        if not self.passwords:
            print("No accounts stored yet.")
            return

        print(
            "\nBe sure, you want to delete the account, you won't get the details back!\n"
        )

        website = input("Enter website to delete: ").lower()

        if website not in self.passwords:
            print("Website not found!")
            return

        confirm = (
            input(f"Are you sure you want to delete '{website}'? (y/n): ")
            .strip()
            .lower()
        )

        if confirm == "y":
            del self.passwords[website]
            self.save_data()
            print("Deleted successfully!")

        else:
            print("Deletion cancelled.")

    def menu(self):
        while True:
            print("\n1. Add account")
            print("2. View all accounts")
            print("3. Search account")
            print("4. Update account")
            print("5. Delete account")
            print("6. Exit")

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("Please enter a number!")
                continue

            if choice == 1:
                self.add_account()

            elif choice == 2:
                self.view_accounts()

            elif choice == 3:
                self.search_account()

            elif choice == 4:
                self.update_account()

            elif choice == 5:
                self.delete_account()

            elif choice == 6:
                print("Exiting...\n")
                break

            else:
                print("Invalid choice!\n")


if __name__ == "__main__":
    manager = PasswordManager()
    manager.menu()
