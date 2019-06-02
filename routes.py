from config import app
from controller_functions import index, cancel_order, add_newuser, view_cart, search, dashboard, login, add_to_cart, submit_order, order_complete

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=add_newuser, methods=["POST"])
app.add_url_rule("/username", view_func=search, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/orders", view_func=dashboard, methods=["GET", "POST"])
app.add_url_rule("/cancel", view_func=cancel_order, methods=["GET", "POST"])
app.add_url_rule("/add_to_cart", view_func=add_to_cart, methods=["GET", "POST"])
app.add_url_rule("/complete", view_func=order_complete, methods=["GET", "POST"])
app.add_url_rule("/view_cart", view_func=view_cart, methods=["GET", "POST"])
app.add_url_rule("/place_order", view_func=submit_order, methods=["POST"])

# app.add_url_rule("/users/<user_id>", view_func=user_profile, methods=["GET", "POST"])
# app.add_url_rule("/bright_ideas/<idea_id>", view_func=idea_details, methods=["GET", "POST"])


