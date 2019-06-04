from flask import Flask, render_template, redirect, request, session, flash
from config import app, db
from models import Users, Product, Purchases, Product_purchases, Category

def index():
    
    
    return render_template("index.html" )

def dashboard():
  
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
        print(session["name"])
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
            session["name"] = result.name
            # return render_template("users.html", users = list_of_all_users, name = session["first_name"], user_id = session["user_id"])
            return redirect("/orders")
   

def logout():
    session.clear()

    return redirect("/")

def cancel_order():
    flash("Your Order Is Cancelled!")

    return redirect("/orders")


def add_to_cart():
    print(request.form)
    items = Product.query.all()
    # items = request.form
    cart_content = []
    total = 0
    total_qty =0
    for item in items:
        dbprice = item.price
        dbitem_id = item.id
        dbitem_name = item.name
        quantity = request.form[str(dbitem_id)]
        if(quantity !='' and quantity != '0'):
            in_cart = {}
            item_cat = int(request.form['item_cat'])
            print(request.form[str(dbprice)])
            print(type(request.form[str(dbprice)]))
            amount = float(request.form[str(dbprice)])*int(quantity)
            category = Category.query.filter_by(id = item_cat).first()
            item_name = request.form[dbitem_name]
            in_cart['amount'] = amount
            in_cart['category'] = category.name
            in_cart['item_name'] = item_name
            in_cart['quantity'] = int(quantity)
            cart_content.append(in_cart)
            total +=amount
            total_qty += int(quantity)
        print(cart_content)
    user = session["name"]
    user_id = session["user_id"]


    return render_template('confirmation.html', cart_content=cart_content, user = user, total = total, user_id = user_id, total_qty = total_qty) 

def order_complete():
    user = session["name"]
    user_id = session["user_id"]

    return render_template('complete.html', user = user, user_id = user_id)


def submit_order():
    print(request.form)

    new_order = Purchases.add_new_purchase(request.form)

    return redirect("/complete")


def view_cart():
    print(request.form)
    items_arr = []
    f = request.form
    items = Product.query.all()
    for item in items:
        items_dict = {}
        items_dict['name'] = item.name
        items_dict['id'] = item.id
        items_dict['cat_id'] = item.cat_id
        items_dict['price'] = item.price
        for key in f.keys():
            print("Here are all KEEEEYYYYYYYYYSSSS: "+key)
            print("Here are all IETM NAAAAAAAYMEEEES: "+ item.name)
            if (item.name == key):
                items_dict['quantity'] = request.form[item.name]
                break
            else: 
                items_dict['quantity'] = 0

        items_arr.append(items_dict)
    return render_template("edit_order.html", name = session["name"], user_id = session["user_id"], items=items_arr)

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