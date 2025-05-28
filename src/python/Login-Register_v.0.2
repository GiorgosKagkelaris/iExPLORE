import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess
import os
import sys
import re

DB_NAME = "iexplore.db"


# --- Έλεγχος email ---
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# --- Εγγραφή Χρήστη ---
def register_user(username, email, password):
    if not is_valid_email(email):
        messagebox.showerror("Σφάλμα", "Μη έγκυρο email")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """, (username, email, hashed_password))
        conn.commit()
        messagebox.showinfo("Επιτυχία", "Η εγγραφή ολοκληρώθηκε!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Σφάλμα", "Το username ή το email υπάρχει ήδη!")
    finally:
        conn.close()


# --- Σύνδεση Χρήστη ---
def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, password_hash, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode("utf-8"), user[1].encode("utf-8")):
        user_id, _, role = user
        messagebox.showinfo("Σύνδεση", f"Καλώς ήρθες, {username}!")

        try:
            # Επιλέγει το κατάλληλο αρχείο dashboard
            dashboard_file = "admin_dashboard.py" if role == "admin" else "user_dashboard.py"
            subprocess.run(["python", "admin_dashboard.py", username]) if role =="admin" else subprocess.Popen([sys.executable, dashboard_file, str(user_id)])

            tk._default_root.destroy()  # Κλείσιμο του παραθύρου σύνδεσης
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία εκκίνησης {dashboard_file}:\n{e}")
    else:
        messagebox.showerror("Σφάλμα", "Λάθος username ή password")



# --- GUI Εγγραφής ---
def register_window():
    reg = tk.Toplevel()
    reg.title("Εγγραφή")

    tk.Label(reg, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(reg)
    username_entry.grid(row=0, column=1)

    tk.Label(reg, text="Email:").grid(row=1, column=0)
    email_entry = tk.Entry(reg)
    email_entry.grid(row=1, column=1)

    tk.Label(reg, text="Password:").grid(row=2, column=0)
    password_entry = tk.Entry(reg, show="*")
    password_entry.grid(row=2, column=1)

    def submit_register():
        register_user(username_entry.get(), email_entry.get(), password_entry.get())

    tk.Button(reg, text="Εγγραφή", command=submit_register).grid(row=3, columnspan=2)


# --- Κεντρικό Παράθυρο ---
def main_window():
    if not os.path.exists(DB_NAME):
        messagebox.showerror("Σφάλμα", f"Η βάση δεδομένων '{DB_NAME}' δεν βρέθηκε.\nΕκτελέστε πρώτα το αρχείο iexplore_database.py.")
        sys.exit()

    root = tk.Tk()
    root.title("Travel Login")

    tk.Label(root, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1)

    tk.Label(root, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(root, text="Σύνδεση", command=lambda: login_user(username_entry.get(), password_entry.get())).grid(row=2, columnspan=2)
    tk.Button(root, text="Εγγραφή", command=register_window).grid(row=3, columnspan=2)

    root.mainloop()


# --- Εκκίνηση ---
if __name__ == "__main__":
    main_window()
