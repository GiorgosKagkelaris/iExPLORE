import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Πάρε το όνομα του διαχειριστή από τη γραμμή εντολών (ή βάλε default)
admin_username = sys.argv[1] if len(sys.argv) > 1 else "Χρήστης"

# Συνάρτηση: Άνοιγμα αρχείου για προσθήκη περιεχομένου
def open_add_content():
    try:
        subprocess.run([sys.executable, "add_content.py"])
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αποτυχία ανοίγματος του module: {e}")

# Συνάρτηση: Άνοιγμα αρχείου για διαχείριση προσφορών
def open_manage_offers():
    try:
        subprocess.run([sys.executable, "manage_offers.py"])
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αποτυχία ανοίγματος του module: {e}")

# Συνάρτηση: Αποσύνδεση χρήστη
def logout():
    confirm = messagebox.askyesno("Αποσύνδεση", "Είσαι σίγουρος/η ότι θέλεις να αποσυνδεθείς;")
    if confirm:
        root.destroy()
        # Αν χρειάζεται επιστροφή στο login, ξεκλείδωσε την παρακάτω γραμμή:
        # subprocess.Popen([sys.executable, "Login-Register_v.0.1.py"])

# Δημιουργία παραθύρου
root = tk.Tk()
root.title("Πίνακας Διαχειριστή")
root.config(bg="#f0f8ff")  # Ανοιχτό γαλάζιο background
root.geometry("500x350")

# Ετικέτα Καλωσορίσματος
tk.Label(root, text=f"👤 Καλώς ήρθες, {admin_username} (Διαχειριστής)",
         font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=20)

# Πλαίσιο για κουμπιά
button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

# Στυλ κουμπιών
button_style = {
    "width": 40,
    "height": 2,
    "bg": "#e6f2ff",
    "fg": "#333",
    "font": ("Arial", 10)
}

# Κουμπιά
tk.Button(button_frame, text="➕ Προσθήκη Νέου Περιεχομένου", command=open_add_content, **button_style).pack(pady=8)
tk.Button(button_frame, text="💸 Διαχείριση Προσφορών & Εκπτώσεων", command=open_manage_offers, **button_style).pack(pady=8)
tk.Button(button_frame, text="🚪 Αποσύνδεση", command=logout, **button_style).pack(pady=20)

# Εκκίνηση του GUI
root.mainloop()
 
