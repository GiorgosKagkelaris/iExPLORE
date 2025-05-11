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

class GroupTripUI:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.manager = GroupTripManager(user_id)
        self.root.title("Οργάνωση Ομαδικού Ταξιδιού - iExplore")
        self.root.geometry("600x650")
        self.root.config(bg="#f0f8ff")

        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Οργάνωση Ομαδικού Ταξιδιού", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(pady=10)

        self.destination_entry = tk.Entry(frame, width=40)
        self.destination_entry.insert(0, "Προορισμός")
        self.destination_entry.grid(row=0, column=0, pady=5)

        self.start_date_entry = tk.Entry(frame, width=40)
        self.start_date_entry.insert(0, "Ημερομηνία Έναρξης (YYYY-MM-DD)")
        self.start_date_entry.grid(row=1, column=0, pady=5)

        self.end_date_entry = tk.Entry(frame, width=40)
        self.end_date_entry.insert(0, "Ημερομηνία Λήξης (YYYY-MM-DD)")
        self.end_date_entry.grid(row=2, column=0, pady=5)

        self.cost_entry = tk.Entry(frame, width=40)
        self.cost_entry.insert(0, "Κόστος ανά άτομο")
        self.cost_entry.grid(row=3, column=0, pady=5)

        self.participants_entry = tk.Entry(frame, width=40)
        self.participants_entry.insert(0, "Emails/ Usernames (χωρισμένα με κόμμα)")
        self.participants_entry.grid(row=4, column=0, pady=5)

        tk.Button(frame, text="Δημιουργία Ομαδικού Ταξιδιού", command=self.create_trip, bg="#e6f2ff", fg="#333", font=("Arial", 10), width=40).grid(row=5, column=0, pady=10)

    def create_trip(self):
        destination = self.destination_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        try:
            cost = float(self.cost_entry.get())
        except ValueError:
            messagebox.showerror("Σφάλμα", "Το κόστος πρέπει να είναι αριθμός.")
            return

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
