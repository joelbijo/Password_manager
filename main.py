
import json
import os

passwords={}
if os.path.exists("passwords.json"):
    with open("passwords.json","r",encoding="utf-8") as json_file:
        try:
            passwords = json.load(json_file)
        except json.JSONDecodeError:
            passwords = {}

def save_data():
    with open("passwords.json","w",encoding="utf-8") as f:
        json.dump(passwords,f,indent=4)

def show(site, data):
    print("-" * 20)
    print(f"Website: {site}")
    print(f"Username: {data['username']}")
    print(f"Password: {data['password']}")

def menu():
    while True:
        print("\n1. Add account\n2. View all accounts\n3. Search account\n4. Update account\n5. Delete account\n6. Exit")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Please enter a number!")
            continue

        if choice==1:
            website=input("\nAdd website: ").lower()
            username=input("Add username: ")
            password=input("Add password:")
            passwords[website]={
                "username":username,
                "password":password
            }
            save_data()

        elif choice==2:
            if not passwords:
                print("No accounts stored yet.")
                continue

            for site,data in passwords.items():
                show(site,data)
                print("-" * 20)
        
        elif choice==3:
            if not passwords:
                print("No accounts stored yet.")
                continue

            website=input("Enter website to search: ").lower()
            found=False
            for site,data in passwords.items():
                if website in site.lower():
                    show(site,data)
                    found=True
            if not found: 
                print("No matching websites found!")
        
        elif choice==4:
            if not passwords:
                print("No accounts stored yet.")
                continue

            website=input("Enter website to update: ").lower()

            if website in passwords:
                print("\nCurrent details:")
                print("Username:", passwords[website]["username"])
                print("Password:", passwords[website]["password"])

                print("\nWhat do you want to update?")
                print("1. Username\n2. Password\n3. Both\n")
                try:
                    ch=int(input("Enter choice: "))
                except ValueError:
                    print("Invalid input!")
                    continue

                updated=False

                if ch==1:
                    new_username=input("Enter new username: ")
                    passwords[website]["username"]=new_username
                    updated=True
                elif ch==2:
                    new_password=input("Enter new password: ")
                    passwords[website]["password"]=new_password
                    updated=True
                elif ch==3:
                    new_username=input("Enter new username: ")
                    new_password=input("Enter new password: ")
                    passwords[website]["username"]=new_username
                    passwords[website]["password"]=new_password
                    updated=True
                else:
                    print("Invalid choice!")

                if updated: 
                    save_data()
                    print("Updated successfully!")
            else:
                print("Website not found!")
    

        elif choice==5:
            if not passwords:
                print("No accounts stored yet.")
                continue

            print("\nBe sure, you want to delete the account, you wont get the details back!\n")
            website=input("Enter website to delete: ").lower()

            if website in passwords:
                del passwords[website]

                save_data()
                print("Deleted successfully!")
            else:
                print("Website not found!")
            
        elif choice==6:
            print("Exiting...\n")
            break

        else:
            print("Invalid choice!\n")
menu()


