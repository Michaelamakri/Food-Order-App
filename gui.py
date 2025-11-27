
import tkinter as tk
from tkinter import messagebox
from database_manager import DatabaseManager
class gui(tk.Frame):
    def __init__(self,root):
        self.root=root
        self.cart=[]
        root.configure(bg="#74AF74")
        root.geometry("600x700")
        root.resizable(True,True)
        self.db = DatabaseManager() 
        self.CreateMainScreen() 

    def CreateMainScreen(self):
        tk.Label(self.root, text="Welcome to FoodApp",bg="#74AF74", font=("Arial", 22, "bold")).pack(pady=10) 
        tk.Button(self.root, text="Log In", width=20, height=2, command=self.login_window).pack(pady=10)
        tk.Button(self.root, text="Sign Up", width=20, height=2, command=self.signup_window).pack(pady=10)
   

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
   
    
    def signup_window(self):
        self.clear_window()
        self.root.title("Sign Up")

        labels = [
            "Name", "Email", "Phone", "Password", "Age",
            "Country", "City", "Region"
        ]
        entries = {}

        for label in labels:
            tk.Label(self.root, text=f"{label}:").pack()
            entry = tk.Entry(self.root, show="*" if label =="Password" else None)
            entry.pack()
            entries[label] = entry

        def signup_action():
            data = {label: entry.get().strip() for label, entry in entries.items()}
            for label in labels:
                data

            if not all(data.values()):
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            try:
                self.db.execute("""
                    INSERT INTO users (name, email, phone, password, age, country, city, region)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["Name"], data["Email"], data["Phone"], data["Password"],
                    data["Age"], data["Country"], data["City"], data["Region"]
                ))
                messagebox.showinfo("Success", "Account created successfully!")
                
                
                
            except Exception as e:
                messagebox.showerror("Database Error ","{e}")

        tk.Button(self.root, text="Sign Up", command=signup_action).pack(pady=20)
     
    def login_window(self):
        self.clear_window()
        self.root.title("Log In")
        tk.Label(self.root, text="Email:").pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        pass_entry = tk.Entry(self.root, show="*")
        pass_entry.pack()
        def login_action(event=None):  
            email = email_entry.get().strip()
            password = pass_entry.get().strip()
            if not  email or not password:
                messagebox.showwarning("Warning", "Please fill all fields.")
                return
            user = self.db.fetchall(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, password)
                )
            if user:
                name = user[0][1]
                city = user[0][7] 
                messagebox.showinfo("Welcome", f"Welcome back, {name}!")
                
                self.clear_window()
                self.show_restaurants_screen(name,city)
            else:
                messagebox.showerror("Error", "Invalid email or password")
                
        tk.Button(self.root, text="Log In", command=login_action).pack(pady=20)
        self.root.bind("<Return>", login_action)
        email_entry.focus_set()
    
    def show_restaurants_screen(self, username,usercity):
        tk.Label(self.root,text=f"Welcome, {username}!",font=("Arial",14),bg="#74AF74").pack(pady=10)
        tk.Label(self.root,text="Available restaurants:",font=("Arial",14),bg="#74AF74").pack(pady=10)
        restaurants =self.db.fetchall(
            "SELECT name FROM restaurants WHERE city=?",
            (usercity,)
            )
        if restaurants==[]:
            tk.Label(self.root,text="No restaurants",bg="#74AF74").pack(pady=10)
        else:
            for rest in restaurants:
                tk.Button(self.root,text=rest[0],bg="#74AF74",width=25,height=2,command=lambda r=rest[0]: self.open_menu(r)).pack(pady=10)
    def add_to_cart(self, name, price):
        self.cart.append((name, price))
        messagebox.showinfo("Cart", f"Added {name} to cart!")
    def open_menu(self, restaurant_name):
        self.clear_window()
        account_btn = tk.Button(self.root, text="👤",font=("Arial", 18),bg="#74AF74",relief="flat",
        command=lambda: self.open_profile_sidebar("User")   # ή πέρασε username αν το κρατάς κάπου
    )
        account_btn.place(relx=0.95, rely=0.02, anchor="ne")
        tk.Label(self.root,text=f"Menu of {restaurant_name}",font=("Arial", 22, "bold"),bg="#74AF74").pack(pady=10)

        menu_items = self.db.fetchall("""
        SELECT item_name, price FROM menu
        WHERE rest_id = (
            SELECT rest_id FROM restaurants WHERE name = ?
        )
    """, (restaurant_name,))

        if menu_items==[]:
            tk.Label(self.root, text="No items found.", bg="#74AF74").pack(pady=10)
            return
        for item_name, price in menu_items:
            frame = tk.Frame(self.root, bg="#74AF74")
            frame.pack(pady=5)
            tk.Label(frame, text=f"{item_name} price:{price}€", bg="#74AF74").pack(side="left", padx=10)
            tk.Button(frame, text="Add to Cart",command=lambda n=item_name, p=price: self.add_to_cart(n, p)).pack(side="right")
    def open_profile_sidebar(self, username):
        
        self.sidebar = tk.Frame(self.root, bg="white", width=250, height=self.root.winfo_height())
        self.sidebar.place(relx=1.0, y=0, anchor="ne")
        tk.Label(self.sidebar, text=username, font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        options = [
        ("Εισερχόμενα μηνύματα", self.fake_page),
        ("Ο λογαριασμός μου", self.fake_page),
        ("Παραγγελίες", self.fake_page),
        ("Διευθύνσεις", self.fake_page),
        ]
        for text, action in options:
            btn = tk.Button(self.sidebar, text=text, anchor="w",relief="flat", bg="white", font=("Arial", 12),command=action
        )
            btn.pack(fill="x", pady=5, padx=15)
            tk.Button(self.sidebar, text="Κλείσιμο", bg="#FF5555", fg="white",command=self.sidebar.destroy).pack(pady=20)
    def fake_page(self):
        messagebox.showinfo("Info", "Αυτή η σελίδα δεν είναι έτοιμη ακόμη.")


   
