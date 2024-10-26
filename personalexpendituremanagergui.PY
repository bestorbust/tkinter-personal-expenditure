import sqlite3
from tkinter import Tk, Frame, StringVar, END, Button, Entry, Label, Text, ttk, messagebox, DISABLED , LabelFrame, NORMAL

class PEM:
    def __init__(self, app):
        self.app = app
        self.app.title("Personal Expenditure Manager")  
        self.app.geometry("8000x800")  

        self.bg_color = "#FFFFFF"  
        self.button_color = "#4CAF50"  
        self.label_font = ("Arial", 10, "bold")  
        self.entry_font = ("Arial", 12)
        self.text_font = ("Arial", 11)
        self.label_bg = "#2B4257"  
        self.label_fg = "#FFFFFF"  

        self.notebook = ttk.Notebook(self.app) 
        self.notebook.pack(fill="both", expand=True) 

        self.add_item_frame = Frame(self.notebook, bg=self.bg_color) 
        self.notebook.add(self.add_item_frame, text="Add Expenditure") 
        self.create_add_item_page() 

        self.check_investment_frame = Frame(self.notebook, bg=self.bg_color) 
        self.notebook.add(self.check_investment_frame, text="Check Expenditure") 
        self.create_check_investment_page() 

        self.check_all_investment_frame = Frame(self.notebook, bg=self.bg_color) 
        self.notebook.add(self.check_all_investment_frame, text="Check ALL Expenditures") 
        self.create_check_all_investment_page() 

    def create_add_item_page(self):
        self.items = [] 
        self.prices = []
        self.date = StringVar()

        Label(self.add_item_frame, text="Personal Expenditure Manager", font=self.label_font, bg=self.label_bg, fg=self.label_fg).pack(fill="x", pady=(10, 20)) 

        entry_frame = Frame(self.add_item_frame, bg=self.bg_color)  
        entry_frame.pack(pady=10)

        for i in range(11):
            item_label = Label(entry_frame, text=f"Item {i+1}", font=self.label_font, bg=self.bg_color, fg="blue") 
            item_label.grid(row=i, column=0, padx=(20, 10), pady=5)
            item_var = StringVar()
            self.items.append(item_var) 
            Entry(entry_frame, textvariable=item_var, font=self.entry_font, width=20).grid(row=i, column=1, padx=10, pady=5) 

            price_label = Label(entry_frame, text="Price", font=self.label_font, bg=self.bg_color, fg="blue") 
            price_label.grid(row=i, column=2, padx=(20, 10), pady=5)
            price_var = StringVar()
            self.prices.append(price_var) 
            Entry(entry_frame, textvariable=price_var, font=self.entry_font, width=10).grid(row=i, column=3, padx=10, pady=5) 

        Label(self.add_item_frame, text="Date", font=self.label_font, bg=self.bg_color, fg="blue").pack(pady=10) 
        Entry(self.add_item_frame, textvariable=self.date, font=self.entry_font, width=20).pack(pady=5) 

        Button(self.add_item_frame, text="Submit", command=self.submit, bg=self.button_color, fg="white", font=self.label_font).pack(pady=10) 
        Button(self.add_item_frame, text="Clear", command=self.clear_add_item_page, bg=self.button_color, fg="white", font=self.label_font).pack() 

    def clear_add_item_page(self):
        for item_var, price_var in zip(self.items, self.prices):
            item_var.set("")
            price_var.set("")
        self.date.set("")

    def submit(self):
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS investments
                     (id INTEGER PRIMARY KEY,
                      item TEXT,
                      price REAL,
                      date TEXT)''')
        for item_var, price_var in zip(self.items, self.prices):
            item = item_var.get() 
            price = price_var.get()
            date = self.date.get()
            if item and price: 
                c.execute("INSERT INTO investments (item, price, date) VALUES (?, ?, ?)", (item, float(price), date))
        conn.commit()
        conn.close()
        self.print_all_investments()
        messagebox.showinfo("Success", "Data saved successfully.") 

    def create_check_investment_page(self):
        self.from_date = StringVar() 
        self.to_date = StringVar() 

        check_frame = Frame(self.check_investment_frame, bg=self.bg_color) 
        check_frame.pack(pady=20)

        Button(check_frame, text="Check Expenditures", command=self.show_investments, bg=self.button_color, fg="white", font=self.label_font).grid(row=0, column=0, padx=(20, 10)) 

        Label(check_frame, text="From Date", font=self.label_font, bg=self.bg_color, fg="blue").grid(row=0, column=1) 
        Entry(check_frame, textvariable=self.from_date, font=self.entry_font).grid(row=0, column=2) 

        Label(check_frame, text="To Date", font=self.label_font, bg=self.bg_color, fg="blue").grid(row=0, column=3)
        Entry(check_frame, textvariable=self.to_date, font=self.entry_font).grid(row=0, column=4)

        table_frame = Frame(self.check_investment_frame, bg=self.bg_color) 
        table_frame.pack(pady=20)
        self.table = ttk.Treeview(table_frame, columns=("Item", "Price", "Date")) 
        self.table.heading("#0", text="ID")
        self.table.heading("Item", text="Item")
        self.table.heading("Price", text="Price")
        self.table.heading("Date", text="Date")
        self.table.pack()

        self.total_label = Label(self.check_investment_frame, text="", font=self.label_font, bg=self.bg_color) 
        self.total_label.pack(pady=10)
        Button(self.check_investment_frame, text="Clear", command=self.clear_check_investment_page, bg=self.button_color, fg="white", font=self.label_font).pack() 

    def clear_check_investment_page(self):
        self.from_date.set("")
        self.to_date.set("")
        for row in self.table.get_children():
            self.table.delete(row)
        self.total_label.config(text="")

    def show_investments(self):
        from_date = self.from_date.get() 
        to_date = self.to_date.get()

        conn = sqlite3.connect('investments.db') 
        c = conn.cursor()
        c.execute("SELECT * FROM investments WHERE date BETWEEN ? AND ?", (from_date, to_date)) 
        investments = c.fetchall()
        conn.close()
        for row in self.table.get_children():
            self.table.delete(row) 

        total = 0 
        for idx, investment in enumerate(investments): 
            self.table.insert(parent='', index='end', iid=idx, text=idx, values=(investment[1], investment[2], investment[3])) 
            total += investment[2] 

        self.total_label.config(text=f"Total expenditure: {total}") 

    def create_check_all_investment_page(self):
        table_frame_all = Frame(self.check_all_investment_frame, bg=self.bg_color)
        table_frame_all.pack(pady=20)

        self.all_text = Text(table_frame_all, height=20, width=90, state=DISABLED, font=self.text_font)
        self.all_text.pack(pady=10)

        all_label = Label(self.check_all_investment_frame, text="Available Expenditures", font=("Arial", 14, "bold"), bg=self.label_bg, fg=self.label_fg)
        all_label.pack()

        delete_frame = LabelFrame(self.check_all_investment_frame, text="Delete Expenditure", padx=10, pady=10, bg=self.bg_color)
        delete_frame.pack(pady=20)

        delete_label = Label(delete_frame, text="Expenditure ID:", font=self.label_font, bg=self.bg_color, fg="blue")
        delete_label.grid(row=0, column=0)

        self.delete_entry = Entry(delete_frame, font=self.entry_font)
        self.delete_entry.grid(row=0, column=1)

        delete_button = Button(delete_frame, text="Delete Expenditure", command=self.delete_investment, bg=self.button_color, fg="white", font=self.label_font)
        delete_button.grid(row=1, column=0, columnspan=2)
        self.print_all_investments()

    def print_all_investments(self):
        conn = sqlite3.connect('investments.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM investments")
        investments = cursor.fetchall()
        conn.close()

        self.all_text.config(state=NORMAL)
        self.all_text.delete('1.0', END)

        if investments:
            self.all_text.insert(END, "Available List of Expenditures:\n")
            for i in investments:
                self.all_text.insert(END, f"\nID: {i[0]}\nItem: {i[1]}\nPrice: {i[2]}\nDate: {i[3]}\n")
        else:
            self.all_text.insert(END, "No expenditure records available.")

        self.all_text.config(state=DISABLED)

    def delete_investment(self):
        try:
            investment_id = int(self.delete_entry.get())
            conn = sqlite3.connect('investments.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM investments WHERE id=?", (investment_id,))
            investment = cursor.fetchone()

            if investment:
                cursor.execute("DELETE FROM investments WHERE id=?", (investment_id,))
                conn.commit()
                messagebox.showinfo("Success", "Expenditure deleted successfully!")
                self.print_all_investments()  
            else:
                messagebox.showerror("Invalid ID", "The entered ID does not exist.")
        except ValueError:
            messagebox.showerror("Invalid ID", "Please enter a valid numeric ID.")

def main():
    app = Tk()
    PEM(app)
    app.mainloop()

if __name__ == "__main__":
    main()
