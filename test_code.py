from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a proper secret key for session management


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

    def show_info(self):
        print(f"{self.name} - ${self.price:.2f}")
        print(f"   > {self.description}")
        if self.reviews:
            avg = sum(r['rating'] for r in self.reviews) / len(self.reviews)
            print(f"   ⭐ {avg:.1f}/5 from {len(self.reviews)} review(s)")
        else:
            print("   ⭐ No reviews yet.")

    def add_review(self, user, rating, comment):
        self.reviews.append({'user': user, 'rating': rating, 'comment': comment})


# Initialize users as a dictionary, not a list
users = {}
products = [
    Product("Peace Lily", 12.99, "Indoor", "Calming with white blooms. Loves shade."),
    Product("Snake Plant", 15.49, "Indoor", "Tough, low-maintenance, and cleans air."),
    Product("Fern", 10.00, "Indoor", "Lush and leafy. Likes humidity."),
    Product("Rose", 8.99, "Outdoor", "Classic blooms with a sweet scent."),
    Product("Lavender", 9.50, "Outdoor", "Smells great, attracts bees."),
    Product("Hibiscus", 11.25, "Outdoor", "Tropical blooms, needs lots of sun.")
]

cart = []
total = 0.0
user = None  # Keep track of the current logged-in user


# Function to show the cart
def show_cart():
    global total
    if not user:  # Check if the user is logged in
        return redirect(url_for('login'))  # Redirect to login if not logged in

    print("\n🛒 Your Cart:")
    if not cart:
        print("Cart is empty.")
    else:
        for p in cart:
            print(f"- {p.name} - ${p.price:.2f}")
        print(f"Total: ${total:.2f}")


# Function to show all reviews
def show_reviews():
    global user
    if not user:  # Check if the user is logged in
        return redirect(url_for('login'))  # Redirect to login if not logged in

    print("\n📝 Reviews:")
    for p in products:
        print(f"\n🌱 {p.name}")
        if p.reviews:
            for r in p.reviews:
                print(f"  {r['user']} rated {r['rating']}/5: \"{r['comment']}\"")
        else:
            print("  No reviews written yet.....")


# Function for the shopping experience
def shop():
    global total
    if not user:  # Check if the user is logged in
        return redirect(url_for('login'))  # Redirect to login if not logged in

    while True:
        print("\n1. Indoor Plants\n2. Outdoor Plants")
        choice = input("Choose a category (1 or 2): ").strip()
        if choice == "1":
            category = "Indoor"
            break
        elif choice == "2":
            category = "Outdoor"
            break
        else:
            print("Invalid choice. Please select 1 for Indoor or 2 for Outdoor.")

    print(f"\n--- {category} Plants ---")
    for p in products:
        if p.category == category:
            p.show_info()

    while True:
        pick = input("\nEnter the name of the plant to add to cart: ").strip()
        for p in products:
            if p.name.lower() == pick.lower() and p.category == category:
                if p in cart:
                    print("Already in cart.")
                else:
                    cart.append(p)
                    total += p.price
                    print(f"{p.name} added to cart.")
                break
        else:
            print("Couldn't find that plant.")
            checkout_option = input(
                "\nWould you like to:\n1. Checkout\n2. Add more plants\nChoose an option (1 or 2): ").strip()
            while checkout_option not in ["1", "2"]:
                print("Invalid option. Please choose 1 to checkout or 2 to add more plants.")
                checkout_option = input(
                    "\nWould you like to:\n1. Checkout\n2. Add more plants\nChoose an option (1 or 2): ").strip()
            if checkout_option == "1":
                print(f"\nThanks for shopping! Total: ${total:.2f}")
                if input("Leave a review? (yes/no): ").lower() == "yes":
                    for p in cart:
                        print(f"\nReview for {p.name}:")
                        while True:
                            try:
                                rating = int(input("Rating (1-5): "))
                                if 1 <= rating <= 5:
                                    break
                                else:
                                    print("Rating must be between 1 and 5.")
                            except:
                                print("Please enter a valid number for rating.")
                        comment = input("Comment: ")
                        p.add_review(user.username, rating, comment)
                        print("Review added!")
                cart.clear()
                total = 0.0
                break
            elif checkout_option == "2":
                continue


# Function to view profile
def profile():
    if not user:  # Check if the user is logged in
        return redirect(url_for('login'))  # Redirect to login if not logged in

    print("\n👤 Profile")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Joined: {user.created}")


# Login or account creation function
def login_or_create(choice):
    global user
    if choice == "1":
        print("\n--- Login ---")
        uname = input("Username: ")
        pwd = input("Password: ")
        if uname in users and users[uname].password == pwd:  # Check if the user exists and password matches
            user = users[uname]
            print(f"Logged in as {uname}.\n")
        else:
            print("Invalid username or password. Please try again.")
            return False
    else:
        print("\n--- Create Account ---")
        uname = input("Username: ")
        email = input("Email: ")
        pwd = input("Password: ")
        user = User(len(users) + 1, uname, email, pwd)
        users[uname] = user  # Add the new user to the dictionary
        print(f"Account created. Welcome, {uname}!\n")
    return True


# Function to welcome the user and choose login or account creation
def welcome():
    print("🌿 Welcome to the Online Plant Nursery!")
    while True:
        print("1. Login\n2. Create Account")
        choice = input("Choose an option (1 or 2): ").strip()
        if choice == "1" or choice == "2":
            if login_or_create(choice):
                break
        else:
            print("Invalid input. Please choose 1 to Login or 2 to Create Account.")


# Main function to run the app
if __name__ == "__main__":
    welcome()

    while True:
        print("\nWhat would you like to do?")
        print("1. Shop\n2. View Cart\n3. Profile\n4. Reviews\n5. Exit")
        action = input("Choose (1–5): ").strip()
        while action not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Please choose between 1 and 5.")
            action = input("Choose (1–5): ").strip()

        if action == "1":
            shop()
        elif action == "2":
            show_cart()
        elif action == "3":
            profile()
        elif action == "4":
            show_reviews()
        elif action == "5":
            print("🌱 Thanks for stopping by! See you next time.")
            break
