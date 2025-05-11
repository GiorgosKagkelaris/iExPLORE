import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import sys
import os

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def disable_notifications(self, notification_type):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET notifications_enabled = ?
            WHERE user_id = ?
        """, (notification_type, self.user_id))
        conn.commit()
        conn.close()

    def notify_user(self, notification_type, message):
        # Αποστολή ειδοποίησης στον χρήστη
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notifications (user_id, type, message)
            VALUES (?, ?, ?)
        """, (self.user_id, notification_type, message))
        conn.commit()
        conn.close()


class TripPost:
    def __init__(self, post_id=None):
        self.post_id = post_id

    @staticmethod
    def create_post(user_id, trip_id, content, visibility, photos):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trip_posts (user_id, trip_id, content, visibility)
            VALUES (?, ?, ?, ?)
        """, (user_id, trip_id, content, visibility))
        post_id = cursor.lastrowid

        for photo in photos:
            cursor.execute("""
                INSERT INTO photos (post_id, filepath)
                VALUES (?, ?)
            """, (post_id, photo))

        # Ειδοποίηση δημιουργίας ανάρτησης
        user = User(user_id)
        user.notify_user("post_created", f"Η εμπειρία σας κοινοποιήθηκε με ID: {post_id}")

        conn.commit()
        conn.close()
        return post_id

    @staticmethod
    def report_post(post_id, reporter_id):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reports (post_id, reporter_id)
            VALUES (?, ?)
        """, (post_id, reporter_id))
        conn.commit()
        conn.close()

    def fetch_post(self):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM trip_posts WHERE post_id = ?", (self.post_id,))
        post = cursor.fetchone()
        conn.close()
        return post[0] if post else None


class InteractionUI:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.photos = []
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Travel Experience Sharing")
        self.root.geometry("600x650")
        self.root.config(bg="#f0f8ff")

        tk.Label(self.root, text="🌍 Κοινοποίηση Ταξιδιωτικής Εμπειρίας", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        self.content_entry = tk.Entry(self.root, width=60, font=("Arial", 10))
        self.content_entry.insert(0, "Περιγραφή...")
        self.content_entry.pack(pady=5)

        self.visibility_entry = tk.Entry(self.root, width=60, font=("Arial", 10))
        self.visibility_entry.insert(0, "Ορατότητα (public/friends)")
        self.visibility_entry.pack(pady=5)

        self.trip_dropdown_label = tk.Label(self.root, text="Επιλέξτε Ταξίδι", font=("Arial", 10), bg="#f0f8ff")
        self.trip_dropdown_label.pack(pady=5)

        self.trip_dropdown = ttk.Combobox(self.root, width=60, font=("Arial", 10))
        self.trip_dropdown.pack(pady=5)

        tk.Button(self.root, text="📸 Προσθήκη Φωτογραφιών", command=self.add_photos, bg="#e6f2ff", fg="#333", font=("Arial", 10), width=40).pack(pady=10)
        tk.Button(self.root, text="📤 Κοινοποίηση Εμπειρίας", command=self.share_experience, bg="#e6f2ff", fg="#333", font=("Arial", 10), width=40).pack(pady=10)
        tk.Button(self.root, text="🚨 Αναφορά Ανάρτησης", command=self.report_post, bg="#e6f2ff", fg="#333", font=("Arial", 10), width=40).pack(pady=10)
        tk.Button(self.root, text="🔕 Απενεργοποίηση Ειδοποιήσεων", command=self.disable_notifications, bg="#e6f2ff", fg="#333", font=("Arial", 10), width=40).pack(pady=10)

        self.load_user_trips()

    def load_user_trips(self):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT trip_id, destination_name
            FROM destinations
            WHERE trip_id IN (
                SELECT trip_id FROM bookings WHERE user_id = ?
            )
        """, (self.user_id,))
        trips = cursor.fetchall()
        conn.close()

        trip_names = [f"{trip[1]} (ID: {trip[0]})" for trip in trips]
        self.trip_dropdown['values'] = trip_names
        if trips:
            self.trip_dropdown.set(trip_names[0])

    def add_photos(self):
        files = filedialog.askopenfilenames(title="Επιλέξτε Φωτογραφίες", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.photos.extend(files)
        messagebox.showinfo("Φωτογραφίες", f"Επιλέχθηκαν {len(files)} φωτογραφίες.")

    def share_experience(self):
        content = self.content_entry.get()
        visibility = self.visibility_entry.get()
        selected_trip = self.trip_dropdown.get()
        trip_id = int(selected_trip.split('(')[1].split(')')[0])
        post_id = TripPost.create_post(self.user_id, trip_id, content, visibility, self.photos)
        messagebox.showinfo("Επιτυχία", f"Η εμπειρία κοινοποιήθηκε με ID: {post_id}")

    def report_post(self):
        post_id = int(self.content_entry.get())
        TripPost.report_post(post_id, self.user_id)
        messagebox.showinfo("Αναφορά", "Η αναφορά καταχωρήθηκε επιτυχώς.")

    def disable_notifications(self):
        user = User(self.user_id)
        user.disable_notifications("likes/comments")
        messagebox.showinfo("Ειδοποιήσεις", "Οι ειδοποιήσεις απενεργοποιήθηκαν.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Παρακαλώ, δώστε user_id ως όρισμα.")
        sys.exit(1)

    user_id = int(sys.argv[1])
    root = tk.Tk()
    app = InteractionUI(root, user_id)
    root.mainloop()
