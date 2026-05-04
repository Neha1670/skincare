import os
import base64
import cv2
import numpy as np
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "supersecretkey"
import pandas as pd

from flask import Flask, render_template

import pandas as pd
from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            flash("Admin login required 🔒", "error")
            return redirect(url_for("adminneha"))
        return f(*args, **kwargs)
    return wrapper
@app.route("/adminneha", methods=["GET", "POST"])
def adminneha():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "adminneha" and password == "12345":
            session["admin_neha"] = True   # ✅ DIFFERENT SESSION
            return redirect(url_for("dashboard"))  # 👈 IMPORTANT CHANGE
        else:
            flash("Invalid credentials ❌", "error")
            return redirect(url_for("adminneha"))

    return render_template("adminneha.html")


@app.route("/neha_logout")
def neha_logout():
    session.pop("admin_neha", None)   # only 2nd admin logout
    flash("Logged out successfully 👋", "success")
    return redirect(url_for("home"))   # ✅ HOME PAGE REDIRECT


@app.route("/dashboard")
def dashboard():

    # ✅ ONLY NEHA ADMIN CAN ACCESS
    if not session.get("admin_neha"):
        flash("Admin login required 🔒", "error")
        return redirect(url_for("adminneha"))


# ===== YEARLY REVENUE =====
    yearly_data = [
        21394, 13260, 19783, 27485,
        13149, 14260, 18021, 37691,
        23409, 54000, 14960, 18374
    ]

    yearly_revenue = sum(yearly_data)

    # ===== COSTS =====
    personal = 24000
    material = 163159
    extra = 60000

    # ===== MONTHLY MATERIAL (FROM YOUR IMAGE) =====
    material_data = [
        15304, 8965, 15690, 9726,
        15972, 13798, 10345, 32479,
        16167, 10285, 7230, 7198
    ]

    # ===== MONTHLY FIXED COST =====
    monthly_personal = 2000        # 24000 / 12
    monthly_extra = 5000          # 60000 / 12

    # ===== MONTHLY EXPENSE CALCULATION =====
    monthly_expenses = []
    for m in material_data:
        monthly_expenses.append(m + monthly_personal + monthly_extra)

    # ===== MONTHLY PROFIT =====
    monthly_profit = []
    for i in range(12):
        monthly_profit.append(yearly_data[i] - monthly_expenses[i])

    # ===== FINAL PROFIT =====
    final_profit = sum(monthly_profit)
  
    # ===== TOTAL DATA =====
    df = pd.read_excel("Pumpkin_Clients_Data_Cleaned.xlsx")
    df.columns = df.columns.str.strip()

    total_clients = len(df)
    total_cities = df["City"].nunique()

    city_counts = df["City"].value_counts().to_dict()
    # ===== PERSON WISE PRODUCT =====
    df = pd.read_excel("bothcombine.xlsx")
    df.columns = df.columns.str.strip()
    df["Product"] = df["Product"].astype(str)
    df["Product_List"] = df["Product"].str.split(",")

    df_exploded = df.explode("Product_List")
    df_exploded["Product_List"] = df_exploded["Product_List"].str.strip()

# count per person
    person_summary = df_exploded.groupby("Name")["Product_List"].count().reset_index()

# top 10
    person_summary = person_summary.sort_values(by="Product_List", ascending=False).head(10)

    person_names = person_summary["Name"].tolist()
    person_counts = person_summary["Product_List"].tolist()
    
    # ===== JANUARY DATA =====
    jan_df = pd.read_excel("client data january 2026.xlsx")

    jan_df.columns = jan_df.columns.str.strip()

    jan_df = jan_df.iloc[:, :4]
    jan_df.columns = ["Total_no", "Name", "City", "Price"]

    jan_city_counts = jan_df["City"].value_counts().to_dict()

    # ⭐ January total clients
    jan_total = len(jan_df)


    # ===== FEBRUARY DATA =====
    feb_df = pd.read_excel("Feb Data 2026.xlsx")

    feb_df.columns = feb_df.columns.str.strip()

    feb_df = feb_df.iloc[:, :4]
    feb_df.columns = ["Total_no", "Name", "City", "Price"]

    feb_city_counts = feb_df["City"].value_counts().to_dict()

    # ⭐ February total clients
    feb_total = len(feb_df)
    # ===== GROWTH CALCULATION =====
    if jan_total > 0:
        growth = ((feb_total - jan_total) / jan_total) * 100
    else:
        growth = 0


