import hashlib
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel

# Database Setup with Security
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('secure_app.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_tables(self):
        # Client table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Product table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transaction table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_code TEXT UNIQUE NOT NULL,
                client_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(client_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        self.conn.commit()
    
    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return False
    
    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

db = Database()

# Main Application Class
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Management System")
        self.root.geometry("1300x750")
        self.root.configure(bg='#f0f4f8')
        
        # Set style
        self.setup_style()
        self.create_widgets()
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#f0f4f8', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TFrame', background='#f0f4f8')
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e66')
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), foreground='#1a4d8c')
    
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)
        ttk.Label(header_frame, text="📊 Business Management System", style='Title.TLabel').pack()
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_search_tab()
        self.create_clients_tab()
        self.create_products_tab()
        self.create_transactions_tab()
    
    def create_search_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Search")
        
        # Search Frame
        search_frame = ttk.LabelFrame(tab, text="Search Criteria", padding=10)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.search_name = ttk.Entry(search_frame, width=30, font=('Segoe UI', 10))
        self.search_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Code:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.search_code = ttk.Entry(search_frame, width=30, font=('Segoe UI', 10))
        self.search_code.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.search_date = ttk.Entry(search_frame, width=30, font=('Segoe UI', 10))
        self.search_date.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(search_frame, text="🔎 Search", command=self.perform_search, style='TButton').grid(row=1, column=2, padx=10, pady=5)
        ttk.Button(search_frame, text="🗑 Clear", command=self.clear_search).grid(row=1, column=3, padx=5, pady=5)
        
        # Results Frame
        results_frame = ttk.LabelFrame(tab, text="Search Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for results
        columns = ('ID', 'Type', 'Name/Product', 'Code', 'Date')
        self.result_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def perform_search(self):
        # Clear previous results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        name = self.search_name.get().strip()
        code = self.search_code.get().strip()
        date = self.search_date.get().strip()
        
        # Search in clients
        if name:
            clients = db.fetch_all("SELECT client_id, name, email, phone, created_at FROM clients WHERE name LIKE ?", (f'%{name}%',))
            for client in clients:
                self.result_tree.insert('', 'end', values=(client[0], 'Client', client[1], client[2], client[4]))
        
        # Search in products
        if code:
            products = db.fetch_all("SELECT product_id, code, name, price, created_at FROM products WHERE code LIKE ?", (f'%{code}%',))
            for product in products:
                self.result_tree.insert('', 'end', values=(product[0], 'Product', product[2], product[1], product[4]))
        
        # Search by date in transactions
        if date:
            transactions = db.fetch_all("SELECT transaction_id, transaction_code, client_id, product_id, transaction_date FROM transactions WHERE transaction_date LIKE ?", (f'%{date}%',))
            for trans in transactions:
                self.result_tree.insert('', 'end', values=(trans[0], 'Transaction', f"Trans: {trans[1]}", f"Client:{trans[2]},Prod:{trans[3]}", trans[4]))
        
        if not name and not code and not date:
            messagebox.showwarning("Attention", "Please enter at least one search criterion!")
        
        if len(self.result_tree.get_children()) == 0 and (name or code or date):
            messagebox.showinfo("No Results", "No matching records found.")
    
    def clear_search(self):
        self.search_name.delete(0, tk.END)
        self.search_code.delete(0, tk.END)
        self.search_date.delete(0, tk.END)
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
    
    def create_clients_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Clients")
        
        # Form Frame
        form_frame = ttk.LabelFrame(tab, text="Client Registration Form", padding=15)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Full Name:*").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.client_name = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        self.client_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:*").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.client_email = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        self.client_email.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.client_phone = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        self.client_phone.grid(row=2, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="➕ Add Client", command=self.add_client).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑 Delete Selected", command=self.delete_client).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.load_clients).pack(side='left', padx=5)
        
        # List Frame
        list_frame = ttk.LabelFrame(tab, text="Clients List", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Name', 'Email', 'Phone', 'Created Date')
        self.client_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.client_tree.heading(col, text=col)
            self.client_tree.column(col, width=180)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=scrollbar.set)
        self.client_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_clients()
    
    def load_clients(self):
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        clients = db.fetch_all("SELECT * FROM clients ORDER BY client_id DESC")
        for client in clients:
            self.client_tree.insert('', 'end', values=client)
    
    def add_client(self):
        name = self.client_name.get().strip()
        email = self.client_email.get().strip()
        phone = self.client_phone.get().strip()
        
        if not name or not email:
            messagebox.showwarning("Attention Alert", "Name and Email are required fields!")
            return
        
        if db.execute_query("INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)", (name, email, phone)):
            messagebox.showinfo("Success", f"Client '{name}' added successfully!")
            self.client_name.delete(0, tk.END)
            self.client_email.delete(0, tk.END)
            self.client_phone.delete(0, tk.END)
            self.load_clients()
    
    def delete_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Please select a client to delete!")
            return
        
        # Confirmation dialog
        if messagebox.askyesno("Confirm Deletion", "⚠️ Are you sure you want to delete this client?\nThis action cannot be undone!"):
            item = self.client_tree.item(selected[0])
            client_id = item['values'][0]
            if db.execute_query("DELETE FROM clients WHERE client_id = ?", (client_id,)):
                messagebox.showinfo("Success", "Client deleted successfully!")
                self.load_clients()
    
    def create_products_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Products")
        
        # Form Frame
        form_frame = ttk.LabelFrame(tab, text="Product Registration Form", padding=15)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Product Code:*").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.product_code = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.product_code.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Product Name:*").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.product_name = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.product_name.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Price:*").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.product_price = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.product_price.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Stock Quantity:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.product_stock = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.product_stock.grid(row=3, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="➕ Add Product", command=self.add_product).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑 Delete Selected", command=self.delete_product).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.load_products).pack(side='left', padx=5)
        
        # List Frame
        list_frame = ttk.LabelFrame(tab, text="Products List", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Code', 'Name', 'Price ($)', 'Stock', 'Created Date')
        self.product_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        self.product_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_products()
    
    def load_products(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        products = db.fetch_all("SELECT * FROM products ORDER BY product_id DESC")
        for product in products:
            self.product_tree.insert('', 'end', values=product)
    
    def add_product(self):
        code = self.product_code.get().strip()
        name = self.product_name.get().strip()
        price = self.product_price.get().strip()
        stock = self.product_stock.get().strip() or '0'
        
        if not code or not name or not price:
            messagebox.showwarning("Attention Alert", "Code, Name, and Price are required fields!")
            return
        
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showwarning("Attention Alert", "Price must be a number and Stock must be an integer!")
            return
        
        if db.execute_query("INSERT INTO products (code, name, price, stock) VALUES (?, ?, ?, ?)", (code, name, price, stock)):
            messagebox.showinfo("Success", f"Product '{name}' added successfully!")
            self.product_code.delete(0, tk.END)
            self.product_name.delete(0, tk.END)
            self.product_price.delete(0, tk.END)
            self.product_stock.delete(0, tk.END)
            self.load_products()
    
    def delete_product(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Please select a product to delete!")
            return
        
        if messagebox.askyesno("Confirm Deletion", "⚠️ Are you sure you want to delete this product?\nThis action cannot be undone!"):
            item = self.product_tree.item(selected[0])
            product_id = item['values'][0]
            if db.execute_query("DELETE FROM products WHERE product_id = ?", (product_id,)):
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_products()
    
    def create_transactions_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💰 Transactions")
        
        # Form Frame
        form_frame = ttk.LabelFrame(tab, text="New Transaction", padding=15)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Client:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.trans_client = ttk.Combobox(form_frame, width=40)
        self.trans_client.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Product:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.trans_product = ttk.Combobox(form_frame, width=40)
        self.trans_product.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Quantity:*").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.trans_quantity = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        self.trans_quantity.grid(row=2, column=1, padx=5, pady=5)
        
        self.load_combos()
        
        ttk.Button(form_frame, text="💵 Create Transaction", command=self.add_transaction).grid(row=3, column=0, columnspan=2, pady=10)
        
        # List Frame
        list_frame = ttk.LabelFrame(tab, text="Transaction History", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Transaction Code', 'Client', 'Product', 'Quantity', 'Total ($)', 'Date')
        self.trans_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.trans_tree.yview)
        self.trans_tree.configure(yscrollcommand=scrollbar.set)
        self.trans_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_transactions()
    
    def load_combos(self):
        clients = db.fetch_all("SELECT client_id, name FROM clients")
        self.trans_client['values'] = [f"{c[0]} - {c[1]}" for c in clients]
        
        products = db.fetch_all("SELECT product_id, name, price FROM products")
        self.trans_product['values'] = [f"{p[0]} - {p[1]} (${p[2]})" for p in products]
    
    def add_transaction(self):
        client_val = self.trans_client.get()
        product_val = self.trans_product.get()
        quantity = self.trans_quantity.get().strip()
        
        if not client_val or not product_val or not quantity:
            messagebox.showwarning("Attention Alert", "Please fill all fields!")
            return
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Attention Alert", "Quantity must be a positive integer!")
            return
        
        client_id = int(client_val.split(' - ')[0])
        product_id = int(product_val.split(' - ')[0])
        
        product_info = db.fetch_all("SELECT price, name FROM products WHERE product_id = ?", (product_id,))
        if not product_info:
            messagebox.showerror("Error", "Product not found!")
            return
        
        price = product_info[0][0]
        total = price * quantity
        trans_code = f"TRX-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if db.execute_query("INSERT INTO transactions (transaction_code, client_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?, ?)",
                          (trans_code, client_id, product_id, quantity, total)):
            messagebox.showinfo("Success", f"Transaction completed!\nTotal: ${total:.2f}\nCode: {trans_code}")
            self.trans_quantity.delete(0, tk.END)
            self.load_transactions()
    
    def load_transactions(self):
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)
        
        query = '''
            SELECT t.transaction_id, t.transaction_code, c.name, p.name, t.quantity, t.total_price, t.transaction_date
            FROM transactions t
            JOIN clients c ON t.client_id = c.client_id
            JOIN products p ON t.product_id = p.product_id
            ORDER BY t.transaction_id DESC
        '''
        transactions = db.fetch_all(query)
        for trans in transactions:
            self.trans_tree.insert('', 'end', values=trans)

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()