import tkinter as tk
import subprocess
from tkinter import messagebox
import sqlite3


class TravelApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id  # user_id περνιέται κατά την εκκίνηση
        self.root.title("Travel Dashboard - Καλώς ήρθες!")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f8ff")  # Ανοιχτό γαλάζιο background

        self.create_main_menu()

    def create_main_menu(self):
        tk.Label(self.root, text="👋 Καλωσήρθες στον Πίνακα Χρήστη!",
                 font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        menu_frame = tk.Frame(self.root, bg="#f0f8ff")
        menu_frame.pack(pady=10)

        options = [
            ("🔍 Αναζήτηση Προορισμών", self.search_destinations),
            ("📌 Προτάσεις Προορισμών", self.recommend_destinations),
            ("📅 Διαχείριση Κρατήσεων", self.manage_bookings),
            ("📖 Ημερολόγιο Ταξιδιών", self.travel_journal),  # Το κουμπί που οδηγεί στο travel_history.py
            ("🌍 Κοινοποίηση Εμπειριών", self.share_experiences),
            ("💬 Μηνύματα & Ειδοποιήσεις", self.messages_notifications),
            ("⚙️ Ρυθμίσεις Λογαριασμού", self.account_settings),
            ("🚪 Αποσύνδεση", self.logout)
        ]

        for (label, command) in options:
            btn = tk.Button(menu_frame, text=label, command=command,
                            width=40, height=2, bg="#e6f2ff", fg="#333", font=("Arial", 10))
            btn.pack(pady=5)

    # Placeholder methods
    def search_destinations(self):
        messagebox.showinfo("🔍 Αναζήτηση", "Λειτουργία αναζήτησης προορισμών.")

    def recommend_destinations(self):
        messagebox.showinfo("📌 Προτάσεις", "Εξατομικευμένες προτάσεις προορισμών.")

    def manage_bookings(self):
        messagebox.showinfo("📅 Κρατήσεις", "Διαχείριση κρατήσεων ταξιδιών.")

    def travel_journal(self):
        # Αντί για messagebox, εκκινεί το travel_history.py με το user_id
        subprocess.Popen(["python", "travel_history.py", str(self.user_id)])

    def share_experiences(self):
        messagebox.showinfo("🌍 Εμπειρίες", "Μοιράσου τις ταξιδιωτικές σου εμπειρίες!")

    def messages_notifications(self):
        messagebox.showinfo("💬 Μηνύματα", "Ειδοποιήσεις & μηνύματα.")

    def account_settings(self):
        messagebox.showinfo("⚙️ Ρυθμίσεις", "Ρυθμίσεις λογαριασμού.")

    def logout(self):
        confirm = messagebox.askyesno("Αποσύνδεση", "Είσαι σίγουρος ότι θέλεις να αποσυνδεθείς;")
        if confirm:
            self.root.destroy()


# Εκτέλεση
if __name__ == "__main__":
    # Πάρτε το user_id από τη διαδικασία login (π.χ. από τη βάση δεδομένων ή τη σύνδεση του χρήστη)
    user_id = 1  # Αυτό είναι ένα παράδειγμα user_id, προσαρμόστε το σύμφωνα με το σύστημά σας
    root = tk.Tk()
    app = TravelApp(root, user_id)
    root.mainloop()