# ===== TOP CITY =====
    top_city = max(city_counts, key=city_counts.get)
    top_count = city_counts[top_city]


    # ===== CITY COORDINATES =====
    city_coordinates = {
        "Rewa": {"lat": 24.5362, "lng": 81.3037},
        "Satna": {"lat": 24.6005, "lng": 80.8322},
        "Bhopal": {"lat": 23.2599, "lng": 77.4126},
        "Jabalpur": {"lat": 23.1815, "lng": 79.9864},
        "Katni": {"lat": 23.8343, "lng": 80.3940},
        "Raipur": {"lat": 21.2514, "lng": 81.6296},
        "Kota": {"lat": 25.2138, "lng": 75.8648},
        "Mandla": {"lat": 22.5970, "lng": 80.3710},
        "Balaghat": {"lat": 21.8129, "lng": 80.1880},
        "Nagod": {"lat": 24.5700, "lng": 80.5900},
        "Gujarat": {"lat": 23.0225, "lng": 72.5714},
        "Maharashtra": {"lat": 19.0760, "lng": 72.8777}
    }


    # ===== TOTAL LOCATIONS =====
    locations = []

    for city, count in city_counts.items():
        if city in city_coordinates:
            locations.append({
                "city": city,
                "lat": city_coordinates[city]["lat"],
                "lng": city_coordinates[city]["lng"],
                "count": count
            })


    # ===== JAN LOCATIONS =====
    jan_locations = []

    for city, count in jan_city_counts.items():
        if city in city_coordinates:
            jan_locations.append({
                "city": city,
                "lat": city_coordinates[city]["lat"],
                "lng": city_coordinates[city]["lng"],
                "count": count
            })


    # ===== FEB LOCATIONS =====
    feb_locations = []

    for city, count in feb_city_counts.items():
        if city in city_coordinates:
            feb_locations.append({
                "city": city,
                "lat": city_coordinates[city]["lat"],
                "lng": city_coordinates[city]["lng"],
                "count": count
            })


    clients = df.to_dict(orient="records")


    return render_template (
    "dashboard.html",
    total_clients=total_clients,
    total_cities=total_cities,
    jan_total=jan_total,
    feb_total=feb_total,
    locations=locations,
    jan_locations=jan_locations,
    feb_locations=feb_locations,
    clients=clients,

    # KPI
    final_profit=final_profit,
    yearly_revenue=yearly_revenue,

    # Charts
    yearly_data=yearly_data,
    monthly_profit=monthly_profit,
    monthly_expenses=monthly_expenses,   # 🔥 YE LINE ADD KARO
    # 🔥 NEW ADDITIONS
    growth=growth,
    top_city=top_city,
    top_count=top_count,
    person_names=person_names,
    person_counts=person_counts,
    )



@app.route('/clients')
def clients():
    try:
        # ===== MAIN DATA =====
        df_main = pd.read_excel("Pumpkin_Clients_Data_Cleaned.xlsx")
        df_main.columns = df_main.columns.str.strip()

        # ===== JAN DATA =====
        jan_df = pd.read_excel("client data january 2026.xlsx")
        jan_df.columns = jan_df.columns.str.strip()
        jan_df = jan_df.iloc[:, :4]
        jan_df.columns = ["Total_no", "Name", "City", "Price"]

        # ===== FEB DATA =====
        feb_df = pd.read_excel("Feb Data 2026.xlsx")
        feb_df.columns = feb_df.columns.str.strip()
        feb_df = feb_df.iloc[:, :4]
        feb_df.columns = ["Total_no", "Name", "City", "Price"]

        return render_template(
            "clients.html",
            clients=df_main.to_dict(orient="records"),
            jan_clients=jan_df.to_dict(orient="records"),
            feb_clients=feb_df.to_dict(orient="records")
        )

    except Exception as e:
        print("Error:", e)
        return "Error loading data"

# Allow image upload up to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # ✅ ORDERS TABLE
        c.execute('''
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            name TEXT,
            quantity INTEGER,
            total_price INTEGER,
            payment_method TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # USERS
        c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')

        # SUBSCRIPTIONS
        c.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL
        )
        ''')

        # SKIN RECORDS
        c.execute('''
        CREATE TABLE IF NOT EXISTS skin_records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            image TEXT,
            skin_type TEXT,
            brightness TEXT,
            product TEXT,
            date TEXT
        )
        ''')

        # MARQUEE
        c.execute('''
        CREATE TABLE IF NOT EXISTS marquee(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
        ''')

        c.execute("SELECT COUNT(*) FROM marquee")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO marquee (text) VALUES ('Welcome to Admin Panel!')")

        conn.commit()

    print("✅ Database initialized successfully!")
