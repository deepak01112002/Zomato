from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define dishes list
dishes = [
    {"dish_id": 1, "name": "Spaghetti Carbonara", "price": 12.99, "availability": True},
    {"dish_id": 2, "name": "Margherita Pizza", "price": 9.99, "availability": True},
    {"dish_id": 3, "name": "Chicken Tikka Masala", "price": 14.99, "availability": False}
]

# Define orders list
orders_list = [
    {"order_id": 1, "customer_name": "John Doe", "dish_ids": [1, 2], "status": "received"},
    {"order_id": 2, "customer_name": "Jane Smith", "dish_ids": [3], "status": "preparing"}
]


@app.route("/")
def menu():
    return render_template("menu.html", dishes=dishes)

@app.route("/menu/add", methods=["GET", "POST"])
def add_dish():
    if request.method == "POST":
        # Retrieve form data and add a new dish to the list
        dish_id = len(dishes) + 1
        name = request.form.get("name")
        price = float(request.form.get("price"))
        availability = request.form.get("availability") == "on"

        dishes.append({"dish_id": dish_id, "name": name, "price": price, "availability": availability})
        return redirect(url_for("menu"))
    return render_template("add_dish.html")

@app.route("/menu/remove/<int:dish_id>")
def remove_dish(dish_id):
    # Remove the dish with the given dish_id from the list
    for dish in dishes:
        if dish["dish_id"] == dish_id:
            dishes.remove(dish)
            break
    return redirect(url_for("menu"))

@app.route("/menu/update/<int:dish_id>", methods=["GET", "POST"])
def update_dish(dish_id):
    # Find the dish with the given dish_id and update its attributes
    dish = next((d for d in dishes if d["dish_id"] == dish_id), None)
    if dish:
        if request.method == "POST":
            dish["name"] = request.form.get("name")
            dish["price"] = float(request.form.get("price"))
            dish["availability"] = request.form.get("availability") == "on"
            return redirect(url_for("menu"))
        return render_template("update_dish.html", dish=dish)
    return redirect(url_for("menu"))

@app.route("/orders")
def view_orders():
    return render_template("orders.html", orders=orders_list)

@app.route("/order/new", methods=["GET", "POST"])
def new_order():
    if request.method == "POST":
        # Retrieve form data and process the new order
        customer_name = request.form.get("customer_name")
        dish_ids = request.form.get("dish_ids").split(",")

        order_id = len(orders_list) + 1
        order_status = "received"

        # Check if each dish is available
        for dish_id in dish_ids:
            dish = next((d for d in dishes if d["dish_id"] == int(dish_id)), None)
            if not dish or not dish["availability"]:
                return render_template("order_error.html", dish_id=dish_id)

        # Process the order
        new_order = {"order_id": order_id, "customer_name": customer_name, "dish_ids": dish_ids, "status": order_status}
        orders_list.append(new_order)
        return redirect(url_for("view_orders"))
    return render_template("new_order.html", dishes=dishes)

@app.route("/order/update/<int:order_id>", methods=["GET", "POST"])
def update_order(order_id):
    # Find the order with the given order_id and update its status
    order = next((o for o in orders_list if o["order_id"] == order_id), None)
    if order:
        if request.method == "POST":
            order["status"] = request.form.get("status")
            return redirect(url_for("view_orders"))
        return render_template("update_order.html", order=order)
    return redirect(url_for("view_orders"))

@app.route("/order/review")
def review_orders():
    return render_template("review_orders.html", orders=orders_list)

if __name__ == "__main__":
    app.run(debug=True)
