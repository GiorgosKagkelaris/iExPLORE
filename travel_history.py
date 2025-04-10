import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys


class TravelHistoryApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Ημερολόγιο Ταξιδιών - Αξιολόγηση")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f8ff")

        self.create_travel_history()

    def create_travel_history(self):
        tk.Label(self.root, text="📖 Το Ημερολόγιο Ταξιδιών σας", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(
            pady=10)
        self.display_user_trips()

    def display_user_trips(self):
        conn = sqlite3.connect("travel.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT t.trip_id, t.destination_name, t.start_date, t.end_date
            FROM bookings b
            JOIN destinations t ON b.offer_id = t.trip_id
            WHERE b.user_id = ? AND b.status = 'confirmed'
        ''', (self.user_id,))
        trips = cursor.fetchall()
        conn.close()

        if trips:
            for trip in trips:
                trip_button = tk.Button(self.root, text=f"{trip[1]} - {trip[2]} έως {trip[3]}",
                                        command=lambda trip_id=trip[0]: self.show_review_form(trip_id))
                trip_button.pack(pady=5, fill='x')
        else:
            messagebox.showinfo("Πληροφορία", "Δεν έχεις πραγματοποιήσει κανένα ταξίδι.")

    def show_review_form(self, trip_id):
        review_window = tk.Toplevel(self.root)
        review_window.title("Αξιολόγηση Ταξιδιού")

        tk.Label(review_window, text="Αξιολόγηση (1-5 αστέρια):").pack(pady=5)

        self.rating_var = tk.IntVar()
        for i in range(1, 6):
            tk.Radiobutton(review_window, text=str(i), variable=self.rating_var, value=i).pack(side=tk.LEFT, padx=5)

        tk.Label(review_window, text="Σχόλιο:").pack(pady=5)
        self.comment_entry = tk.Entry(review_window, width=40)
        self.comment_entry.pack(pady=5)

        tk.Button(review_window, text="Υποβολή Αξιολόγησης", command=lambda: self.submit_review(trip_id)).pack(pady=10)

    def submit_review(self, trip_id):
        rating = self.rating_var.get()
        comment = self.comment_entry.get()

        if rating == 0:
            messagebox.showerror("Σφάλμα", "Πρέπει να επιλέξετε μια αξιολόγηση αστέρων.")
            return

        conn = sqlite3.connect("travel.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO trip_reviews (user_id, trip_id, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (self.user_id, trip_id, str(rating), comment))
        conn.commit()
        conn.close()

        messagebox.showinfo("Επιτυχία", "Η αξιολόγησή σας καταχωρήθηκε με επιτυχία!")
        self.root.destroy()


# Εκτέλεση
if __name__ == "__main__":
    user_id = int(sys.argv[1])  # Λήψη του user_id από το command line
    root = tk.Tk()
    app = TravelHistoryApp(root, user_id)
    root.mainloop()