@app.route("/search")
def search():
    category = request.args.get("category", "home").lower()
    user = session.get("user")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT text FROM marquee ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    marquee_text = row[0] if row else ""
    conn.close()

    # -------- CATEGORY BASED -------- #
    if category == "home":
        products_list = featured_products + best_sellers
        template = "index.html"

    elif category == "face":
        products_list = [p for p in featured_products if p["category"] == "face"]
        template = "face.html"

    elif category == "best_seller":
        products_list = best_sellers
        template = "bestseller.html"

    elif category == "hair":
        products_list = [
            {"name": "Herbal Shampoo", "image": "h.jpg", "price": "₹899"},
            {"name": "Hair Serum", "image": "goil.jpg", "price": "₹1,200"},
            {"name": "Conditioner", "image": "slap.jpg", "price": "₹750"},
            {"name": "Oil shot", "image": "oil.jpg", "price": "₹1,100"},
            {"name": "Hair Mask", "image": "hmask.jpg", "price": "₹1,300"},
            {"name": "Leave-in Spray", "image": "sampoo.jpg", "price": "₹950"}
        ]
        template = "hair.html"

    elif category == "body":
        products_list = [
            {"name": "Body Lotion", "image": "1.jpg", "price": "₹650"},
            {"name": "Exfoliating Scrub", "image": "2.png", "price": "₹800"},
            {"name": "Moisturizing Cream", "image": "3.png", "price": "₹900"},
            {"name": "Shower Gel", "image": "4.png", "price": "₹550"},
            {"name": "Body Butter", "image": "5.png", "price": "₹1,100"},
            {"name": "Sunscreen Lotion", "image": "6.png", "price": "₹950"}
        ]
        template = "body.html"

    else:
        products_list = featured_products + best_sellers
        template = "index.html"

    return render_template(
        template,
        products=products_list,
        best_sellers=best_sellers,
        featured_products=featured_products,
        user=user,
        marquee_text=marquee_text,
        category=category
    )
    


@app.route('/')
def home():
    # ---------------- Fetch products from database ----------------
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image, price FROM products")
    db_products = cursor.fetchall()
    conn.close()

    product_list = []
    for p in db_products:
        product_list.append({
            "id": p[0],
            "name": p[1],
            "image": p[2],
            "price": p[3]
        })

    # ---------------- Combine with global featured + best sellers ----------------
    all_products = featured_products + best_sellers + product_list

    # ---------------- Marquee & user info ----------------
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT text FROM marquee ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    marquee_text = row[0] if row else ""
    conn.close()
    user = session.get("user")

    return render_template(
        "index.html",
        products=all_products,
        featured_products=featured_products,
        best_sellers=best_sellers,
        user=user,
        marquee_text=marquee_text
    )





# Cart route
@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "cart" not in session:
        session["cart"] = {}

    if request.method == "POST":
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        # Validate product_id
        try:
            pid_int = int(product_id)
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Invalid product ID"}), 400

        # Validate quantity
        try:
            qty_int = int(quantity)
            if qty_int < 1:
                qty_int = 1
        except (ValueError, TypeError):
            qty_int = 1

        # Add to session cart
        cart = session["cart"]
        if str(pid_int) in cart:
            cart[str(pid_int)] += qty_int
        else:
            cart[str(pid_int)] = qty_int
        session["cart"] = cart

        return jsonify({"success": True, "message": f"Added {qty_int} item(s) to cart"})

    # ---------------- GET METHOD ---------------- #
    items = []
    total = 0
    cart_session = session.get("cart", {})

    # Combine all products
    all_products = featured_products + best_sellers

    for pid, qty in cart_session.items():
        try:
            pid_int = int(pid)
        except ValueError:
            continue

        # Find product by id
        product = next((p for p in all_products if p.get("id") == pid_int), None)
        if product:
            price = int(str(product["price"]).replace("₹", "").replace(",", ""))
            subtotal = price * qty
            total += subtotal
            items.append({
                "id": product["id"],
                "name": product["name"],
                "price": price,
                "image": product["image"],
                "qty": qty,
                "subtotal": subtotal
            })

    return render_template("cart.html", items=items, total=total)



