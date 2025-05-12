import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys

class ProfilePreferencesApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Ρυθμίσεις Προφίλ και Προτιμήσεις")
        self.root.geometry("500x400")
        self.root.configure(bg="#f9f9f9")

        # Σύνδεση στη βάση
        self.conn = sqlite3.connect("iexplore.db")
        self.cursor = self.conn.cursor()

        # GUI elements
        tk.Label(root, text="Προτιμώμενοι Προορισμοί:", bg="#f9f9f9").pack(pady=(10, 0))
        self.dest_entry = tk.Entry(root, width=50)
        self.dest_entry.pack(pady=5)

        tk.Label(root, text="Διατροφικές Προτιμήσεις:", bg="#f9f9f9").pack(pady=(10, 0))
        self.diet_entry = tk.Entry(root, width=50)
        self.diet_entry.pack(pady=5)

        tk.Label(root, text="Τύπος Διαμονής:", bg="#f9f9f9").pack(pady=(10, 0))
        self.accommodation_var = tk.StringVar()
        self.accommodation_var.set("hotel")
        options = ["hotel", "hostel", "apartment", "resort"]
        tk.OptionMenu(root, self.accommodation_var, *options).pack(pady=5)

        tk.Button(root, text="Αποθήκευση", command=self.save_preferences,
                  bg="#4CAF50", fg="white", width=20).pack(pady=20)

        self.load_existing_preferences()

    def load_existing_preferences(self):
        self.cursor.execute("""
            SELECT preferred_destinations, dietary_preferences, accommodation_type 
            FROM user_preferences WHERE user_id = ?""", (self.user_id,))
        row = self.cursor.fetchone()
        if row:
            self.dest_entry.insert(0, row[0])
            self.diet_entry.insert(0, row[1])
            self.accommodation_var.set(row[2])

    def save_preferences(self):
        destinations = self.dest_entry.get()
        diet = self.diet_entry.get()
        accommodation = self.accommodation_var.get()

        # Έλεγχος αν υπάρχει ήδη εγγραφή για τον χρήστη
        self.cursor.execute("SELECT * FROM user_preferences WHERE user_id = ?", (self.user_id,))
        exists = self.cursor.fetchone()

        if exists:
            self.cursor.execute("""
                UPDATE user_preferences 
                SET preferred_destinations = ?, dietary_preferences = ?, accommodation_type = ?
                WHERE user_id = ?
            """, (destinations, diet, accommodation, self.user_id))
        else:
            self.cursor.execute("""
                INSERT INTO user_preferences (user_id, preferred_destinations, dietary_preferences, accommodation_type)
                VALUES (?, ?, ?, ?)
            """, (self.user_id, destinations, diet, accommodation))

        self.conn.commit()
        messagebox.showinfo("Επιτυχία", "Οι προτιμήσεις αποθηκεύτηκαν με επιτυχία!")

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        messagebox.showerror("Σφάλμα", "Δεν δόθηκε user_id!")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        messagebox.showerror("Σφάλμα", "Μη έγκυρο user_id!")
        sys.exit(1)

    root = tk.Tk()
    app = ProfilePreferencesApp(root, user_id)
    root.mainloop()
