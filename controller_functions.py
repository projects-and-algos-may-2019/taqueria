from flask import Flask, render_template, redirect, request, session, flash
from config import app, db
from models import Users, Product, Purchases, Product_purchases

def index():
    
    
    return render_template("index.html" )

def dashboard():
    # ideas = Ideas.query.all()
    items = Product.query.all()
    print("*****************()()()()******************")
    
    return render_template("orders.html", name = session["name"], user_id = session["user_id"], items=items)

def add_newuser():
    validation_check = Users.validate_user(request.form)
    if not validation_check:        
       return redirect("/")
    else:
        
        new_user = Users.add_new_user(request.form)
        session["user_id"] = new_user.id
        session["name"] = new_user.name
        print(session["user_id"])
        print(session["alias"])
        return redirect("/orders")

def search():
    found = False
    result = Users.query.filter(Users.email.like("{}%".format(request.form["email"]))).all()
    print(result)

    if result:
        found = True
    return render_template('partials/username.html', found=found)  

def login():
    rule = request.url_rule
    if "login" in rule.rule:
        validation_check = Users.validate_login(request.form)
        if not validation_check:        
            return redirect("/")
        else:
            list_of_all_users = Users.query.all()
            result = Users.query.filter_by(email = request.form["username"]).first()
            session["user_id"] = result.id
            print(result.id)
            session["name"] = result.name
            session["alias"] = result.alias
            # return render_template("users.html", users = list_of_all_users, name = session["first_name"], user_id = session["user_id"])
            return redirect("/orders")
   

def logout():
    session.clear()

    return redirect("/")

# def like():


#     print(request.form)
#     print(request.form['user_id'])
#     print("<><><<><><><><><><><><><><><><><><<")

#     new_like = Likes.add_likes(request.form)

#     return redirect("/bright_ideas")




# def add_idea():

#     print(request.form)
#     print(request.form['user_id'])
#     print("<><><<><><><><><><><><><><><><><><<")

#     validation_check = Ideas.validate_idea(request.form)
#     if not validation_check:        
#         return redirect("/bright_ideas")
#     else:
        
#         new_idea = Ideas.add_new_idea(request.form)
#         session["idea_id"] = new_idea.id
        
#         return redirect("/bright_ideas")

# # def add_granted():
    
# #     new_granted = Granted.add_granted(request.form)
   
    
# #     return redirect("/wishes")

# # def remove_wish():
    
# #     removed = Wishes.delete_wish(request.form)
   
    
# #     return redirect("/wishes")

# def user_profile(user_id):
#     print("<><><<><><><><><DDDDDDDDDDDDDDDDD><><><><><><><><><<")
#     user_id = request.form["v_user_id"]
#     print(user_id)
#     the_user = Users.query.filter_by(id = user_id).first()
#     posts = the_user.user_ideas
#     likes = the_user.user_likes

    
#     return render_template("view_user.html", user = the_user, posts = len(posts), likes = len(likes) )

# def idea_details(idea_id):
#     print("<><><<><><><><><DDDDDDDDDDDDDDDDD><><><><><><><><><<")
#     idea_id = request.form["v_idea_id"]
#     print(idea_id)
#     the_idea = Ideas.query.filter_by(id = idea_id).first()
    
#     # posts = the_user.user_ideas
#     likes = the_idea.liked
#     print(likes)

    
#     return render_template("view_idea.html", idea=the_idea, likes=likes)

# def delete():
#     print(request.form)
#     idea_id = request.form["which_idea"]

#     the_gone_idea = Ideas.delete_idea(request.form)

#     print("it is GOOOooooooooonnnneeeeeeeeeeeee")
    
#     return redirect("/bright_ideas")