@app.route('/checkout', methods=['POST'])
def checkout():
    print("🔥 CHECKOUT CALLED")

    cart = session.get("cart", {})

    print("CART:", cart)

    if not cart:
        print("❌ CART EMPTY")
        return "Cart empty"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for pid, qty in cart.items():
        print("PID:", pid, "QTY:", qty)

        cursor.execute("SELECT name, price FROM products WHERE id=?", (int(pid),))
        product = cursor.fetchone()

        print("PRODUCT:", product)

        if product:
            name, price = product

            # 🔥 FIX PRICE
            price = int(str(price).replace("₹", "").replace(",", ""))

            total_price = price * int(qty)

            cursor.execute("""
                INSERT INTO orders (product_id, name, quantity, total_price, payment_method)
                VALUES (?, ?, ?, ?, ?)
            """, (int(pid), name, int(qty), total_price, "Cash on Delivery"))

            print("✅ INSERTED:", name)

        else:
            print("❌ PRODUCT NOT FOUND")

    conn.commit()
    conn.close()

    session.pop("cart", None)

    print("🎉 ORDER SUCCESS")

    return redirect(url_for('success'))

# ---------------- PRODUCT DATA (global) ---------------- #
featured_products = [
    {"id": 1, "name": "Sunblock Face Sunscreen", "image": "4.png", "price": "₹600", "category": "face"},
    {"id": 2, "name": "Eternal face serum", "image": "1.jpg", "price": "₹450", "category": "face"},
    {"id": 3, "name": "Coffee Walnut", "image": "5.png", "price": "₹350", "category": "face"},
    {"id": 4, "name": "De -Tan Pack", "image": "2.png", "price": "₹500", "category": "face"},
    {"id": 5, "name": "Serum", "image": "24k.jpg", "price": "₹600", "category": "face"},
    {"id": 6, "name": "Radiance Serum", "image": "9.png", "price": "₹400", "category": "face"},
]

best_sellers = [
    {"id": 7, "name": "Green Tea Toner", "image": "6.png", "price": "₹400", "category": "best_seller"},
    {"id": 8, "name": "Multi Vitamin", "image": "m.png", "price": "₹500", "category": "best_seller"},
    {"id": 9, "name": "Aloe vera gel ", "image": "r.png", "price": "₹425", "category": "best_seller"},
    {"id": 10, "name": "De -Tan Pack", "image": "2.png", "price": "₹500", "category": "best_seller"},
    {"id": 11, "name": "Vitamin C", "image": "11.png", "price": "₹350", "category": "best_seller"},
    {"id": 12, "name": "Sunblock Sunscreen", "image": "4.png", "price": "₹600", "category": "best_seller"},
]

   
   
@app.route("/bestseller")
def bestseller():
    return render_template("bestseller.html", best_sellers=best_sellers)

@app.route("/face")
def face():
    face_products = [p for p in featured_products if p["category"] == "face"]
    return render_template("face.html", products=face_products)



@app.route("/body")
def body():
    body_products = [
        {"name": "Body Lotion", "image": "body1.jpg", "price": "₹650", "category": "body"},
        {"name": "Exfoliating Scrub", "image": "body2.jpg", "price": "₹800", "category": "body"},
        {"name": "Moisturizing Cream", "image": "body3.jpg", "price": "₹900", "category": "body"},
        {"name": "Shower Gel", "image": "body4.jpg", "price": "₹550", "category": "body"},
        {"name": "Body Butter", "image": "body5.jpg", "price": "₹1,100", "category": "body"},
        {"name": "Sunscreen Lotion", "image": "body6.jpg", "price": "₹950", "category": "body"}
    ]
    return render_template("body.html", products=body_products)

# ---------------- ROUTES ---------------- #




