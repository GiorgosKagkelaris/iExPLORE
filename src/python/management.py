import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

DB_PATH = "iexplore.db"

def get_offers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT offer_id, trip_id, destination, price, available_seats, start_date, end_date FROM travel_offers")
    results = c.fetchall()
    conn.close()
    return results

def refresh_offers(tree):
    for row in tree.get_children():
        tree.delete(row)
    for offer in get_offers():
        tree.insert('', 'end', values=offer)

def add_offer_window():
    def submit_offer():
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                INSERT INTO travel_offers (trip_id, destination, price, available_seats, start_date, end_date, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                int(trip_id.get()), destination.get(), float(price.get()), int(seats.get()),
                start_date.get(), end_date.get(), 1  # dummy admin id
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Επιτυχία", "Η προσφορά προστέθηκε.")
            win.destroy()
            refresh_offers(tree)
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία προσθήκης: {e}")

    win = tk.Toplevel(root)
    win.title("Νέα Προσφορά")

    labels = ["Trip ID", "Προορισμός", "Τιμή", "Διαθέσιμες Θέσεις", "Ημ/νία Έναρξης", "Ημ/νία Λήξης"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0, pady=5, padx=5)
        entry = tk.Entry(win)
        entry.grid(row=i, column=1)
        entries.append(entry)

    trip_id, destination, price, seats, start_date, end_date = entries

    tk.Button(win, text="Αποθήκευση", command=submit_offer).grid(row=len(labels), columnspan=2, pady=10)

def delete_offer(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Προσοχή", "Επέλεξε μία προσφορά για διαγραφή.")
        return
    offer_id = tree.item(selected[0])['values'][0]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM travel_offers WHERE offer_id = ?", (offer_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Επιτυχία", "Η προσφορά διαγράφηκε.")
    refresh_offers(tree)

def show_reviews():
    def load_reviews():
        trip = trip_id.get()
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT rating, comment FROM trip_reviews WHERE trip_id = ?", (trip,))
            reviews = c.fetchall()
            conn.close()
            review_list.delete(0, tk.END)
            for r in reviews:
                review_list.insert(tk.END, f"⭐ {r[0]} - {r[1]}")
        except:
            review_list.insert(tk.END, "Σφάλμα ανάκτησης αξιολογήσεων.")

    rev = tk.Toplevel(root)
    rev.title("Αξιολογήσεις Χρηστών")

    tk.Label(rev, text="Trip ID:").pack(pady=5)
    trip_id = tk.Entry(rev)
    trip_id.pack()
    tk.Button(rev, text="Εμφάνιση Αξιολογήσεων", command=load_reviews).pack(pady=5)

    review_list = tk.Listbox(rev, width=60)
    review_list.pack(pady=10)

root = tk.Tk()
root.title("Διαχείριση Προσφορών & Εκπτώσεων")
root.geometry("900x500")
root.config(bg="#f0f8ff")

title = tk.Label(root, text="💼 Διαχείριση Προσφορών", font=("Helvetica", 18, "bold"), bg="#f0f8ff")
title.pack(pady=10)

# Treeview για προβολή προσφορών
columns = ("ID", "Trip ID", "Προορισμός", "Τιμή", "Θέσεις", "Έναρξη", "Λήξη")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(pady=10)

refresh_offers(tree)

button_style = {
    "width": 40,
    "height": 2,
    "bg": "#e6f2ff",
    "fg": "#333",
    "font": ("Arial", 10)
}


btn_frame = tk.Frame(root, bg="#f0f8ff")
btn_frame.pack(pady=20)


tk.Button(btn_frame, text="➕ Νέα Προσφορά", command=add_offer_window, **button_style).pack(pady=8)
tk.Button(btn_frame, text="🗑️ Διαγραφή Επιλεγμένης Προσφοράς", command=lambda: delete_offer(tree), **button_style).pack(pady=8)
tk.Button(btn_frame, text="⭐ Προβολή Αξιολογήσεων", command=show_reviews, **button_style).pack(pady=8)

root.mainloop()
