
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import mysql.connector
from mysql.connector import IntegrityError, Error

# -----------------------------------------
# DATABASE CONFIGURATION
# -----------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Alancrzs@09",  # Enter your actual MySQL password
    "database": "warrantyvault"
}

# Demo user created in the database
USER_ID = 1


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


# -----------------------------------------
# MAIN APPLICATION
# -----------------------------------------
class WarrantyVault:
    def __init__(self, root):
        self.root = root
        self.root.title("WarrantyVault - Warranty Tracker")
        self.root.geometry("1200x740")
        self.root.minsize(950, 650)

        self.selected_product_id = None

        self.create_widgets()
        self.load_products()

    # -------------------------------------
    # CREATE GUI
    # -------------------------------------
    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="WarrantyVault",
            font=("Arial", 25, "bold")
        )
        title.pack(pady=(15, 2))

        subtitle = tk.Label(
            self.root,
            text="Personal Warranty and Repair Tracker",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 18))

        # Product form
        form = ttk.LabelFrame(
            self.root,
            text="Product Details",
            padding=15
        )
        form.pack(fill="x", padx=15, pady=5)

        self.product_name = tk.StringVar()
        self.brand = tk.StringVar()
        self.serial_number = tk.StringVar()
        self.purchase_date = tk.StringVar(value=date.today().isoformat())
        self.purchase_price = tk.StringVar(value="0")
        self.warranty_months = tk.StringVar(value="12")

        fields = [
            ("Product Name", self.product_name),
            ("Brand", self.brand),
            ("Serial Number", self.serial_number),
            ("Purchase Date (YYYY-MM-DD)", self.purchase_date),
            ("Purchase Price", self.purchase_price),
            ("Warranty Months", self.warranty_months)
        ]

        for index, (label_text, variable) in enumerate(fields):
            row = index // 3
            col = index % 3

            field_frame = ttk.Frame(form)
            field_frame.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=10,
                pady=7
            )

            ttk.Label(
                field_frame,
                text=label_text
            ).pack(anchor="w")

            ttk.Entry(
                field_frame,
                textvariable=variable,
                width=30
            ).pack(fill="x", pady=(5, 0))

        for col in range(3):
            form.columnconfigure(col, weight=1)

        # Buttons
        button_frame = ttk.Frame(form)
        button_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=(12, 5)
        )

        ttk.Button(
            button_frame,
            text="Add Product",
            command=self.add_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Update Selected",
            command=self.update_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Load Sample Product",
            command=self.load_sample_product
        ).pack(side="left", padx=5)

        # Search area
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=15, pady=12)

        ttk.Label(
            search_frame,
            text="Search:"
        ).pack(side="left", padx=(0, 10))

        self.search_text = tk.StringVar()

        ttk.Entry(
            search_frame,
            textvariable=self.search_text,
            width=32
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_products
        ).pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.load_products
        ).pack(side="left", padx=5)

        # Product table
        table_frame = ttk.Frame(self.root)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columns = (
            "id",
            "product",
            "brand",
            "serial",
            "purchase_date",
            "expiry",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14
        )

        headings = {
            "id": "ID",
            "product": "Product",
            "brand": "Brand",
            "serial": "Serial Number",
            "purchase_date": "Purchase Date",
            "expiry": "Warranty Expiry",
            "status": "Status"
        }

        widths = {
            "id": 55,
            "product": 170,
            "brand": 130,
            "serial": 150,
            "purchase_date": 130,
            "expiry": 130,
            "status": 120
        }

        for column in columns:
            self.tree.heading(
                column,
                text=headings[column]
            )
            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_product
        )

        # Status bar
        self.status_label = ttk.Label(
            self.root,
            text="Ready",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=15, pady=(0, 8))

    # -------------------------------------
    # LOAD SAMPLE DETAILS INTO FORM
    # -------------------------------------
    def load_sample_product(self):
        self.clear_form()

        self.product_name.set("Laptop")
        self.brand.set("HP")
        self.serial_number.set("HP-WV-001")
        self.purchase_date.set("2026-10-26")
        self.purchase_price.set("55000")
        self.warranty_months.set("12")

        self.status_label.config(
            text="Sample laptop details loaded. Click Add Product to save."
        )

    # -------------------------------------
    # VALIDATE FORM DATA
    # -------------------------------------
    def get_form_data(self):
        name = self.product_name.get().strip()
        brand = self.brand.get().strip()
        serial = self.serial_number.get().strip()
        purchase_date = self.purchase_date.get().strip()

        if not name or not brand or not serial:
            messagebox.showwarning(
                "Missing Details",
                "Please enter the product name, brand, and serial number."
            )
            return None

        try:
            parsed_date = datetime.strptime(
                purchase_date,
                "%Y-%m-%d"
            ).date()

            if parsed_date > date.today():
                messagebox.showwarning(
                    "Invalid Date",
                    "Purchase date cannot be in the future."
                )
                return None

            price = float(self.purchase_price.get())
            months = int(self.warranty_months.get())

            if price < 0:
                raise ValueError("Price cannot be negative.")

            if months < 0:
                raise ValueError("Warranty months cannot be negative.")

        except ValueError:
            messagebox.showerror(
                "Invalid Details",
                "Enter a valid date (YYYY-MM-DD), non-negative price, "
                "and whole-number warranty months."
            )
            return None

        return (
            name,
            brand,
            serial,
            parsed_date,
            price,
            months
        )

    # -------------------------------------
    # ADD PRODUCT
    # -------------------------------------
    def add_product(self):
        data = self.get_form_data()

        if data is None:
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
                INSERT INTO products
                (user_id, product_name, brand, serial_number,
                 purchase_date, purchase_price, warranty_months)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (USER_ID,) + data
            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo(
                "Success",
                "Product added successfully!"
            )

            self.clear_form()
            self.load_products()

        except IntegrityError:
            if conn:
                conn.rollback()

            messagebox.showerror(
                "Duplicate Serial Number",
                "This serial number already exists. Please use a unique one."
            )

        except Error as error:
            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # -------------------------------------
    # LOAD PRODUCTS
    # -------------------------------------
    def load_products(self):
        self.display_products(search_term=None)

    # -------------------------------------
    # SEARCH PRODUCTS
    # -------------------------------------
    def search_products(self):
        term = self.search_text.get().strip()
        self.display_products(search_term=term)

    # -------------------------------------
    # DISPLAY PRODUCTS
    # -------------------------------------
    def display_products(self, search_term=None):
        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
                SELECT
                    product_id,
                    product_name,
                    brand,
                    serial_number,
                    purchase_date,
                    DATE_ADD(
                        purchase_date,
                        INTERVAL warranty_months MONTH
                    ) AS warranty_expiry
                FROM products
                WHERE user_id = %s
            """

            values = [USER_ID]

            if search_term:
                query += """
                    AND (
                        product_name LIKE %s
                        OR brand LIKE %s
                        OR serial_number LIKE %s
                    )
                """
                pattern = "%" + search_term + "%"
                values.extend([pattern, pattern, pattern])

            query += " ORDER BY product_id DESC"

            cursor.execute(query, tuple(values))
            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in rows:
                product_id, name, brand, serial, purchase, expiry = row

                status = self.get_status(expiry)

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        product_id,
                        name,
                        brand,
                        serial,
                        purchase,
                        expiry,
                        status
                    )
                )

            self.status_label.config(
                text=f"Products displayed: {len(rows)}"
            )

        except Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # -------------------------------------
    # CALCULATE WARRANTY STATUS
    # -------------------------------------
    @staticmethod
    def get_status(expiry_date):
        if expiry_date is None:
            return "Unknown"

        if isinstance(expiry_date, datetime):
            expiry_date = expiry_date.date()

        if expiry_date >= date.today():
            return "Active"

        return "Expired"

    # -------------------------------------
    # SELECT PRODUCT FROM TABLE
    # -------------------------------------
    def select_product(self, event=None):
        selection = self.tree.selection()

        if not selection:
            return

        values = self.tree.item(
            selection[0],
            "values"
        )

        self.selected_product_id = int(values[0])

        self.product_name.set(values[1])
        self.brand.set(values[2])
        self.serial_number.set(values[3])
        self.purchase_date.set(str(values[4]))

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT purchase_price, warranty_months
                FROM products
                WHERE product_id = %s AND user_id = %s
                """,
                (self.selected_product_id, USER_ID)
            )

            row = cursor.fetchone()

            if row:
                self.purchase_price.set(str(row[0]))
                self.warranty_months.set(str(row[1]))

        except Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # -------------------------------------
    # UPDATE PRODUCT
    # -------------------------------------
    def update_product(self):
        if self.selected_product_id is None:
            messagebox.showwarning(
                "Select Product",
                "Please select a product from the table first."
            )
            return

        data = self.get_form_data()

        if data is None:
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
                UPDATE products
                SET product_name = %s,
                    brand = %s,
                    serial_number = %s,
                    purchase_date = %s,
                    purchase_price = %s,
                    warranty_months = %s
                WHERE product_id = %s AND user_id = %s
            """

            values = data + (
                self.selected_product_id,
                USER_ID
            )

            cursor.execute(query, values)
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Not Updated",
                    "No product was updated. Check your selection."
                )
            else:
                messagebox.showinfo(
                    "Success",
                    "Product updated successfully!"
                )

            self.clear_form()
            self.load_products()

        except IntegrityError:
            if conn:
                conn.rollback()

            messagebox.showerror(
                "Duplicate Serial Number",
                "Another product already uses this serial number."
            )

        except Error as error:
            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # -------------------------------------
    # DELETE PRODUCT
    # -------------------------------------
    def delete_product(self):
        if self.selected_product_id is None:
            messagebox.showwarning(
                "Select Product",
                "Please select a product from the table first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this product?"
        )

        if not confirm:
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM products
                WHERE product_id = %s AND user_id = %s
                """,
                (self.selected_product_id, USER_ID)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Product deleted successfully!"
            )

            self.clear_form()
            self.load_products()

        except Error as error:
            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                "Could not delete the product. If it has repair-history "
                "records, those may need to be removed first.\n\n"
                + str(error)
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # -------------------------------------
    # CLEAR FORM
    # -------------------------------------
    def clear_form(self):
        self.selected_product_id = None

        self.product_name.set("")
        self.brand.set("")
        self.serial_number.set("")
        self.purchase_date.set(date.today().isoformat())
        self.purchase_price.set("0")
        self.warranty_months.set("12")

        if hasattr(self, "tree"):
            for item in self.tree.selection():
                self.tree.selection_remove(item)

        self.status_label.config(text="Ready")


# -----------------------------------------
# RUN APPLICATION
# -----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WarrantyVault(root)
    root.mainloop()
