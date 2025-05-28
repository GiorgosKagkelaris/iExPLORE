import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database connection
conn = sqlite3.connect('iexplore.db')
cursor = conn.cursor()

# Κλάση User
class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

    @staticmethod
    def get_user_by_email(email):
        cursor.execute("SELECT user_id, username, email FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            return User(result[0], result[1], result[2])
        return None


# Κλάση UserProfile (Αποθήκευση προσωπικών δεδομένων και προτιμήσεων)
class UserProfile:
    def __init__(self, user_id, name, email, preferences=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.preferences = preferences if preferences else {}

    def save_profile(self, preferences=None):
        if preferences:
            self.preferences.update(preferences)
        cursor.execute("INSERT INTO user_profiles (user_id, name, email, preferences) VALUES (?, ?, ?, ?)", 
                       (self.user_id, self.name, self.email, str(self.preferences)))
        conn.commit()

    def update_preferences(self, new_preferences):
        self.preferences.update(new_preferences)
        cursor.execute("UPDATE user_profiles SET preferences = ? WHERE user_id = ?", 
                       (str(self.preferences), self.user_id))
        conn.commit()

    def get_preferences(self):
        return self.preferences


# Κλάση RecommendationEngine (Για την παραγωγή προτάσεων)
class RecommendationEngine:
    @staticmethod
    def update_recommendations(user_id):
        # Εδώ θα μπορούσαμε να προσθέσουμε λογική για να παράγουμε εξατομικευμένες προτάσεις
        messagebox.showinfo("Προτάσεις", "Εξατομικευμένες προτάσεις για τον χρήστη.")

    @staticmethod
    def provide_general_suggestions():
        # Εδώ θα προσθέσουμε γενικές προτάσεις αν δεν έχουν καθοριστεί προτιμήσεις
        messagebox.showinfo("Προτάσεις", "Γενικές προτάσεις ταξιδιών.")


# Κλάση ProfileSettingsWindow (GUI για Ρυθμίσεις Προφίλ)
class ProfileSettingsWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.profile_window = None
        self.user_profile = UserProfile(self.user.user_id, self.user.username, self.user.email)

    def open_profile_settings(self):
        if self.profile_window is None or not self.profile_window.winfo_exists():
            self.profile_window = tk.Toplevel(self.root)
            self.profile_window.title("Ρυθμίσεις Προφίλ")
            self.profile_window.geometry("600x650")

            # Εμφάνιση φόρμας για τα προσωπικά δεδομένα
            tk.Label(self.profile_window, text="Όνομα:").pack()
            self.name_entry = tk.Entry(self.profile_window, width=50)
            self.name_entry.insert(0, self.user.username)
            self.name_entry.pack()

            tk.Label(self.profile_window, text="Email:").pack()
            self.email_entry = tk.Entry(self.profile_window, width=50)
            self.email_entry.insert(0, self.user.email)
            self.email_entry.pack()

            tk.Label(self.profile_window, text="Προτιμήσεις Ταξιδιών (π.χ. Προορισμός, Τύπος Διαμονής):").pack()
            self.preferences_entry = tk.Entry(self.profile_window, width=50)
            self.preferences_entry.pack()

            # Κουμπί για αποθήκευση
            save_button = tk.Button(self.profile_window, text="Αποθήκευση Προφίλ", command=self.save_profile)
            save_button.pack(pady=10)

            # Κουμπί για παράλειψη προτιμήσεων
            skip_button = tk.Button(self.profile_window, text="Παράλειψη Προτιμήσεων", command=self.skip_preferences)
            skip_button.pack(pady=5)

    def save_profile(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        preferences = self.preferences_entry.get()

        # Αποθήκευση προφίλ και προτιμήσεων
        self.user_profile.save_profile(preferences)

        # Ενημέρωση προτάσεων
        if preferences:
            RecommendationEngine.update_recommendations(self.user.user_id)
        else:
            RecommendationEngine.provide_general_suggestions()

        messagebox.showinfo("Επιτυχία", "Το προφίλ σας αποθηκεύτηκε επιτυχώς!")
        self.profile_window.destroy()

    def skip_preferences(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        # Αποθήκευση προφίλ χωρίς προτιμήσεις
        self.user_profile.save_profile()

        # Παροχή γενικών προτάσεων
        RecommendationEngine.provide_general_suggestions()

        messagebox.showinfo("Επιτυχία", "Το προφίλ σας αποθηκεύτηκε επιτυχώς χωρίς προτιμήσεις!")
        self.profile_window.destroy()


# Κλάση MainWindow (Κύριο παράθυρο της εφαρμογής)
class MainWindow:
    def __init__(self, root):
        self.root = root

    def open_profile_settings(self):
        user_email = "user@example.com"  # Για παράδειγμα, το email του χρήστη
        user = User.get_user_by_email(user_email)
        if user:
            profile_window = ProfileSettingsWindow(self.root, user)
            profile_window.open_profile_settings()
        else:
            messagebox.showerror("Σφάλμα", "Ο χρήστης δεν βρέθηκε.")

# Εφαρμογή Tkinter
root = tk.Tk()
root.title("Διαχείριση Ταξιδιών - Αρχικό Μενού")

main_window = MainWindow(root)

# Κουμπί για άνοιγμα ρυθμίσεων προφίλ
profile_button = tk.Button(root, text="Ρυθμίσεις Προφίλ", command=main_window.open_profile_settings, width=40, height=2)
profile_button.pack(pady=5)

root.mainloop()
