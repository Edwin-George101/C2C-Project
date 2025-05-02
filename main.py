import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from initialize_db import initialize_database

#Needs to be better formated
# should make better frames and lines

DB_NAME = 'bank.db'
class Bank:
   def __init__(self, root):
       self.root = root
       self.root.title("Banking System")
      
       #main frame
       self.main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
       self.main_frame.pack(fill=tk.BOTH, expand=True)
      
       #title label
       title_label = tk.Label(
           self.main_frame,
           text="banking system", font=("Arial", 18, ), bg="#f0f0f0"
       )
       title_label.pack(pady=(0, 20))
       #create frames
       self.create_acc_frame()
       self.manage_acc_frame()
       #initialize database 
       initialize_database()
      
       #load account 
       self.load_accounts()
   def create_acc_frame(self):
    #create account section!
       frame = tk.LabelFrame(
           self.main_frame,
           text="create new account",
           font=("Arial", 12),
           bg="#f0f0f0",
           padx=30,
           pady=100
       )
       frame.pack(fill=tk.X, pady=(0, 30))
      
       #input fields!@
       name_label = tk.Label(frame, text="Name:", bg="#f0f0f0")
       name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
       self.name_entry = tk.Entry(frame, width=30)
       self.name_entry.grid(row=0, column=1, padx=26, pady=26)
      
       email_label = tk.Label(frame, text="Email:", bg="#f0f0f0")
       email_label.grid(row=1, column=0, sticky="w", padx=5, pady=5),
       self.email_entry = tk.Entry(frame, width=30)
       self.email_entry.grid(row=1, column=1, padx=5, pady=5)
      
       # Create button s!
       create_btn = tk.Button(
           frame,
           text="create account",
           command=self.create_account,
           bg="#4CAF53",
           fg="black",
           padx=30
       )
       create_btn.grid(row=2, column=1, sticky="e", padx=5, pady=10)
   def manage_acc_frame(self):
       frame = tk.LabelFrame(
           self.main_frame,
           text="manage accounts",
           font=("Arial", 12),
           bg="#f0f0f0",
           padx=100,
           pady=100
       )
       frame.pack(fill=tk.BOTH)
      
       #header for accounts d@
       self.tree_frame = tk.Frame(frame)
       self.tree_frame.pack(fill=tk.BOTH,  padx=5, pady=5)
       #scroll bar!
       scrollbar = ttk.Scrollbar(self.tree_frame)
       scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
       #headers
       self.accounts_tree = ttk.Treeview(
           self.tree_frame,
           columns=("ID", "Name", "Email", "Balance"),
           show="headings",
           yscrollcommand=scrollbar.set
       )
       #headers dfgdfg
       self.accounts_tree.heading("ID", text="id")
       self.accounts_tree.heading("Name", text="name")
       self.accounts_tree.heading("Email", text="email")
       self.accounts_tree.heading("Balance", text="balance")
      
       self.accounts_tree.column("ID", width=70)
       self.accounts_tree.column("Name", width=130)
       self.accounts_tree.column("Email", width=190)
       self.accounts_tree.column("Balance", width=90)
      
       self.accounts_tree.pack(fill=tk.BOTH, expand=True)
       scrollbar.config(command=self.accounts_tree.yview)
       # Action buttons
       btn_frame = tk.Frame(frame, bg="#f0f0f0")
       btn_frame.pack(fill=tk.X, pady=10)
       #buttons
       deposit_button = tk.Button(
           btn_frame,
           text="Deposit",
           command=self.deposit,
           bg="#FF0000",
           fg="white",
           padx=20
       )
       deposit_button.pack(side=tk.RIGHT, padx=5)
      
       withdraw_btn = tk.Button(
           btn_frame,
           text="Withdraw",
           command=self.withdraw,
           bg="#FF0000",
           fg="white",
           padx=10
       )
       withdraw_btn.pack(side=tk.LEFT, padx=10)
      
       delete_btn = tk.Button(
           btn_frame,
           text="Delete Account",
           command=self.delete_account,
           bg="#FF0000",
           fg="white",
           padx=10
       )
       delete_btn.pack(side=tk.LEFT, padx=10)
      
       refresh_btn = tk.Button(
           btn_frame,
           text="Refresh",
           command=self.load_accounts,
           bg="#FF0000",
           fg="white",
           padx=20
       )
       refresh_btn.pack(side=tk.RIGHT, padx=5)

   def create_account(self):
       name = self.name_entry.get()
       email = self.email_entry.get()
      
       if not name or not email:
           messagebox.showerror("Error", "Name and email are required")
           return
       try:
           with sqlite3.connect(DB_NAME) as conn:
               cursor = conn.cursor()
               cursor.execute("INSERT INTO accounts (name, email) VALUES (?, ?)", (name, email))
               account_id = cursor.lastrowid
               conn.commit()
              
               messagebox.showinfo("Success", f"Account created successfully! Account ID: {account_id}")
               self.name_entry.delete(0, tk.END)
               self.email_entry.delete(0, tk.END)
               self.load_accounts()
       except Exception as e:
           messagebox.showerror("Error", f"Failed to create account: {str(e)}")

   def load_accounts(self):
       #clear data
       for item in self.accounts_tree.get_children():
           self.accounts_tree.delete(item)
          
       try:
           with sqlite3.connect(DB_NAME) as conn:
               cursor = conn.cursor()
               cursor.execute("SELECT account_id, name, email, balance FROM accounts")
               accounts = cursor.fetchall()
              
               for account in accounts:
                   account_id, name, email, balance = account
                   self.accounts_tree.insert("", tk.END, values=(account_id, name, email, f"${balance:.3f}"))
       except Exception as e:
           messagebox.showerror("Error", f"Failed to load accounts: {str(e)}")
          
   def get_selected_account(self):
       selected_items = self.accounts_tree.selection()
       if not selected_items:
           messagebox.showerror("Error", "Please select an account!")
           return None
          
       item = selected_items[0]
       account_id = self.accounts_tree.item(item, "values")[0]
       return account_id
   def deposit(self):
       account_id = self.get_selected_account()
       if not account_id:
           return
       amount = simpledialog.askfloat("Deposit", "enter amount to deposit:")
       if amount is None:
           return
          
       try:
           with sqlite3.connect(DB_NAME) as conn:
               cursor = conn.cursor()
               cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (amount, account_id))
               conn.commit()
               messagebox.showinfo("success", f"deposited ${amount:.3f} successfully!")
               self.load_accounts()
       except Exception as e:
           messagebox.showerror("Error", f"failed to deposit: {str(e)}")
   def withdraw(self):
       account_id = self.get_selected_account()
       if not account_id:
           return
          
       amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:", minvalue=0.01)
       if amount is None:
           return
       try:
           with sqlite3.connect(DB_NAME) as conn:
               cursor = conn.cursor()
               # check if there's enough balance
               cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
               balance = cursor.fetchone()[0]
              
               if balance < amount:
                   messagebox.showerror("Error", "Insufficient funds!")
                   return
                  
               cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (amount, account_id))
               conn.commit()
               messagebox.showinfo("Success", f"Withdrew ${amount:.2f} successfully!")
               self.load_accounts()
       except Exception as e:
           messagebox.showerror("Error", f"Failed to withdraw: {str(e)}")
          
   def delete_account(self):
       """delete an account"""
       account_id = self.get_selected_account()
       if not account_id:
           return
          
       confirm = messagebox.askyesno("confirm", "Are you sure?")
       if not confirm:
           return
          
       try:
           with sqlite3.connect(DB_NAME) as conn:
               cursor = conn.cursor()
               cursor.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
               conn.commit()
               messagebox.showinfo("Success", "Account deleted successfully!")
               self.load_accounts()
       except Exception as e:
           messagebox.showerror("Error", f"Failed to delete account: {str(e)}")

def main():
   root = tk.Tk()
   app = Bank(root)
   root.mainloop()

if __name__ == "__main__":
   main()
