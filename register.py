from tkinter import *
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox as mb
import login
import bcrypt  # Make sure to install this library

class RegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1200x550")
        
        self.frame_1 = Frame(self.master, width=550, height=340, background="lightblue", relief=GROOVE)
        self.frame_1.place(x=350, y=80)
        self.frame_1.pack_propagate(0)

        Label(self.frame_1, text="REGISTER", background="lightblue", font="Times_New_Roman 25 bold").place(x=180, y=20)

        Label(self.frame_1, text="UserName:", background="lightblue", font="Times_New_Roman 10 bold").place(x=55, y=90)
        self.username_entry = Entry(self.frame_1, width=40, highlightcolor="red", font="arial 10")
        self.username_entry.place(x=160, y=90)

        Label(self.frame_1, text="Password:", background="lightblue", font="Times_New_Roman 10 bold").place(x=60, y=120)
        self.password_entry = Entry(self.frame_1, width=40, highlightcolor="red", font="Times_New_Roman 10", show='*')
        self.password_entry.place(x=160, y=120)

        Label(self.frame_1, text="Re-Password:", background="lightblue", font="Times_New_Roman 10 bold").place(x=40, y=150)
        self.repassword_entry = Entry(self.frame_1, width=40, highlightcolor="red", font="Times_New_Roman 10", show='*')
        self.repassword_entry.place(x=160, y=150)

        Label(self.frame_1, text="Mobile Number:", background="lightblue", font="Times_New_Roman 10 bold").place(x=25, y=180)
        self.mobile_entry = Entry(self.frame_1, width=40, highlightcolor="red", font="Times_New_Roman 10")
        self.mobile_entry.place(x=160, y=180)

        Label(self.frame_1, text="Place:", background="lightblue", font="Times_New_Roman 10 bold").place(x=78, y=210)
        self.place_entry = Entry(self.frame_1, width=40, highlightcolor="red", font="Times_New_Roman 10")
        self.place_entry.place(x=160, y=210)

        Button(self.frame_1, text="Register", width=15, command=self.onclick, bg="lightgreen", padx=3, pady=3).place(x=300, y=250)
        Button(self.frame_1, text="Login", width=15, command=self.back, bg="lightgreen", padx=3, pady=3).place(x=150, y=250)

    def back(self):
        self.frame_1.destroy()
        login.LoginApp(self.master)

    def open_login(self):
        self.master.destroy()
        login.LoginApp(Tk())

    def onclick(self):
        username = self.username_entry.get().strip()
        userpassword = self.password_entry.get().strip()
        repassword = self.repassword_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        place = self.place_entry.get().strip()

        if not all([username, userpassword, repassword, mobile, place]):
            mb.showwarning("Input Error", "Please fill all fields.")
            return

        if userpassword != repassword:
            mb.showwarning("Input Error", "Passwords do not match.")
            return

        if not mobile.isdigit() or len(mobile) != 10:  # Example validation for mobile
            mb.showwarning("Input Error", "Please enter a valid mobile number (10 digits).")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="selva"
            )
            cursor = connection.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM selvaa WHERE username = %s", (username,))
            if cursor.fetchone():
                mb.showwarning("Input Error", "Username already exists.")
                return

            # Hash the password before storing
            hashed_password = bcrypt.hashpw(userpassword.encode('utf-8'), bcrypt.gensalt())

            query = "INSERT INTO selvaa (username, password, mobile, place) VALUES (%s, %s, %s, %s)"
            values = (username, hashed_password.decode('utf-8'), mobile, place)

            cursor.execute(query, values)
            connection.commit()
            mb.showinfo("Success", "Registration successful")
            
            self.open_login()

            # Clear the input fields
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
            self.repassword_entry.delete(0, END)
            self.mobile_entry.delete(0, END)
            self.place_entry.delete(0, END())

        except Error as e:
            mb.showerror("Database Error", f"Error connecting to database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    root = Tk()
    app = RegistrationApp(root)
    root.mainloop()
