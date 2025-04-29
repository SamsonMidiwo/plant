from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# User class
class User:
    def __init__(self, uid, username, email, password):
        self.uid = uid
        self.username = username
        self.email = email
        self.password = password
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Product class
class Product:
    def __init__(self, name, price, category, description):
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.reviews = []

    def add_review(self, user, rating, comment):
        self.reviews.append({'user': user, 'rating': rating, 'comment': comment})

# Global state (basic demo, not production safe)
users = {}
products = [
    Product("Peace Lily", 12.99, "Indoor", "Calming with white blooms. Loves shade."),
    Product("Snake Plant", 15.49, "Indoor", "Tough, low-maintenance, and cleans air."),
    Product("Fern", 10.00, "Indoor", "Lush and leafy. Likes humidity."),
    Product("Rose", 8.99, "Outdoor", "Classic blooms with a sweet scent."),
    Product("Lavender", 9.50, "Outdoor", "Smells great, attracts bees."),
    Product("Hibiscus", 11.25, "Outdoor", "Tropical blooms, needs lots of sun.")
]

user = None
cart = []
total = 0.0

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global user
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(len(users) + 1, username, email, password)
        users[username] = user
        return redirect(url_for('shop'))
    return render_template('signup.html')

# Login route (no check)
@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(len(users) + 1, username, '', password)
        users[username] = user
        return redirect(url_for('shop'))
    return render_template('login.html')

# Shop page
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    global user, cart, total
    if not user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        product_name = request.form['product_name']
        selected_product = next((p for p in products if p.name == product_name), None)
        if selected_product:
            cart.append(selected_product)
            total += selected_product.price
    return render_template('shop.html', username=user.username, products=products, cart=cart, total=total)

# Checkout
@app.route('/checkout')
def checkout():
    if not user:
        return redirect(url_for('login'))
    return render_template('checkout.html', cart=cart, total=total)

# Profile
@app.route('/profile')
def profile():
    if not user:
        return redirect(url_for('login'))
    return render_template('profile.html', username=user.username, email=user.email, created=user.created)

# Logout
@app.route('/logout')
def logout():
    global user, cart, total
    user = None
    cart = []
    total = 0.0
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
