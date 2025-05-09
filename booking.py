import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys

DB_PATH = 'iexplore.db'

class BookingApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Κράτηση Ταξιδιού")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f8ff")

        self.create_booking_interface()

    def create_booking_interface(self):
        tk.Label(self.root, text="Επιλογή Κατηγορίας Ταξιδιού", font=("Helvetica", 14), bg="#f0f8ff").pack(pady=10)

        categories = ["Αεροπορικό", "Οδικό", "Κρουαζιέρα"]
        self.category_var = tk.StringVar()
        self.category_var.set("Αεροπορικό")

        for category in categories:
            tk.Radiobutton(self.root, text=category, variable=self.category_var, value=category, bg="#f0f8ff").pack()

        confirm_button = tk.Button(self.root, text="Επιβεβαίωση Κατηγορίας", command=self.show_trips)
        confirm_button.pack(pady=20)

    def show_trips(self):
        selected_category = self.category_var.get()
        category_map = {"Αεροπορικό": "air", "Οδικό": "road", "Κρουαζιέρα": "cruise"}
        category_db_value = category_map.get(selected_category)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT trip_id, destination_name, price, start_date, end_date FROM destinations WHERE category = ? AND available_seats > 0", (category_db_value,))
        trips = cursor.fetchall()
        conn.close()

        if not trips:
            messagebox.showinfo("Διαθέσιμα Ταξίδια", "Δεν υπάρχουν διαθέσιμα ταξίδια για την κατηγορία αυτή.")
            return

        self.show_trip_selection(trips)

    def show_trip_selection(self, trips):
        self.trip_selection_window = tk.Toplevel(self.root)
        self.trip_selection_window.title("Επιλογή Ταξιδιού")
        self.trip_selection_window.geometry("500x400")
        self.trip_selection_window.config(bg="#f0f8ff")

        for trip in trips:
            trip_id, destination, price, start_date, end_date = trip
            trip_info = f"{destination} - {start_date} έως {end_date} - {price} €"
            tk.Button(self.trip_selection_window, text=trip_info, command=lambda t=trip: self.confirm_booking(t)).pack(pady=5)

    def confirm_booking(self, trip):
        trip_id, destination, price, start_date, end_date = trip
        confirm = messagebox.askyesno("Επιβεβαίωση Κράτησης", f"Θέλεις να προχωρήσεις με την κράτηση για το {destination} με κόστος {price} €;")

        if confirm:
            self.process_payment(trip_id, price)

    def process_payment(self, trip_id, amount):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bookings (user_id, offer_id, status) VALUES (?, ?, 'confirmed')", (self.user_id, trip_id))
            conn.commit()
            booking_id = cursor.lastrowid
            cursor.execute("INSERT INTO payments (booking_id, amount, payment_status) VALUES (?, ?, 'paid')", (booking_id, amount))
            conn.commit()
            conn.close()
            messagebox.showinfo("Επιτυχία Κράτησης", "Η κράτηση ολοκληρώθηκε επιτυχώς!")
        except Exception as e:
            messagebox.showerror("Σφάλμα Κράτησης", f"Σφάλμα κατά την ολοκλήρωση της κράτησης: {e}")


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
    app = BookingApp(root, user_id)
    root.mainloop()
