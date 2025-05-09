import sqlite3
import tkinter as tk
from tkinter import messagebox
import sys

class GroupTripManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def create_group_trip(self, destination, start_date, end_date, cost_per_person):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO group_trips (organizer_id, destination, start_date, end_date, cost_per_person)
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.user_id, destination, start_date, end_date, cost_per_person)
        )

        group_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return group_id

    def add_participants(self, group_id, participants):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()

        for participant in participants:
            cursor.execute(
                """
                SELECT user_id FROM users WHERE email = ? OR username = ?
                """,
                (participant, participant)
            )
            user = cursor.fetchone()
            if user:
                user_id = user[0]
                cursor.execute(
                    """
                    INSERT INTO group_trip_members (group_id, user_id, status)
                    VALUES (?, ?, 'invited')
                    """,
                    (group_id, user_id)
                )

        conn.commit()
        conn.close()

    def confirm_participation(self, group_id, user_id, confirm=True):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()

        status = 'confirmed' if confirm else 'declined'
        cursor.execute(
            """
            UPDATE group_trip_members
            SET status = ?
            WHERE group_id = ? AND user_id = ?
            """,
            (status, group_id, user_id)
        )

        conn.commit()
        conn.close()

    def finalize_group_trip(self, group_id):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT user_id FROM group_trip_members
            WHERE group_id = ? AND status = 'confirmed'
            """,
            (group_id,)
        )
        confirmed_members = cursor.fetchall()
        conn.close()
        return [member[0] for member in confirmed_members]

class GroupTripUI:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.manager = GroupTripManager(user_id)
        self.create_ui()

    def create_ui(self):
        self.root.title("Οργάνωση Ομαδικού Ταξιδιού")
        self.root.geometry("600x400")

        tk.Label(self.root, text="Δημιουργία Ομαδικού Ταξιδιού", font=("Arial", 16)).pack(pady=10)

        self.destination_entry = tk.Entry(self.root)
        self.destination_entry.pack(pady=5)
        self.destination_entry.insert(0, "Προορισμός")

        self.start_date_entry = tk.Entry(self.root)
        self.start_date_entry.pack(pady=5)
        self.start_date_entry.insert(0, "Ημερομηνία Έναρξης (YYYY-MM-DD)")

        self.end_date_entry = tk.Entry(self.root)
        self.end_date_entry.pack(pady=5)
        self.end_date_entry.insert(0, "Ημερομηνία Λήξης (YYYY-MM-DD)")

        self.cost_entry = tk.Entry(self.root)
        self.cost_entry.pack(pady=5)
        self.cost_entry.insert(0, "Κόστος ανά άτομο")

        self.participants_entry = tk.Entry(self.root)
        self.participants_entry.pack(pady=5)
        self.participants_entry.insert(0, "Emails/ Usernames (χωρισμένα με κόμμα)")

        tk.Button(self.root, text="Δημιουργία Ταξιδιού", command=self.create_trip).pack(pady=10)

    def create_trip(self):
        destination = self.destination_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        cost = float(self.cost_entry.get())
        participants = self.participants_entry.get().split(",")

        group_id = self.manager.create_group_trip(destination, start_date, end_date, cost)
        self.manager.add_participants(group_id, participants)

        messagebox.showinfo("Επιτυχία", "Το ομαδικό ταξίδι δημιουργήθηκε επιτυχώς!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Παρακαλώ, δώστε user_id ως όρισμα.")
        sys.exit(1)

    user_id = int(sys.argv[1])
    root = tk.Tk()
    app = GroupTripUI(root, user_id)
    root.mainloop()
