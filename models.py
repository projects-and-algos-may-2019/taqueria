from sqlalchemy.sql import func, expression
from flask import flash
from config import db, bcrypt
import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=\S{5,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')


class Users(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(145))
    email = db.Column(db.String(125))
    password = db.Column(db.String(125))
    user_orders = db.relationship('Orders', backref='owner')
    user_likes = db.relationship('Likes', backref='user_liked')

    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_user(cls, user_data):
        is_valid = True
        if len(user_data["name"]) < 1:
            is_valid = False
            flash("Please provide name")
        if len(user_data["alias"]) < 1:
            is_valid = False
            flash("Please provide alias")
        if not EMAIL_REGEX.match(user_data["email"]):
            is_valid = False
            flash("Please provide a valid email")
        if len(user_data["password"]) < 8:
            is_valid = False
            flash("Password should be at least 8 characters")
        if user_data["password"] != user_data["cpassword"]:
            is_valid = False
            flash("Passwords do not match")
        return is_valid

    @classmethod
    def validate_login(cls, user_data):
        print(user_data)
        is_valid = True
        result = Users.query.filter_by(email = user_data["username"]).first()

        if not EMAIL_REGEX.match(user_data["username"]):
            is_valid = False
            flash("Please provide a valid email")
        if len(user_data["password"]) < 3:
            is_valid = False
            flash("Password should be at least 8 characters")
        if result:
            if not bcrypt.check_password_hash(result.password, user_data['password']):
                is_valid = False
                flash("Passwords incorrect")
        return is_valid

    @classmethod
    def add_new_user(cls, user_data):
        hashed_password = bcrypt.generate_password_hash(user_data["password"])
        user_to_add = cls(name=user_data["name"], alias=user_data["alias"], email=user_data["email"], password=hashed_password)
        db.session.add(user_to_add)
        db.session.commit()
        return user_to_add


class Ideas(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idea = db.Column(db.String(145))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    liked = db.relationship('Likes', backref= 'idea_liked')
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    

    @classmethod
    def validate_idea(cls, user_data):
        is_valid = True
        if len(user_data["idea"]) < 3:
            is_valid = False
            flash("Please provide your idea, it should be at least 3 words!")
        return is_valid


    @classmethod
    def add_new_idea(cls, user_data):
        print(user_data["user_id"])
        print("***************************")

        user_owner = Users.query.get(user_data["user_id"])
        idea_to_add = cls(idea=user_data["idea"], owner = user_owner)
        db.session.add(idea_to_add)
        db.session.commit()
        return idea_to_add

    @classmethod
    def delete_idea(cls, user_data):
        
        idea_to_delete = Ideas.query.filter_by(id=user_data['which_idea']).first()
        # existing_wish = Wishes.query.get(user_data['removed_id'])

        # user_wished = Users.query.get(user_data["user_id"])
        # existing_wish.wishes_of_user.remove(user_wished)
        # user_wished.user_wishes.remove(existing_wish)

        db.session.delete(idea_to_delete)
        db.session.commit()
        
        return  idea_to_delete
        

    # @classmethod
    # def edit_wish(cls, user_data):
        
    #     wish_to_edit = Wishes.query.filter_by(id=user_data['edit_id'])
    #     wish_to_edit.item=user_data["item"]
    #     wish_to_edit.description=user_data["description"]
        
    #     db.session.commit()
        
    #     return  wish_to_edit
        




class Likes(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('ideas.id'))

    created_at = db.Column(db.DateTime, server_default=func.now())   
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    

    @classmethod
    def add_likes(cls, user_data):
       
        idea_ids =[]
        print(user_data)
        user_liked = Users.query.get(user_data["user_id"])
        idea_liked = Ideas.query.get(user_data["idea_id"])
        print(idea_liked)
        existing_likes=user_liked.user_likes
        for like in existing_likes:
            i = like.idea_id
            idea_ids.append(i)

        new_like=idea_liked.liked
        
        print("==================++++++++++++======================")
        print(user_data["idea_id"])
        print(idea_ids)
        print("==================++++++++++++======================")
       
        print(existing_likes)
        print("==================++++++++++++======================")
        print(new_like)

        if(int(user_data["idea_id"]) not in idea_ids):
            print(user_liked.user_likes)
            print("??????????????<>><><><><><><<>??????????????????")
            like_to_add = cls(user_liked = user_liked, idea_liked =idea_liked)
            db.session.add(like_to_add)
            db.session.commit()
            return like_to_add
        else: 
            flash("You have already liked this Idea!")
            print("Skipped if Skipped if Skipped if Skipped if Skipped if Skipped if Skipped if Skipped if ")
            return new_like


      