@app.route("/get_marquee")
def get_marquee():
    """Return latest marquee instantly (AJAX fetch)"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT text FROM marquee ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            if row and row[0]:
                return {"text": row[0]}
    except Exception as e:
        print("⚠️ Marquee fetch error:", e)
    return {"text": "🎃 Welcome to Pumpkin SkinCare! Glow Naturally, Shine Confidently ✨"}



# About Us route
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and password required!", "error")
        return redirect(url_for("home"))

    hashed_password = generate_password_hash(password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        session["user"] = username
        flash(f"Signup successful! Welcome, {username} 🎉", "success")
    except sqlite3.IntegrityError:
        flash("Username already exists. Try another!", "error")

    return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Optional admin hardcoded credential
    if username == "admin" and password == "admin123":
        session["admin"] = True
        flash("Welcome, Admin 👑", "success")
        return redirect(url_for("admin_dashboard"))

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        row = c.fetchone()

    if row and check_password_hash(row[0], password):
        session["user"] = username
        flash(f"Welcome back, {username} 😊", "success")
    else:
        flash("Invalid username or password!", "error")

    return redirect(url_for("home"))
os.makedirs("uploads", exist_ok=True)


@app.route("/live_analyzer")
def live_analyzer():
    return render_template("live_analyzer.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("image")  # ✅ fixed input name
    captured_data = request.form.get("captured")

    # Save uploaded file
    if file and file.filename:
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

    # Save captured camera image
    elif captured_data:
        img_data = base64.b64decode(captured_data.split(",")[1])
        filepath = os.path.join("uploads", "camera_image.jpg")
        with open(filepath, "wb") as f:
            f.write(img_data)

    else:
        flash("Please upload or capture an image!", "error")
        return redirect(url_for("live_analyzer"))

    # Run model (Dummy result for now)
    result = analyze_skin(filepath)
    products = pumpkin_products(result["skin_type"])

    return render_template("result.html", result=result, products=products)


def analyze_skin(filepath):
    img = cv2.imread(filepath)
    if img is None:
        return {
            "skin_type": "Unknown",
            "acne_level": "Unknown",
            "dark_circles": "Unknown",
            "wrinkles": "Unknown"
        }

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    # Simple brightness-based skin type logic
    if brightness < 90:
        skin_type = "Dry"
    elif brightness < 130:
        skin_type = "Normal"
    elif brightness < 170:
        skin_type = "Combination"
    else:
        skin_type = "Oily"

    return {
        "skin_type": skin_type,
        "acne_level": "Low",     # You can make better logic later
        "dark_circles": "Moderate",
        "wrinkles": "Low"
    }


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    if not email:
        flash("Please provide an email.", "error")
        return redirect(url_for("home"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check if email already exists
    cur.execute("SELECT email FROM subscriptions WHERE email=?", (email,))
    existing_email = cur.fetchone()

    if existing_email:
        flash("You are already subscribed!", "subscribe")
        conn.close()
        return redirect(url_for("home"))

    # Insert new email
    cur.execute("INSERT INTO subscriptions (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()

    flash("Subscribed successfully! 🎉", "subscribe")
    return redirect(url_for("home"))


@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("admin"):
        flash("Admin login required!", "error")
        return redirect(url_for("home"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()

    cur.execute("SELECT id, email FROM subscriptions")
    subscriptions = cur.fetchall()

    cur.execute("SELECT * FROM skin_records")
    skin_records = cur.fetchall()

    # ✅ ORDERS FETCH
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        users=users,
        subscriptions=subscriptions,
        skin_records=skin_records,
        orders=orders
    )
@app.route("/delete_user/<int:id>", methods=["POST"])
def delete_user(id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM users WHERE id=?", (id,))
        conn.commit()
    flash("User deleted ✅", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/delete_subscribe/<int:id>", methods=["POST"])
def delete_subscribe(id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM subscriptions WHERE id=?", (id,))
        conn.commit()
    flash("Email removed ✅", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/update_user/<int:id>", methods=["GET", "POST"])
def update_user(id):
    if not session.get("admin"):
        flash("Admin login required!", "error")
        return redirect(url_for("home"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == "POST":
        new_username = request.form.get("username")
        new_password = request.form.get("password")

        if new_password:
            new_password = generate_password_hash(new_password)
            cur.execute("UPDATE users SET username=?, password=? WHERE id=?", (new_username, new_password, id))
        else:
            cur.execute("UPDATE users SET username=? WHERE id=?", (new_username, id))

        conn.commit()
        conn.close()
        flash("User updated ✅", "success")
        return redirect(url_for("admin_dashboard"))

    cur.execute("SELECT id, username FROM users WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()

    return render_template("update_user.html", user=user)

@app.route("/edit_marquee", methods=["GET", "POST"])
def edit_marquee():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == "POST":
        new_text = request.form.get("text", "")
        # Update the latest marquee row
        cur.execute(
            "UPDATE marquee SET text = ? WHERE id = (SELECT id FROM marquee ORDER BY id DESC LIMIT 1)",
            (new_text,)
        )
        conn.commit()
        conn.close()
        flash("Marquee Updated Successfully ✅")
        return redirect(url_for("edit_marquee"))

    # GET request — fetch current text
    cur.execute("SELECT text FROM marquee ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    current_text = row[0] if row else ""
    conn.close()

    return render_template("edit_marquee.html", current_text=current_text)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    # Combine all products into one list
    all_products = featured_products + best_sellers  # + face + body if needed

    # Check if product_id exists
    if 0 <= product_id < len(all_products):
        product = all_products[product_id]
    else:
        flash("Product not found!", "error")
        return redirect(url_for("home"))

    return render_template("product_detail.html", product=product)



# ---------------- REST / JSON helpers (optional) ---------------- #
@app.route("/api/users")
def api_users():
    # Example API to return users as JSON (admin only)
    if not session.get("admin"):
        return jsonify({"error": "admin required"}), 403

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users")
    users = [{"id": r[0], "username": r[1]} for r in cur.fetchall()]
    conn.close()
    return jsonify(users)


# ---------------- AI MODEL FUNCTIONS ---------------- #
def analyze_skin(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    acne = np.mean(gray) / 255
    wrinkle = np.std(gray) / 255
    dark = (255 - np.mean(gray)) / 255

    return {
        "skin_type": "Combination" if acne > 0.4 else "Dry",
        "acne_level": round(acne, 2),
        "wrinkles": round(wrinkle, 2),
        "dark_circles": round(dark, 2)
    }

def pumpkin_products(skin_type):
    data = {
        "Dry": ["Hydrating Cream", "Honey Glow Mask", "Seed Oil Serum"],
        "Combination": ["Pumpkin Face Wash", "Clay Mask", "Brightening Toner"],
        "Oily": ["Salicylic Cleanser", "Oil Control Gel", "Mattifying Moisturizer"]
    }
    return data.get(skin_type, data["Combination"])





@app.route("/logout")
def logout():
    session.clear()   # Removes admin/user session
    flash("Logged out successfully ✅")
    return redirect(url_for("home"))


@app.route('/success')
def success():
    # Define products locally if all_products is not global
    # ---------------- PRODUCT DATA (global) ---------------- #
    featured_products = [
    {"id": 1, "name": "Sunblock Sunscreen", "image": "4.png", "price": "₹600", "category": "face"},
    {"id": 2, "name": "Eternal face serum", "image": "1.jpg", "price": "₹450", "category": "face"},
    {"id": 3, "name": "Coffee Walnut", "image": "5.png", "price": "₹350", "category": "face"},
    {"id": 4, "name": "De -Tan Pack", "image": "2.png", "price": "₹500", "category": "face"},
    {"id": 5, "name": "Stretch Mark", "image": "7.png", "price": "₹600", "category": "face"},
    {"id": 6, "name": "Radiance Serum", "image": "9.png", "price": "₹400", "category": "face"},
]


    best_sellers = [
    {"id": 7, "name": "Night Repair Cream", "image": "6.png", "price": "₹1,800", "category": "best_seller"},
    {"id": 8, "name": "Brightening Serum", "image": "9.png", "price": "₹1,400", "category": "best_seller"},
    {"id": 9, "name": "Aloe Face Cream", "image": "4.png", "price": "₹1,250", "category": "best_seller"},
    {"id": 10, "name": "Night Repair Cream", "image": "2.png", "price": "₹1,800", "category": "best_seller"},
    {"id": 11, "name": "Brightening Serum", "image": "11.png", "price": "₹1,400", "category": "best_seller"},
    {"id": 12, "name": "Aloe Face Cream", "image": "4.png", "price": "₹1,250", "category": "best_seller"},
]

    all_products = featured_products + best_sellers

    cart = session.get("cart", {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = next((p for p in all_products if p["id"] == int(pid)), None)
        if product:
            # Remove ₹ and commas to calculate total
            price = int(str(product["price"]).replace("₹","").replace(",",""))
            subtotal = price * qty
            total += subtotal
            items.append({
                "name": product["name"],
                "qty": qty,
                "price": price,
                "subtotal": subtotal
            })

    # Clear cart after order
    session["cart"] = {}

    return render_template('success.html', items=items, total=total)


init_db()

# Cleanup old marquee entries automatically
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute("DELETE FROM marquee WHERE text IS NULL")
    conn.commit()
    print("🧹 Cleaned old empty marquee rows")

@app.route("/test_cart")
def test_cart():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("SELECT * FROM cart")
    data = c.fetchall()
    conn.close()
    return str(data)



# ---------------- RUN ---------------- #
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
    
    
    
    
    



