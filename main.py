# main.py - Pastilicious interactive features (PyScript + Python)
# Each function below is an EVENT HANDLER: it runs when the user does something.

from html import escape
from pyscript import document, when

# Product names and their prices
PRICES = {
    "Regular Chicken Pastil": 35,
    "Spicy Chicken Pastil": 40,
    "Chicken Pastil with Egg": 45,
    "Extra Chicken Pastil": 50,
}


# ---------- Helper functions ----------

def get(element_id):
    """Find an element on the page by its id."""
    return document.getElementById(element_id)


def read_quantity(text):
    """Convert the typed quantity to a whole number. Return 0 if it is invalid."""
    try:
        quantity = int(text)
    except ValueError:
        return 0
    if quantity <= 0:
        return 0
    return quantity


def show_error(text):
    """Show a friendly error message in the order form."""
    get("order-error").innerText = text


def build_summary(product, quantity):
    """Calculate the total and return the order summary as HTML."""
    price = PRICES[product]

    # Calculate the total price
    total = price * quantity

    return f"""
        <div class="summary-box">
            <p><strong>{product}</strong></p>
            <p>{quantity} × ₱{price}</p>
            <p class="total">Total: ₱{total}</p>
        </div>
    """


def check_product_and_quantity():
    """Validate product and quantity. Return (product, quantity) or None."""
    product = get("product-select").value
    quantity = read_quantity(get("quantity").value)

    if product == "":
        show_error("Please select a product.")
        return None
    if quantity == 0:
        show_error("Please enter a valid quantity.")
        return None
    return product, quantity


# ---------- Event 1 & 2: Hero buttons scroll to sections ----------

@when("click", "#view-menu-btn")
def go_to_menu(event):
    get("menu").scrollIntoView({"behavior": "smooth"})


@when("click", "#order-now-btn")
def go_to_order(event):
    get("order").scrollIntoView({"behavior": "smooth"})


# ---------- Event 3: Add to Order ----------

@when("click", ".add-btn")
def add_to_order(event):
    # Find out which product's button was clicked
    product = event.currentTarget.getAttribute("data-product")

    # Select that product in the order form
    get("product-select").value = product

    # Start with a quantity of 1 if nothing was typed yet
    if read_quantity(get("quantity").value) == 0:
        get("quantity").value = "1"

    # Show the order summary right away and go to the order form
    show_error("")
    get("order-confirmation").innerHTML = ""
    quantity = read_quantity(get("quantity").value)
    get("order-summary").innerHTML = build_summary(product, quantity)
    get("order").scrollIntoView({"behavior": "smooth"})


# ---------- Event 4: Calculate Total ----------

@when("click", "#calculate-btn")
def calculate_total(event):
    show_error("")
    result = check_product_and_quantity()
    if result is None:
        return
    product, quantity = result
    get("order-confirmation").innerHTML = ""
    get("order-summary").innerHTML = build_summary(product, quantity)


# ---------- Event 5: Place Order ----------

@when("click", "#place-order-btn")
def place_order(event):
    show_error("")

    # Check the customer name
    name = get("customer-name").value.strip()
    if name == "":
        show_error("Please enter your name.")
        return

    # Check the product and quantity
    result = check_product_and_quantity()
    if result is None:
        return
    product, quantity = result

    # Calculate the total price
    total = PRICES[product] * quantity
    request = get("special-request").value.strip()

    # Show the order summary and the confirmation message
    get("order-summary").innerHTML = build_summary(product, quantity)

    confirmation = f"""
        <div class="confirm-box">
            <p><strong>Thank you, {escape(name)}! Your order has been successfully placed.</strong></p>
            <p>Product: {product}</p>
            <p>Quantity: {quantity}</p>
            <p>Total: ₱{total}</p>
    """
    if request != "":
        confirmation += f"<p>Special Request: {escape(request)}</p>"
    confirmation += "</div>"
    get("order-confirmation").innerHTML = confirmation


# ---------- Event 6: Clear Order ----------

@when("click", "#clear-order-btn")
def clear_order(event):
    get("customer-name").value = ""
    get("product-select").value = ""
    get("quantity").value = ""
    get("special-request").value = ""
    get("order-summary").innerHTML = '<p class="muted">Your order summary will appear here.</p>'
    get("order-confirmation").innerHTML = ""
    show_error("")


# ---------- Quick Price Calculator ----------

@when("click", "#calc-btn")
def calculate_quick_price(event):
    product = get("calc-product").value
    quantity = read_quantity(get("calc-quantity").value)
    result_box = get("calc-result")

    if product == "":
        result_box.innerHTML = '<p class="message error">Please select a product.</p>'
        return
    if quantity == 0:
        result_box.innerHTML = '<p class="message error">Please enter a valid quantity.</p>'
        return

    # Calculate the total price
    price = PRICES[product]
    total = price * quantity

    result_box.innerHTML = f"""
        <div class="summary-box">
            <p>{product}: ₱{price}</p>
            <p>Quantity: {quantity}</p>
            <p class="total">Total: ₱{total}</p>
        </div>
    """


# ---------- Event 8: Reset Calculator ----------

@when("click", "#calc-reset-btn")
def reset_calculator(event):
    get("calc-product").value = ""
    get("calc-quantity").value = ""
    get("calc-result").innerHTML = ""


# ---------- Event 7: Feedback form submission ----------

@when("submit", "#feedback-form")
def submit_feedback(event):
    # Stop the browser from reloading the page
    event.preventDefault()

    name = get("fb-name").value.strip()
    rating = get("fb-rating").value
    comment = get("fb-comment").value.strip()
    message = get("feedback-message")

    # Check that all fields are filled in
    if name == "" or rating == "" or comment == "":
        message.className = "message error"
        message.innerText = "Please fill in your name, rating, and comment."
        return

    # Build the review card (stars are repeated based on the rating)
    stars = "★" * int(rating)
    card = document.createElement("div")
    card.className = "review"
    card.innerHTML = f"""
        <div class="stars">{stars}</div>
        <p>"{escape(comment)}"</p>
        <p class="muted">— {escape(name)}</p>
    """

    # Add the new card at the top of the reviews list
    reviews = get("reviews")
    placeholder = get("no-reviews")
    if placeholder is not None:
        placeholder.remove()
    reviews.insertBefore(card, reviews.firstChild)

    # Show thank-you message and clear the form
    message.className = "message success"
    message.innerText = "Thank you for your feedback!"
    get("fb-name").value = ""
    get("fb-rating").value = ""
    get("fb-comment").value = ""
