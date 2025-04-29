import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import subprocess
import os
import sys

# --- Αρχικοποίηση Βάσης Δεδομένων ---
def init_db():
    conn = sqlite3.connect("iexplore.db")
    cursor = conn.cursor()
    conn.commit()
    conn.close()


# --- Εγγραφή Χρήστη ---
def register_user(username, email, password):
    conn = sqlite3.connect("iexplore.db")
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                       (username, email, hashed_password))
        conn.commit()
        messagebox.showinfo("Επιτυχία", "Η εγγραφή ολοκληρώθηκε!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Σφάλμα", "Το username ή το email υπάρχει ήδη!")
    finally:
        conn.close()


# --- Σύνδεση Χρήστη ---
def login_user(username, password):
    conn = sqlite3.connect("iexplore.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode("utf-8"), user[1].encode("utf-8")):
        messagebox.showinfo("Σύνδεση", f"Καλώς ήρθες, {username}!")

        # Εκκίνηση του user_dashboard.py
        try:
            subprocess.Popen([sys.executable, "user_dashboard.py", str(user[0])])
            tk._default_root.destroy()  # Κλείνει το παράθυρο login
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία εκκίνησης user_dashboard.py:\n{e}")
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
    init_db()
    main_window()
