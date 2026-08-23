import tkinter as tk
from tkinter import messagebox, ttk
from vault import add_password, get_password, generate_strong_password

class PasswordVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Vault 🔐")
        self.root.geometry("480x420")
        self.root.resizable(False, False)
        
        # Configure layout styling colors
        self.bg_color = "#f4f6f9"
        self.primary_color = "#1e293b"
        self.accent_color = "#2563eb"
        
        self.root.configure(bg=self.bg_color)
        self.master_password = ""
        
        # Initialize the Application Interfaces
        self.create_lock_screen()

    def create_lock_screen(self):
        """Builds the initial secure master login overlay."""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=40)
        frame.pack(fill="both", expand=True)
        
        lbl_title = tk.Label(frame, text="VAULT LOCK SCREEN", font=("Arial", 16, "bold"), fg=self.primary_color, bg=self.bg_color)
        lbl_title.pack(pady=(0, 20))
        
        lbl_hint = tk.Label(frame, text="Enter your Master Password to unlock data:", font=("Arial", 10), fg="#64748b", bg=self.bg_color)
        lbl_hint.pack(pady=(0, 5))
        
        self.ent_master = tk.Entry(frame, show="*", font=("Arial", 12), width=30, justify="center")
        self.ent_master.pack(pady=10)
        self.ent_master.focus()
        
        btn_unlock = tk.Button(frame, text="Unlock Vault", font=("Arial", 11, "bold"), fg="white", bg=self.accent_color, padx=15, pady=5, command=self.unlock_vault)
        btn_unlock.pack(pady=20)

    def create_dashboard_screen(self):
        """Builds the main dashboard area for operations."""
        self.clear_window()
        
        # Main wrapper container
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Add Credentials
        tab_add = tk.Frame(notebook, bg=self.bg_color, padx=15, pady=15)
        notebook.add(tab_add, text=" Add Password ")
        
        tk.Label(tab_add, text="Account/Platform Name:", bg=self.bg_color, font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.ent_account = tk.Entry(tab_add, font=("Arial", 11), width=35)
        self.ent_account.pack(fill="x", pady=5)
        
        tk.Label(tab_add, text="Password:", bg=self.bg_color, font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.ent_pass = tk.Entry(tab_add, font=("Arial", 11), width=35)
        self.ent_pass.pack(fill="x", pady=5)
        
        # Inner helper control layout frame
        btn_frame = tk.Frame(tab_add, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=15)
        
        btn_gen = tk.Button(btn_frame, text="⚡ Auto-Generate Strong", font=("Arial", 9), bg="#64748b", fg="white", command=self.populate_generated_password)
        btn_gen.pack(side="left", padx=(0, 10))
        
        btn_save = tk.Button(btn_frame, text="💾 Save Securely", font=("Arial", 9, "bold"), bg="#10b981", fg="white", command=self.save_credential)
        btn_save.pack(side="right")
        
        # Tab 2: Retrieve Credentials
        tab_get = tk.Frame(notebook, bg=self.bg_color, padx=15, pady=15)
        notebook.add(tab_get, text=" Retrieve Password ")
        
        tk.Label(tab_get, text="Target Account to Search:", bg=self.bg_color, font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.ent_search = tk.Entry(tab_get, font=("Arial", 11), width=35)
        self.ent_search.pack(fill="x", pady=5)
        
        btn_fetch = tk.Button(tab_get, text="🔍 Decrypt and View", font=("Arial", 10, "bold"), bg=self.accent_color, fg="white", command=self.fetch_credential)
        btn_fetch.pack(fill="x", pady=15)
        
        self.lbl_result = tk.Label(tab_get, text="", font=("Courier", 12, "bold"), fg="#b91c1c", bg="#fee2e2", pady=10, relief="solid", bd=1)
        
    def unlock_vault(self):
        pwd = self.ent_master.get().strip()
        if not pwd:
            messagebox.showerror("Error", "Master Password entry field cannot be empty.")
            return
        self.master_password = pwd
        self.create_dashboard_screen()

    def populate_generated_password(self):
        generated = generate_strong_password()
        self.ent_pass.delete(0, tk.END)
        self.ent_pass.insert(0, generated)

    def save_credential(self):
        account = self.ent_account.get().strip()
        password = self.ent_pass.get().strip()
        
        if not account or not password:
            messagebox.showerror("Error", "All parameter inputs are required.")
            return
            
        add_password(account, password, self.master_password)
        messagebox.showinfo("Success", f"Credentials encrypted and stored for {account}!")
        self.ent_account.delete(0, tk.END)
        self.ent_pass.delete(0, tk.END)

    def fetch_credential(self):
        account = self.ent_search.get().strip()
        if not account:
            messagebox.showerror("Error", "Please input an account name.")
            return
            
        decrypted = get_password(account, self.master_password)
        if decrypted:
            self.lbl_result.pack(fill="x", pady=10)
            self.lbl_result.config(text=f"Password: {decrypted}", fg="#047857", bg="#d1fae5")
        else:
            self.lbl_result.pack(fill="x", pady=10)
            self.lbl_result.config(text="Access Denied / Not Found", fg="#b91c1c", bg="#fee2e2")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = PasswordVaultApp(app_root)
    app_root.mainloop()
