import tkinter as tk
import subprocess
from tkinter import messagebox
import sys

class TravelApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Travel Dashboard - Καλώς ήρθες!")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f8ff")  # Ανοιχτό γαλάζιο background

        self.create_main_menu()

    def create_main_menu(self):
        tk.Label(self.root, text=f"👋 Καλωσήρθες στον Πίνακα Χρήστη (ID: {self.user_id})!",
                 font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        menu_frame = tk.Frame(self.root, bg="#f0f8ff")
        menu_frame.pack(pady=10)

        options = [
            ("🔍 Αναζήτηση Προορισμών", self.search_destinations),
            ("📌 Προτάσεις Προορισμών", self.recommend_destinations),
            ("📅 Διαχείριση Κρατήσεων", self.manage_bookings),
            ("📖 Ημερολόγιο Ταξιδιών", self.travel_journal),
            ("   Δημιουργία Πλάνου", self.trip_plan),
            ("   Κοινωνική Αλληλεπίδραση", self.interaction),
            ("🌍 Κοινοποίηση Εμπειριών", self.share_experiences),
            ("💬 Μηνύματα & Ειδοποιήσεις", self.messages_notifications),
            ("⚙️ Ρυθμίσεις Προφίλ", self.profile_and_preferences),
            ("🚪 Αποσύνδεση", self.logout)
        ]

        for (label, command) in options:
            btn = tk.Button(menu_frame, text=label, command=command,
                            width=40, height=2, bg="#e6f2ff", fg="#333", font=("Arial", 10))
            btn.pack(pady=5)

    def search_destinations(self):
        subprocess.Popen([sys.executable, "booking.py", str(self.user_id)])

    def recommend_destinations(self):
        messagebox.showinfo("📌 Προτάσεις", "Εξατομικευμένες προτάσεις προορισμών.")

    def manage_bookings(self):
        messagebox.showinfo("📅 Κρατήσεις", "Διαχείριση κρατήσεων ταξιδιών.")

    def travel_journal(self):
        subprocess.Popen([sys.executable, "travel_history.py", str(self.user_id)])

    def trip_plan(self):
        subprocess.Popen([sys.executable, "trip_plan.py", str(self.user_id)])

    def share_experiences(self):
        messagebox.showinfo("🌍 Εμπειρίες", "Μοιράσου τις ταξιδιωτικές σου εμπειρίες!")

    def interaction(self):
        subprocess.Popen([sys.executable, "interaction.py", str(self.user_id)])

    def messages_notifications(self):
        messagebox.showinfo("💬 Μηνύματα", "Ειδοποιήσεις & μηνύματα.")

    def profile_and_preferences(self):
        subprocess.Popen([sys.executable, "profile_and_preferences.py", str(self.user_id)])

    def logout(self):
        confirm = messagebox.askyesno("Αποσύνδεση", "Είσαι σίγουρος ότι θέλεις να αποσυνδεθείς;")
        if confirm:
            self.root.destroy()


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
    app = TravelApp(root, user_id)
    root.mainloop()
