from config import app
from controller_functions import index, add_newuser, search, dashboard, add_idea, login, like, user_profile, idea_details, delete


app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=add_newuser, methods=["POST"])
app.add_url_rule("/username", view_func=search, methods=["POST"])
app.add_url_rule("/delete", view_func=delete, methods=["POST"])
app.add_url_rule("/post_idea", view_func=add_idea, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/like", view_func=like, methods=["POST"])
app.add_url_rule("/bright_ideas", view_func=dashboard, methods=["GET", "POST"])
app.add_url_rule("/users/<user_id>", view_func=user_profile, methods=["GET", "POST"])
app.add_url_rule("/bright_ideas/<idea_id>", view_func=idea_details, methods=["GET", "POST"])


