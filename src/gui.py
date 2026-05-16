import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from crypto.vault import load_vault, save_vault
from passwordstrength import password_strength

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Passfort Password Manager")
        self.root.geometry("450x500")
        
        # Initialize themed Tkinter for a more modern appearance
        self.style = ttk.Style()
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
            
        # Define color palette and styles
        bg_color = "#f4f7f9"
        self.root.configure(bg=bg_color)
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground="#2c3e50", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#1a252f")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), background="#3498db", foreground="white", padding=6, borderwidth=0)
        self.style.map("TButton", background=[("active", "#2980b9")])
        
        self.master_password = None
        self.vault_data = {}

        self.show_login_screen()

    def clear_screen(self):
        """Utility to clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        
        ttk.Label(self.root, text="Welcome to Passfort", style="Header.TLabel").pack(pady=30)
        
        if not os.path.exists("data.json"):
            ttk.Label(self.root, text="Create your master password:").pack(pady=5)
        else:
            ttk.Label(self.root, text="Enter your master password:").pack(pady=5)
            
        self.password_entry = ttk.Entry(self.root, show="*", font=("Segoe UI", 12), width=25)
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<Return>', self.login)
        
        ttk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self, event=None):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            return
            
        try:
            self.vault_data = load_vault(password)
            self.master_password = password
            self.show_main_menu()
        except Exception:
            messagebox.showerror("Error", "Wrong master password or corrupted vault file.")

    def show_main_menu(self):
        self.clear_screen()
        ttk.Label(self.root, text="Main Menu", style="Header.TLabel").pack(pady=30)
        
        ttk.Button(self.root, text="Add New Credentials", command=self.show_add_credentials, width=25).pack(pady=10)
        ttk.Button(self.root, text="View Saved Credentials", command=self.show_view_credentials, width=25).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit, width=25).pack(pady=10)

    def show_add_credentials(self):
        self.clear_screen()
        ttk.Label(self.root, text="Add Credentials", style="Header.TLabel").pack(pady=20)
        
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10, padx=40, fill=tk.X)
        
        ttk.Label(form_frame, text="Title:").pack(anchor=tk.W)
        title_entry = ttk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        title_entry.pack(pady=(0, 10), fill=tk.X)
        
        ttk.Label(form_frame, text="Username:").pack(anchor=tk.W)
        username_entry = ttk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        username_entry.pack(pady=(0, 10), fill=tk.X)
        
        ttk.Label(form_frame, text="Password:").pack(anchor=tk.W)
        # Hide the password input with asterisks
        password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, show="*", textvariable=password_var, font=("Segoe UI", 11), width=30)
        password_entry.pack(pady=(0, 2), fill=tk.X)
        
        strength_label = ttk.Label(form_frame, text="", font=("Segoe UI", 9, "bold"))
        strength_label.pack(anchor=tk.W, pady=(0, 2))
        
        tips_label = ttk.Label(form_frame, text="", font=("Segoe UI", 9), foreground="#7f8c8d", wraplength=300)
        tips_label.pack(anchor=tk.W, pady=(0, 10))
        
        def update_strength(*args):
            pwd = password_var.get()
            if not pwd:
                strength_label.config(text="")
                tips_label.config(text="")
                return
                
            strength, tips = password_strength(pwd)
            strength_label.config(text=f"Strength: {strength}")
            
            if strength == "Weak":
                strength_label.config(foreground="red")
            elif strength == "Medium":
                strength_label.config(foreground="orange")
            elif strength == "Strong":
                strength_label.config(foreground="#9ACD32") # Yellow-Green
            else:
                strength_label.config(foreground="green")
                
            if tips:
                tips_label.config(text="Tips:\n- " + "\n- ".join(tips))
            else:
                tips_label.config(text="")
                
        password_var.trace_add("write", update_strength)
        
        ttk.Label(form_frame, text="URL:").pack(anchor=tk.W)
        url_entry = ttk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        url_entry.pack(pady=(0, 15), fill=tk.X)
        
        def save():
            title = title_entry.get()
            if not title:
                messagebox.showerror("Error", "Title is required")
                return
                
            self.vault_data[title] = {
                "username": username_entry.get(),
                "password": password_entry.get(),
                "url": url_entry.get()
            }
            save_vault(self.vault_data, self.master_password)
            messagebox.showinfo("Success", "Credentials saved successfully!")
            self.show_main_menu()
            
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_main_menu, width=15).pack(side=tk.LEFT, padx=5)

    def show_view_credentials(self):
        self.clear_screen()
        ttk.Label(self.root, text="Saved Credentials", style="Header.TLabel").pack(pady=15)
        
        # This smoothly addresses the "null" issue you noted in your `read_credentials.py` file.
        if not self.vault_data:
            ttk.Label(self.root, text="No credentials saved yet.").pack(pady=20)
            ttk.Button(self.root, text="Back", command=self.show_main_menu).pack()
            return

        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)

        # Adding a modern scrollbar attached to the listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, width=40, yscrollcommand=scrollbar.set, font=("Segoe UI", 11), 
                             bg="#ffffff", fg="#2c3e50", selectbackground="#3498db", selectforeground="white", 
                             relief="flat", highlightthickness=1, highlightcolor="#3498db", highlightbackground="#cccccc")
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for title in self.vault_data:
            listbox.insert(tk.END, title)
            
        def view_selected(event=None):
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a credential first.")
                return
            title = listbox.get(selection[0])
            cred = self.vault_data[title]
            self.show_credential_details(title, cred)

        listbox.bind('<Double-1>', view_selected)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="View/Edit Selected", command=view_selected, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Back", command=self.show_main_menu, width=20).pack(pady=5)

    def show_credential_details(self, title, cred, reveal=False, message=""):
        self.clear_screen()
        ttk.Label(self.root, text=title, style="Header.TLabel").pack(pady=20)
        
        if message:
            ttk.Label(self.root, text=message, foreground="green").pack(pady=5)
            
        details_frame = ttk.Frame(self.root)
        details_frame.pack(pady=10, padx=40, fill=tk.X)
        
        ttk.Label(details_frame, text=f"Username: {cred.get('username')}", font=("Segoe UI", 12)).pack(anchor=tk.W, pady=5)
        ttk.Label(details_frame, text=f"URL: {cred.get('url')}", font=("Segoe UI", 12)).pack(anchor=tk.W, pady=5)
        
        if reveal:
            password_str = cred.get('password')
        else:
            password_str = "*" * len(cred.get('password', ''))
            
        pass_frame = ttk.Frame(details_frame)
        pass_frame.pack(anchor=tk.W, pady=5, fill=tk.X)
        ttk.Label(pass_frame, text="Password: ", font=("Segoe UI", 12)).pack(side=tk.LEFT)
        ttk.Label(pass_frame, text=password_str, font=("Segoe UI", 12)).pack(side=tk.LEFT)
        
        def reveal_password():
            self.prompt_master_password(title, cred, "reveal")
                
        def change_password():
            self.prompt_master_password(title, cred, "change")
            
        def copy_password():
            self.root.clipboard_clear()
            self.root.clipboard_append(cred.get('password'))
            self.show_credential_details(title, cred, reveal=reveal, message="Password copied to clipboard!")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        if not reveal:
            ttk.Button(button_frame, text="Show Password", command=reveal_password, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Copy Password", command=copy_password, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Change Password", command=change_password, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Back", command=self.show_view_credentials, width=20).pack(pady=5)

    def prompt_master_password(self, title, cred, action):
        self.clear_screen()
        ttk.Label(self.root, text="Authentication Required", style="Header.TLabel").pack(pady=20)
        ttk.Label(self.root, text=f"Enter master password for {title}:").pack(pady=5)
        
        password_entry = ttk.Entry(self.root, show="*", font=("Segoe UI", 12), width=25)
        password_entry.pack(pady=10)
        password_entry.focus()
        
        error_label = ttk.Label(self.root, text="", foreground="red")
        error_label.pack(pady=5)
        
        def submit(event=None):
            entered_pass = password_entry.get()
            if entered_pass == self.master_password:
                if action == "reveal":
                    self.show_credential_details(title, cred, reveal=True)
                elif action == "change":
                    self.prompt_new_password(title, cred)
            else:
                error_label.config(text="Incorrect master password.")
                
        password_entry.bind('<Return>', submit)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Submit", command=submit, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=lambda: self.show_credential_details(title, cred), width=15).pack(side=tk.LEFT, padx=5)

    def prompt_new_password(self, title, cred):
        self.clear_screen()
        ttk.Label(self.root, text="Change Password", style="Header.TLabel").pack(pady=20)
        ttk.Label(self.root, text=f"Enter new password for {title}:").pack(pady=5)
        
        password_var = tk.StringVar()
        password_entry = ttk.Entry(self.root, show="*", textvariable=password_var, font=("Segoe UI", 12), width=25)
        password_entry.pack(pady=(10, 2))
        password_entry.focus()
        
        strength_label = ttk.Label(self.root, text="", font=("Segoe UI", 9, "bold"))
        strength_label.pack(pady=(0, 2))
        
        tips_label = ttk.Label(self.root, text="", font=("Segoe UI", 9), foreground="#7f8c8d", wraplength=300, justify=tk.CENTER)
        tips_label.pack(pady=(0, 5))
        
        def update_strength(*args):
            pwd = password_var.get()
            if not pwd:
                strength_label.config(text="")
                tips_label.config(text="")
                return
                
            strength, tips = password_strength(pwd)
            strength_label.config(text=f"Strength: {strength}")
            
            if strength == "Weak":
                strength_label.config(foreground="red")
            elif strength == "Medium":
                strength_label.config(foreground="orange")
            elif strength == "Strong":
                strength_label.config(foreground="#9ACD32")
            else:
                strength_label.config(foreground="green")
                
            if tips:
                tips_label.config(text="Tips:\n- " + "\n- ".join(tips))
            else:
                tips_label.config(text="")
                
        password_var.trace_add("write", update_strength)
        
        error_label = ttk.Label(self.root, text="", foreground="red")
        error_label.pack(pady=5)
        
        def submit(event=None):
            new_pass = password_entry.get()
            if new_pass:
                self.vault_data[title]["password"] = new_pass
                cred["password"] = new_pass
                save_vault(self.vault_data, self.master_password)
                self.show_credential_details(title, cred, message="Password changed successfully!")
            else:
                error_label.config(text="Password cannot be empty.")
                
        password_entry.bind('<Return>', submit)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=submit, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=lambda: self.show_credential_details(title, cred), width=15).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()