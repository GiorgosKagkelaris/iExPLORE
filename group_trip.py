import tkinter as tk
from tkinter import messagebox
import sqlite3


# Database connection
conn = sqlite3.connect('iexplore.db')
cursor = conn.cursor()


# Κλάση User
class User:
    def __init__(self, user_id, email, name):
        self.user_id = user_id
        self.email = email
        self.name = name

    @staticmethod
    def get_user_by_email(email):
        cursor.execute("SELECT user_id, email, name FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            return User(result[0], result[1], result[2])
        return None


# Κλάση Trip
class Trip:
    def __init__(self, destination, start_date, end_date, cost_per_person):
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.cost_per_person = cost_per_person


# Κλάση GroupTrip (Επεκτείνει την κλάση Trip)
class GroupTrip(Trip):
    def __init__(self, organizer_id, destination, start_date, end_date, cost_per_person):
        super().__init__(destination, start_date, end_date, cost_per_person)
        self.organizer_id = organizer_id
        self.group_id = None  # Θα οριστεί μετά την εισαγωγή στη βάση
        self.members = []

    def save_to_db(self):
        cursor.execute("INSERT INTO group_trips (organizer_id, destination, start_date, end_date, cost_per_person) VALUES (?, ?, ?, ?, ?)", 
                       (self.organizer_id, self.destination, self.start_date, self.end_date, self.cost_per_person))
        self.group_id = cursor.lastrowid
        conn.commit()

    def add_member(self, user):
        self.members.append(user)
        cursor.execute("INSERT INTO group_trip_members (group_id, user_id, status) VALUES (?, ?, 'invited')", 
                       (self.group_id, user.user_id))
        conn.commit()

    def send_invitations(self):
        for user in self.members:
            Invitation.send_invitation(user, self)


# Κλάση Invitation
class Invitation:
    @staticmethod
    def send_invitation(user, group_trip):
        # Θα μπορούσε να είναι μια αποστολή email στην πραγματικότητα
        messagebox.showinfo("Πρόσκληση", f"Η πρόσκληση για το ομαδικό ταξίδι προς {group_trip.destination} έχει σταλεί στον {user.name} ({user.email}).")


# Κλάση GroupTripWindow (Εφαρμογή Tkinter)
class GroupTripWindow:
    def __init__(self, root):
        self.root = root
        self.group_window = None

    def open_group_travel(self):
        if self.group_window is None or not self.group_window.winfo_exists():
            self.group_window = tk.Toplevel(self.root)
            self.group_window.title("Οργάνωση Ομαδικού Ταξιδιού")
            self.group_window.geometry("600x650")

            # Input Fields
            tk.Label(self.group_window, text="Emails συμμετεχόντων (διαχωρίστε με κόμμα)").pack()
            self.emails_entry = tk.Entry(self.group_window, width=50)
            self.emails_entry.pack()

            tk.Label(self.group_window, text="Προορισμός").pack()
            self.destination_entry = tk.Entry(self.group_window, width=50)
            self.destination_entry.pack()

            tk.Label(self.group_window, text="Ημερομηνία Έναρξης (YYYY-MM-DD)").pack()
            self.start_date_entry = tk.Entry(self.group_window, width=50)
            self.start_date_entry.pack()

            tk.Label(self.group_window, text="Ημερομηνία Λήξης (YYYY-MM-DD)").pack()
            self.end_date_entry = tk.Entry(self.group_window, width=50)
            self.end_date_entry.pack()

            send_button = tk.Button(self.group_window, text="Δημιουργία Ομαδικού Ταξιδιού", command=self.create_group_trip)
            send_button.pack(pady=10)

    def create_group_trip(self):
        emails = self.emails_entry.get().split(",")
        destination = self.destination_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        organizer_email = "organizer@example.com"  # Για παράδειγμα, το email του οργανωτή
        organizer = User.get_user_by_email(organizer_email)
        if not organizer:
            messagebox.showerror("Σφάλμα", "Ο οργανωτής δεν βρέθηκε.")
            return

        group_trip = GroupTrip(organizer.user_id, destination, start_date, end_date, 100.00)
        group_trip.save_to_db()

        for email in emails:
            user = User.get_user_by_email(email.strip())
            if user:
                group_trip.add_member(user)

        group_trip.send_invitations()
        messagebox.showinfo("Ομαδικό Ταξίδι", "Η ομαδική κράτηση δημιουργήθηκε και οι προσκλήσεις στάλθηκαν!")


# Main window
root = tk.Tk()
root.title("Διαχείριση Ταξιδιών - Αρχικό Μενού")

group_trip_window = GroupTripWindow(root)

# Button for Group Trip
group_trip_button = tk.Button(root, text="Οργάνωση Ομαδικού Ταξιδιού", command=group_trip_window.open_group_travel, width=40, height=2)
group_trip_button.pack(pady=5)

root.mainloop()
 
