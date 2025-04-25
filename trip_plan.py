import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import datetime

class TravelPlanApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Δημιουργία Προσωπικού Πλάνου")
        self.root.geometry("500x500")

        self.create_plan_form()

    def create_plan_form(self):
        tk.Label(self.root, text="Δημιουργία Πλάνου", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Προορισμός:").pack()
        self.destination_entry = tk.Entry(self.root)
        self.destination_entry.pack()

        tk.Label(self.root, text="Ημερομηνία Έναρξης (YYYY-MM-DD):").pack()
        self.start_entry = tk.Entry(self.root)
        self.start_entry.pack()

        tk.Label(self.root, text="Ημερομηνία Λήξης (YYYY-MM-DD):").pack()
        self.end_entry = tk.Entry(self.root)
        self.end_entry.pack()

        tk.Label(self.root, text="Δραστηριότητες:").pack()
        self.activities_entry = tk.Entry(self.root)
        self.activities_entry.pack()

        tk.Button(self.root, text="Αποθήκευση Πλάνου", command=self.save_plan).pack(pady=10)
        tk.Button(self.root, text="Αυτόματη Πρόταση Πλάνου", command=self.auto_generate_plan).pack(pady=5)
        tk.Button(self.root, text="Τα Πλάνα μου", command=self.show_user_plans).pack(pady=5)

    def save_plan(self):
        destination = self.destination_entry.get()
        start_date = self.start_entry.get()
        end_date = self.end_entry.get()
        activities = self.activities_entry.get()

        if not all([destination, start_date, end_date]):
            messagebox.showerror("Σφάλμα", "Όλα τα πεδία είναι υποχρεωτικά.")
            return

        conn = sqlite3.connect("travel.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO travel_plans (user_id, title, destination, start_date)
            VALUES (?, ?, ?, ?)
        ''', (self.user_id, activities, destination, start_date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Επιτυχία", "Το πλάνο αποθηκεύτηκε.")
        self.root.destroy()

    def auto_generate_plan(self):
        suggestions = ["Παρίσι με επίσκεψη στον Πύργο του Άιφελ", "Ρώμη και Κολοσσαίο", "Κρουαζιέρα στο Αιγαίο"]
        suggestion = simpledialog.askstring("Πρόταση", f"Διάλεξε ένα:", initialvalue=suggestions[0])
        if suggestion:
            self.destination_entry.insert(0, suggestion.split()[0])
            self.activities_entry.insert(0, suggestion)

    def show_user_plans(self):
        conn = sqlite3.connect("travel.db")
        cursor = conn.cursor()
        cursor.execute("SELECT plan_id, destination, start_date FROM travel_plans WHERE user_id = ?", (self.user_id,))
        plans = cursor.fetchall()
        conn.close()

        plans_window = tk.Toplevel(self.root)
        plans_window.title("Τα Πλάνα Μου")

        for plan in plans:
            frame = tk.Frame(plans_window)
            frame.pack(fill="x", pady=2)
            tk.Label(frame, text=f"{plan[1]} - {plan[2]}").pack(side="left")
            tk.Button(frame, text="Διαγραφή", command=lambda p_id=plan[0]: self.delete_plan(p_id, plans_window)).pack(side="right")

    def delete_plan(self, plan_id, window):
        if messagebox.askyesno("Επιβεβαίωση", "Θέλεις σίγουρα να διαγράψεις αυτό το πλάνο;"):
            conn = sqlite3.connect("travel.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM travel_plans WHERE plan_id = ?", (plan_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Διαγραφή", "Το πλάνο διαγράφηκε.")
            window.destroy()
            self.show_user_plans()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        user_id = int(sys.argv[1])
        root = tk.Tk()
        app = TravelPlanApp(root, user_id)
        root.mainloop()
    else:
        print("Παρακαλώ δώστε user_id ως όρισμα.")
