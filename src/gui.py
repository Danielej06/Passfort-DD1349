import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from crypto.vault import load_vault, save_vault, vault_exists, load_urls, update_vault, create_vault
from crypto.masterpassword import verify_master_password, create_master_password
from passwordstrength import password_strength
from password_generator import strong_password_generator
from session_manager import SessionManager

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
        
        self.style.configure("Generate.TButton", font=("Segoe UI", 10, "bold"), background="#2ecc71", foreground="white", padding=4, borderwidth=0)
        self.style.map("Generate.TButton", background=[("active", "#27ae60")])
        
        self.master_password = None
        self.vault_data = {}

        self.session_manager = SessionManager()
        self.root.bind("<Any-KeyPress>", self.reset_timer)
        self.root.bind("<Any-Button>", self.reset_timer)
        self.root.bind("<Any-Motion>", self.reset_timer)
        self.check_session()

        self.show_login_screen()

    def reset_timer(self, event=None):
        if self.session_manager.started:
            self.session_manager.reset_time()

    def check_session(self):
        if self.session_manager.started and self.session_manager.session_state_expiry():
            self.master_password = None
            self.show_login_screen()
            messagebox.showwarning("Session Expired", "You have been logged out due to inactivity.")
        self.root.after(1000, self.check_session)

    def clear_screen(self):
        """Utility to clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        
        ttk.Label(self.root, text="Welcome to Passfort", style="Header.TLabel").pack(pady=30)
        
        if not vault_exists():
            ttk.Label(self.root, text="Create your master password:").pack(pady=5)
            self.is_creating = True
        else:
            ttk.Label(self.root, text="Enter your master password:").pack(pady=5)
            self.is_creating = False
            
        pass_frame = ttk.Frame(self.root)
        pass_frame.pack(pady=10)
        self.password_entry = ttk.Entry(pass_frame, show="*", font=("Segoe UI", 12), width=25)
        self.password_entry.pack(side=tk.LEFT)
        
        toggle_btn = ttk.Button(pass_frame, text="Show", width=5)
        toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        toggle_btn.bind("<ButtonPress-1>", lambda e: self.password_entry.config(show=""))
        toggle_btn.bind("<ButtonRelease-1>", lambda e: self.password_entry.config(show="*"))
        
        self.password_entry.bind('<Return>', self.login)
        
        btn_text = "Create Vault" if self.is_creating else "Login"
        ttk.Button(self.root, text=btn_text, command=self.login).pack(pady=20)

    def login(self, event=None):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            return
            
        ## Is a boolean to check if vault exists and what the user is doing right now

        ## If there is no vault and the user is currently creating a mass pass.
        if self.is_creating:
            ## Push entered password in gui as master password into newly created vault.
            create_master_password(password)
            create_vault()
            self.master_password = password
            self.session_manager.session_started()
            messagebox.showinfo("Success", "Master password and vault created!")
            self.show_main_menu()
        else:
            ## check master password true.
            if verify_master_password(password):
                self.master_password = password
                self.session_manager.session_started()
                self.show_main_menu()
            else:
                ## if an error occurs or password is wrong.
                messagebox.showerror("Error", "Wrong master password or corrupted vault file.")

    def show_main_menu(self):
        self.clear_screen()
        ttk.Label(self.root, text="Main Menu", style="Header.TLabel").pack(pady=30)
        ## All the visuals for the buttons.

        ttk.Button(self.root, text="Add New Credentials", command=self.show_add_credentials, width=25).pack(pady=10)
        ttk.Button(self.root, text="View Saved Credentials", command=self.show_view_credentials, width=25).pack(pady=10)
        ttk.Button(self.root, text="Delete Vault & Exit", command=self.delete_vault_and_exit, width=25).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit, width=25).pack(pady=10)

    ## Function to delete the db files, which erases all passwords and 
    def delete_vault_and_exit(self):
        if messagebox.askyesno("Delete Vault", "Are you sure you want to delete your entire vault? This action cannot be undone."):
            # Close connections to the databases to ensure they can be safely removed, especially on Windows
            import crypto.vault
            import crypto.masterpassword
            try:
                crypto.vault.con.close()
            except Exception:
                pass
            try:
                crypto.masterpassword.con.close()
            except Exception:
                pass
                
                ## remove db files
            if os.path.exists("data.db"):
                os.remove("data.db")
            if os.path.exists("password.db"):
                os.remove("password.db")
            messagebox.showinfo("Success", "Vault deleted successfully. The application will now exit.")
            self.root.quit()

    ## Add credentials button
    def show_add_credentials(self):
        self.clear_screen()
        ttk.Label(self.root, text="Add Credentials", style="Header.TLabel").pack(pady=20)
        
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10, padx=40, fill=tk.X)
        
        ttk.Label(form_frame, text="URL:").pack(anchor=tk.W)
        url_entry = ttk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        url_entry.pack(pady=(0, 10), fill=tk.X)
        
        ttk.Label(form_frame, text="Username:").pack(anchor=tk.W)
        username_entry = ttk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        username_entry.pack(pady=(0, 10), fill=tk.X)
        
        ttk.Label(form_frame, text="Password:").pack(anchor=tk.W)
        # Hide the password input with asterisks
        pass_frame = ttk.Frame(form_frame)
        pass_frame.pack(pady=(0, 2), fill=tk.X)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(pass_frame, show="*", textvariable=password_var, font=("Segoe UI", 11), width=30)
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        toggle_btn = ttk.Button(pass_frame, text="Show", width=5)
        toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        toggle_btn.bind("<ButtonPress-1>", lambda e: password_entry.config(show=""))
        toggle_btn.bind("<ButtonRelease-1>", lambda e: password_entry.config(show="*"))
        
        ## Generate password button.
        def generate_pwd():
            pwd = strong_password_generator()
            password_var.set(pwd)
            
        generate_btn = ttk.Button(form_frame, text="Generate Secure Password", command=generate_pwd, style="Generate.TButton")
        generate_btn.pack(pady=(5, 10))
        
        strength_label = ttk.Label(form_frame, text="", font=("Segoe UI", 9, "bold"))
        strength_label.pack(anchor=tk.CENTER, pady=(0, 2))
        
        tips_label = ttk.Label(form_frame, text="", font=("Segoe UI", 9), foreground="#7f8c8d", wraplength=300, justify=tk.CENTER)
        tips_label.pack(anchor=tk.CENTER, pady=(0, 10))
        
        ## Password Strength
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
        
        def save():
            url = url_entry.get()
            username = username_entry.get()
            pwd = password_var.get()
            
            if not url or not username or not pwd:
                messagebox.showerror("Error", "All fields are required")
                return
                
            entry = {"url": url, "username": username, "password": pwd}
            if not vault_exists():
                create_vault()
            save_vault(entry, self.master_password)
            messagebox.showinfo("Success", "Credentials saved successfully!")
            self.show_main_menu()
            
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=self.show_main_menu, width=15).pack(side=tk.LEFT, padx=5)

    def show_view_credentials(self):
        self.clear_screen()
        ttk.Label(self.root, text="Saved Credentials", style="Header.TLabel").pack(pady=15)
        
        urls = load_urls()
        ## If no credentials are saved
        if not urls:
            ttk.Label(self.root, text="No credentials saved yet.").pack(pady=20)
            ttk.Button(self.root, text="Back", command=self.show_main_menu).pack()
            return

        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)

        # Adding a modern scrollbar attached to the listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ## The big box where all the credentials can be viewed
        
        listbox = tk.Listbox(list_frame, width=40, yscrollcommand=scrollbar.set, font=("Segoe UI", 11), 
                             bg="#ffffff", fg="#2c3e50", selectbackground="#3498db", selectforeground="white", 
                             relief="flat", highlightthickness=1, highlightcolor="#3498db", highlightbackground="#cccccc")
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for u in urls:
            listbox.insert(tk.END, f"{u[0]} ({u[1]})")
            
        def view_selected(event=None):
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a credential first.")
                return
            choice = selection[0] + 1
            try:
                cred = load_vault(self.master_password, choice)
                self.show_credential_details(choice, cred)
            except Exception:
                ## In the case an error occurs.
                messagebox.showerror("Error", "Could not load credential.")

        listbox.bind('<Double-1>', view_selected)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="View/Edit Selected", command=view_selected, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Back", command=self.show_main_menu, width=20).pack(pady=5)

    def show_credential_details(self, choice, cred, reveal=False, message=""):
        self.clear_screen()
        ttk.Label(self.root, text=cred.get('url'), style="Header.TLabel").pack(pady=20)
        
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
            self.prompt_master_password(choice, cred, "reveal")
                
        def change_password():
            self.prompt_master_password(choice, cred, "change")
            
        def copy_password():
            self.root.clipboard_clear()
            self.root.clipboard_append(cred.get('password'))
            self.show_credential_details(choice, cred, reveal=reveal, message="Password copied to clipboard!")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        if not reveal:
            ttk.Button(button_frame, text="Show Password", command=reveal_password, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Copy Password", command=copy_password, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Change Password", command=change_password, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Back", command=self.show_view_credentials, width=20).pack(pady=5)

    def prompt_master_password(self, choice, cred, action):
        self.clear_screen()
        ttk.Label(self.root, text="Authentication Required", style="Header.TLabel").pack(pady=20)
        ttk.Label(self.root, text=f"Enter master password for {cred.get('url')}:").pack(pady=5)
        
        pass_frame = ttk.Frame(self.root)
        pass_frame.pack(pady=10)
        password_entry = ttk.Entry(pass_frame, show="*", font=("Segoe UI", 12), width=25)
        password_entry.pack(side=tk.LEFT)
        
        toggle_btn = ttk.Button(pass_frame, text="Show", width=5)
        toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        toggle_btn.bind("<ButtonPress-1>", lambda e: password_entry.config(show=""))
        toggle_btn.bind("<ButtonRelease-1>", lambda e: password_entry.config(show="*"))
        
        password_entry.focus()
        
        error_label = ttk.Label(self.root, text="", foreground="red")
        error_label.pack(pady=5)
        
        def submit(event=None):
            entered_pass = password_entry.get()
            if entered_pass == self.master_password:
                if action == "reveal":
                    self.show_credential_details(choice, cred, reveal=True)
                elif action == "change":
                    self.prompt_new_password(choice, cred)
            else:
                error_label.config(text="Incorrect master password.")
                
        password_entry.bind('<Return>', submit)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Submit", command=submit, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=lambda: self.show_credential_details(choice, cred), width=15).pack(side=tk.LEFT, padx=5)

    def prompt_new_password(self, choice, cred):
        self.clear_screen()
        ttk.Label(self.root, text="Change Password", style="Header.TLabel").pack(pady=20)
        ttk.Label(self.root, text=f"Enter new password for {cred.get('url')}:").pack(pady=5)
        
        pass_frame = ttk.Frame(self.root)
        pass_frame.pack(pady=(10, 2))
        password_var = tk.StringVar()
        password_entry = ttk.Entry(pass_frame, show="*", textvariable=password_var, font=("Segoe UI", 12), width=25)
        password_entry.pack(side=tk.LEFT)
        
        toggle_btn = ttk.Button(pass_frame, text="Show", width=5)
        toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        toggle_btn.bind("<ButtonPress-1>", lambda e: password_entry.config(show=""))
        toggle_btn.bind("<ButtonRelease-1>", lambda e: password_entry.config(show="*"))
        
        password_entry.focus()
        
        def generate_pwd():
            pwd = strong_password_generator()
            password_var.set(pwd)
            password_entry.config(show="")  # Reveal the generated password
            
        generate_btn = ttk.Button(self.root, text="Generate Secure Password", command=generate_pwd, style="Generate.TButton")
        generate_btn.pack(pady=(5, 10))
        
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
                cred["password"] = new_pass
                update_vault(cred, self.master_password, choice)
                self.show_credential_details(choice, cred, message="Password changed successfully!")
            else:
                error_label.config(text="Password cannot be empty.")
                
        password_entry.bind('<Return>', submit)
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=submit, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=lambda: self.show_credential_details(choice, cred), width=15).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()