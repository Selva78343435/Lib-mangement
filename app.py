from tkinter import *
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox as mb
import login  # Ensure the login module is correctly implemented

class StudentApp:
    def __init__(self, master):
        self.master = master
        
        # Top Frame
        frame_1 = Frame(master, width="1200", height="50", background="red", relief=GROOVE)
        frame_1.pack()
        
        label_1 = Label(frame_1, text="LIBRARY MANAGEMENT", bg="red", bd="5", width="1200",
                        font="Times_New_Roman 30 bold", foreground="black", relief=GROOVE)
        label_1.pack()
 
        # Left Frame for Student Details
        frame_3 = Frame(master, width="500", height="1200", background="red", bd="5", relief=GROOVE)
        frame_3.pack(side=LEFT)
        frame_3.pack_propagate(0)
        
        # Right Frame for other contents 
        frame_4 = Frame(master, width="900", height="1500", background="red", bd="5", relief=GROOVE)
        frame_4.pack(side=RIGHT)
        frame_4.pack_propagate(0)
        
        
        # Labels and Entry Fields
        Label(frame_3, text="Student Details", bg="red", font="Times_New_Roman 20 bold").place(x=20, y=20)

        Label(frame_3, text="ID:", bg="red", font="Times_New_Roman 10 bold").place(x=60, y=80)
        self.id_entry = Entry(frame_3, width="40")
        self.id_entry.place(x=150, y=80)

        Label(frame_3, text="Name:", bg="red", font="Times_New_Roman 10 bold").place(x=60, y=110)
        self.name_entry = Entry(frame_3, width="40")
        self.name_entry.place(x=150, y=110)

        Label(frame_3, text="Book No:", bg="red", font="Times_New_Roman 10 bold").place(x=60, y=140)
        self.bookno_entry = Entry(frame_3, width="40")
        self.bookno_entry.place(x=150, y=140)

        Label(frame_3, text="BookName:", bg="red", font="Times_New_Roman 10 bold").place(x=60, y=170)
        self.BookName_entry =Entry(frame_3,  width=40)
        self.BookName_entry.place(x=150, y=170)

        Label(frame_3, text="Department:", bg="red", font="Times_New_Roman 10 bold").place(x=60, y=200)
        self.department_entry = Entry(frame_3, width="40")
        self.department_entry.place(x=150, y=200)

        # Buttons for actions
        Button(frame_3, text="ADD", width="15", padx="5", bg="white", command=self.submit).place(x=200, y=240)
        Button(frame_3, text="Update", width="15", padx="5", bg="white", command=self.update).place(x=200, y=270)
        Button(frame_3, text="DELETE", width="15", padx="5", bg="white", command=self.delete).place(x=200, y=300)
        Button(frame_3, text="Clear", width="15", padx="5", bg="white", command=self.clear).place(x=200, y=330)
        Button(frame_3, text="Login", width="20", padx="5", bg="white", command=self.open_login).place(x=10, y=350)
        
        # Treeview for data display
        self.tree = ttk.Treeview(frame_4, columns=("c1", "c2", "c3", "c4","c5"), show='headings', height=30)
        self.tree.pack()
        
        self.tree.column("#1", anchor=CENTER, width="180")
        self.tree.heading("#1", text="Id")
        
        self.tree.column("#2", anchor=CENTER, width="180")
        self.tree.heading("#2", text="Name")
        
        self.tree.column("#3", anchor=CENTER, width="180")
        self.tree.heading("#3", text="Book No")
        
        self.tree.column("#4", anchor=CENTER, width="180")
        self.tree.heading("#4", text="BookName")
        
        self.tree.column("#5", anchor=CENTER, width="180")
        self.tree.heading("#5", text="Department")
        
        # Load initial data
        self.load_data()

    def load_data(self):
        # Load data from the database into the treeview
        try:
            connection = mysql.connector.connect(host='localhost', database='selva', user='root', password='')
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, book_no, BookNAme, department FROM students")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Error as e:
            mb.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_login(self):
        self.master.destroy()  # Close the current window
        login.LoginApp(Tk())    

    def submit(self):
        student_id = self.id_entry.get()
        student_name = self.name_entry.get()
        book_no = self.bookno_entry.get()
        book_Name= self.BookName_entry.get()
        department = self.department_entry.get()

        if not (student_id and student_name and book_no and book_Name and department):
            mb.showwarning("Input Error", "All fields must be filled out.")
            return

        # Insert data into the database
        try:
            connection = mysql.connector.connect(host='localhost', database='selva', user='root', password='')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO students (id, name, book_no, BookName, department) VALUES (%s, %s, %s, %s, %s)", 
                           (student_id, student_name, book_no, book_Name, department))
            connection.commit()
            mb.showinfo("Success", "Student added successfully.")
            self.tree.insert("", "end", values=(student_id, student_name, book_no, book_Name, department))
            self.clear()
        except Error as e:
            mb.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update(self):
        selected_item = self.tree.selection()
        if not selected_item:
            mb.showwarning("Select Error", "Please select a student record to update.")
            return

        student_id = self.id_entry.get()
        student_name = self.name_entry.get()
        book_no = self.bookno_entry.get()
        Book_Name = self.BookName_entry.get()
        department = self.department_entry.get()

        if not (student_id and student_name and book_no and Book_Name and department):
            mb.showwarning("Input Error", "All fields must be filled out.")
            return
        
        # Update data in the database
        try:
            connection = mysql.connector.connect(host='localhost', database='selva', user='root', password='')
            cursor = connection.cursor()
            cursor.execute("UPDATE students SET name=%s, book_no=%s, BookName=%s, department=%s WHERE id=%s", 
                           (student_name, book_no, Book_Name, department, student_id))
            connection.commit()
            mb.showinfo("Success", "Student updated successfully.")
            self.load_data()  # Reload data to reflect changes
            self.clear()
        except Error as e:
            mb.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            mb.showwarning("Select Error", "Please select a student record to delete.")
            return

        student_id = self.tree.item(selected_item)["values"][0]  # Get ID from selected item

        # Delete data from the database
        try:
            connection = mysql.connector.connect(host='localhost', database='selva', user='root', password='')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            connection.commit()
            mb.showinfo("Success", "Student deleted successfully.")
            self.tree.delete(selected_item)  # Remove from treeview
            self.clear()
        except Error as e:
            mb.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                cursor.close()


    def clear(self):
            # Clear all entry fields
            self.id_entry.delete(0, END)
            self.name_entry.delete(0, END)
            self.bookno_entry.delete(0, END)
            self.BookName_entry.delete(0,END)
            self.department_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    root.resizable(FALSE, FALSE)
    root.geometry("1300x550")
    root.title("College Library Management System")
    
    StudentApp(root)
    root.mainloop()