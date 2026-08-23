import getpass
from vault import add_password, get_password

def main():
    print("=== SECURE LOCAL PASSWORD VAULT ===")
    print("[*] Please set or enter your Master Password to unlock the vault.")
    
    # getpass hides the password typing input in standard terminals
    master_password = getpass.getpass("Master Password: ").strip()
    
    if not master_password:
        print("[-] Master Password cannot be empty. Exiting...")
        return

    while True:
        print("\n=== VAULT MENU ===")
        print("1. Add/Update a Password")
        print("2. Retrieve a Password")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            account = input("Enter account name (e.g., Google, Netflix): ").strip()
            password = input(f"Enter password for {account}: ").strip()
            if account and password:
                add_password(account, password, master_password)
            else:
                print("[-] Account name and password cannot be empty.")
                
        elif choice == "2":
            account = input("Enter the account name to retrieve: ").strip()
            if account:
                password = get_password(account, master_password)
                if password:
                    print(f"[➔] Decrypted Password for {account}: {password}")
            else:
                print("[-] Account name cannot be empty.")
                
        elif choice == "3":
            print("[*] Locking vault. Stay secure!")
            break
        else:
            print("[-] Invalid choice. Please pick 1, 2, or 3.")

if __name__ == "__main__":
    main()
