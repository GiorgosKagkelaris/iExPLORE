import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database connection
conn = sqlite3.connect('iexplore.db')
cursor = conn.cursor()

# Open Group Trip Creation Window
def open_group_travel():
    group_window = tk.Toplevel()
    group_window.title("Οργάνωση Ομαδικού Ταξιδιού")
    group_window.geometry("600x650")

    # Input Fields
    tk.Label(group_window, text="Emails συμμετεχόντων (διαχωρίστε με κόμμα)").pack()
    emails_entry = tk.Entry(group_window, width=50)
    emails_entry.pack()

    tk.Label(group_window, text="Προορισμός").pack()
    destination_entry = tk.Entry(group_window, width=50)
    destination_entry.pack()

    tk.Label(group_window, text="Ημερομηνία Έναρξης (YYYY-MM-DD)").pack()
    start_date_entry = tk.Entry(group_window, width=50)
    start_date_entry.pack()

    tk.Label(group_window, text="Ημερομηνία Λήξης (YYYY-MM-DD)").pack()
    end_date_entry = tk.Entry(group_window, width=50)
    end_date_entry.pack()

    def create_group_trip():
        emails = emails_entry.get().split(",")
        destination = destination_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        organizer_id = 1  # Δοκιμαστικό - Στη συνέχεια θα γίνει δυναμικό
        cost_per_person = 100.00  # Για δοκιμή

        # Δημιουργία Ομαδικού Ταξιδιού
        cursor.execute("INSERT INTO group_trips (organizer_id, destination, start_date, end_date, cost_per_person) VALUES (?, ?, ?, ?, ?)", (organizer_id, destination, start_date, end_date, cost_per_person))
        group_id = cursor.lastrowid
        conn.commit()

        # Αποστολή Προσκλήσεων
        for email in emails:
            email = email.strip()
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if user:
                user_id = user[0]
                cursor.execute("INSERT INTO group_trip_members (group_id, user_id, status) VALUES (?, ?, 'invited')", (group_id, user_id))

        conn.commit()
        messagebox.showinfo("Ομαδικό Ταξίδι", "Οι προσκλήσεις εστάλησαν επιτυχώς!")

    send_button = tk.Button(group_window, text="Δημιουργία Ομαδικού Ταξιδιού", command=create_group_trip)
    send_button.pack(pady=10)

root = tk.Tk()
root.title("Διαχείριση Ταξιδιών - Αρχικό Μενού")

# Button for Group Trip
group_trip_button = tk.Button(root, text="Οργάνωση Ομαδικού Ταξιδιού", command=open_group_travel, width=40, height=2)
group_trip_button.pack(pady=5)

root.mainloop()
 
