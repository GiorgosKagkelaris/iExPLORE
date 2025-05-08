import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser

# --- Λήψη ιστορικού ταξιδιών ---
def fetch_user_travel_history(user_id):
    conn = sqlite3.connect("iexplore.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            t.trip_id,
            t.destination,
            t.start_date,
            t.end_date,
            t.price,
            b.status
        FROM bookings b
        JOIN travel_offers t ON b.offer_id = t.offer_id
        WHERE b.user_id = ?
        ORDER BY t.start_date DESC
    """, (user_id,))

    history = cursor.fetchall()
    conn.close()
    return history

# --- Καταχώρηση αξιολόγησης ---
def submit_review(user_id, trip_id, rating, comment):
    conn = sqlite3.connect("iexplore.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO trip_reviews (user_id, trip_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """, (user_id, trip_id, rating, comment))
        conn.commit()
        messagebox.showinfo("Επιτυχία", "Η αξιολόγηση καταχωρήθηκε επιτυχώς!")
        generate_pdf(user_id, trip_id, rating, comment)
    except sqlite3.Error as e:
        messagebox.showerror("Σφάλμα", f"Σφάλμα αξιολόγησης: {e}")
    finally:
        conn.close()

# --- Δημιουργία PDF αξιολόγησης ---
def generate_pdf(user_id, trip_id, rating, comment):
    conn = sqlite3.connect("iexplore.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT destination, start_date, end_date
        FROM travel_offers
        WHERE trip_id = ?
    """, (trip_id,))
    trip = cursor.fetchone()
    conn.close()

    if not trip:
        return

    destination, start, end = trip
    filename = f"review_{user_id}_{trip_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Αξιολόγηση Ταξιδιού: {destination}")
    c.drawString(100, 730, f"Από: {start}")
    c.drawString(100, 710, f"Έως: {end}")
    c.drawString(100, 690, f"Βαθμολογία: {rating} Αστέρια")
    c.drawString(100, 670, f"Σχόλιο: {comment}")
    c.save()

    webbrowser.open(filename)

# --- Κύρια κλάση Ιστορικού ---
class TravelHistoryApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("📖 Ιστορικό Ταξιδιών")
        self.root.geometry("750x500")
        self.show_history()

    def show_history(self):
        history = fetch_user_travel_history(self.user_id)

        if not history:
            tk.Label(self.root, text="Δεν υπάρχουν ταξίδια.", font=("Arial", 14)).pack(pady=20)
            return

        tk.Label(self.root, text="Ταξίδια που έχεις κάνει:", font=("Arial", 16, "bold")).pack(pady=10)
        frame = tk.Frame(self.root)
        frame.pack()

        headers = ["Προορισμός", "Έναρξη", "Λήξη", "Τιμή", "Κατάσταση", "Αξιολόγηση"]
        for i, h in enumerate(headers):
            tk.Label(frame, text=h, font=("Arial", 10, "bold"), width=15, borderwidth=1, relief="solid").grid(row=0, column=i)

        for row_idx, (trip_id, dest, start, end, price, status) in enumerate(history, start=1):
            tk.Label(frame, text=dest, width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=0)
            tk.Label(frame, text=start, width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=1)
            tk.Label(frame, text=end, width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=2)
            tk.Label(frame, text=f"{price:.2f} €", width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=3)
            tk.Label(frame, text=status, width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=4)

            btn = tk.Button(frame, text="Αξιολόγηση", width=15,
                            command=lambda trip_id=trip_id: self.open_review_form(trip_id))
            btn.grid(row=row_idx, column=5)

    def open_review_form(self, trip_id):
        win = tk.Toplevel(self.root)
        win.title("Αξιολόγηση Ταξιδιού")
        tk.Label(win, text="Αστέρια (1-5):").pack(pady=5)

        rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            tk.Radiobutton(win, text=str(i), variable=rating_var, value=i).pack()

        tk.Label(win, text="Σχόλιο:").pack(pady=5)
        comment_entry = tk.Entry(win, width=50)
        comment_entry.pack(pady=5)

        def submit():
            rating = rating_var.get()
            comment = comment_entry.get()
            submit_review(self.user_id, trip_id, rating, comment)
            win.destroy()

        tk.Button(win, text="Υποβολή", command=submit).pack(pady=10)

# --- Εκκίνηση προγράμματος ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        tk.Tk().withdraw()
        messagebox.showerror("Σφάλμα", "Απαιτείται user_id.")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        tk.Tk().withdraw()
        messagebox.showerror("Σφάλμα", "Μη έγκυρο user_id.")
        sys.exit(1)

    root = tk.Tk()
    app = TravelHistoryApp(root, user_id)
    root.mainloop()
