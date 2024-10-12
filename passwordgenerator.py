import tkinter as tk
from tkinter import messagebox
import random
import string
import sqlite3

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        self.username = tk.StringVar()
        self.password_length = tk.IntVar()
        self.generated_password = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Create main frame
        main_frame = tk.Frame(self.master, bg='#d9944d')
        main_frame.pack(padx=20, pady=20)

        # Create title label
        title_label = tk.Label(main_frame, text="PASSWORD GENERATOR:", anchor=tk.N, fg='white', bg='#d9944d', font=('arial', 20, 'bold'))
        title_label.grid(row=0, column=1, padx=10, pady=10)

        # Create username label and entry
        username_label = tk.Label(main_frame, text="Enter Username:", font=('times', 15, 'bold'), bg='#d9944d', fg='black')
        username_label.grid(row=1, column=0, padx=10, pady=10)
        username_entry = tk.Entry(main_frame, textvariable=self.username, font=('times', 15), bd=6, relief='ridge', bg='#e1dbd5', fg='black')
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create password length label and entry
        password_length_label = tk.Label(main_frame, text="Enter Password Length:", font=('times', 15, 'bold'), bg='#d9944d', fg='black')
        password_length_label.grid(row=2, column=0, padx=10, pady=10)
        password_length_entry = tk.Entry(main_frame, textvariable=self.password_length, font=('times', 15), bd=6, relief='ridge', bg='#e1dbd5', fg='black')
        password_length_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create generated password label and entry
        generated_password_label = tk.Label(main_frame, text="Generated Password:", font=('times', 15, 'bold'), bg='#d9944d', fg='black')
        generated_password_label.grid(row=3, column=0, padx=10, pady=10)
        generated_password_entry = tk.Entry(main_frame, textvariable=self.generated_password, font=('times', 15), bd=6, relief='ridge', bg='#e1dbd5', fg='black')
        generated_password_entry.grid(row=3, column=1, padx=10, pady=10)

        # Create buttons
        generate_button = tk.Button(main_frame, text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font=('Verdana', 15, 'bold'), bg='#e1dbd5', fg='black', command=self.generate_password)
        generate_button.grid(row=4, column=1, padx=10, pady=10)

        accept_button = tk.Button(main_frame, text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font=('Helvetica', 15, 'bold', 'italic'), bg='#e1dbd5', fg='black', command=self.accept_fields)
        accept_button.grid(row=5, column=1, padx=10, pady=10)

        reset_button = tk.Button(main_frame, text="RESET", bd=3, relief='solid', padx=1, pady=1, font=('Helvetica', 15, 'bold', 'italic'), bg='#e1dbd5', fg='black', command=self.reset_fields)
        reset_button.grid(row=6, column=1, padx=10, pady=10)

    def generate_password(self):
        username = self.username.get()
        password_length = self.password_length.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return

        if not password_length:
            messagebox.showerror("Error", "Password length cannot be empty")
            return

        if password_length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        # Generate password
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(password_length))
        self.generated_password.set(password)

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = "SELECT * FROM users WHERE Username = ?"
            cursor.execute(find_user, (self.username.get(),))

            if cursor.fetchall():
                messagebox.showerror("Error", "Username already exists")
                return

            insert_query = "INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)"
            cursor.execute(insert_query, (self.username.get(), self.generated_password.get()))
            db.commit()
            messagebox.showinfo("Success", "Password generated successfully")

    def reset_fields(self):
        self.username.set("")
        self.password_length.set(0)
        self.generated_password.set("")

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Password Generator')
    root.geometry('660x500')
    root.config(bg='#d9944d')
    root.resizable(False, False)

    password_generator = PasswordGenerator(root)
    root.mainloop()