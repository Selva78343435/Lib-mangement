from tkinter import *
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox as mb
import register  # Ensure this module is correctly implemented
import app  # Ensure this module is correctly implemented

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1200x550")

        self.frame_1 = Frame(self.master, width=500, height=300, background="lightblue", relief=GROOVE)
        self.frame_1.place(x=350, y=80)
        self.frame_1.pack_propagate(0)

        Label(self.frame_1, text="LOGIN", background="lightblue", font="arial 25 bold").place(x=180, y=20)

        Label(self.frame_1, text="UserName:", background="lightblue", font="arial 10 bold").place(x=30, y=80)
        self.username_entry = Entry(self.frame_1, width=40, highlightcolor="red", font="arial 10")
        self.username_entry.place(x=150, y=80)

        Label(self.frame_1, text="Password:", background="lightblue", font="arial 10 bold").place(x=30, y=120)
        self.password_entry = Entry(self.frame_1, width=40, highlightcolor="red", font="arial 10", show='*')
        self.password_entry.place(x=150, y=120)

        Button(self.frame_1, text="Login", width=15, command=self.onclick, bg="lightgreen", padx=3, pady=3).place(x=220, y=170)
        Button(self.frame_1, text="Register here", width=15, command=self.open_register, bg="lightgreen", padx=3, pady=3).place(x=220, y=210)
        # Button(self.frame_1, text="", width=15, command=self.open_app, bg="lightgreen", padx=3, pady=3).place(x=220, y=240)

    def open_register(self):
        self.frame_1.destroy()
        register.RegistrationApp(self.master)

    def open_app(self):
        self.frame_1.destroy()
        app.StudentApp(self.master)

    def onclick(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            mb.showwarning("Input Error", "Please fill in both fields.")
            return

        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="selva")
            cursor = connection.cursor()
            query = "SELECT username, password FROM selvaa WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                mb.showinfo("Login", "Login successful")
                self.open_app()  # Transition to the student app
            else:
                mb.showerror("Login", "Invalid username or password.")
        except Error as e:
            mb.showerror("Error", f"Error connecting to database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()
