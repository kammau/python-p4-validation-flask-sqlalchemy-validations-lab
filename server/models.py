from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    @validates("name")
    def validate_name(self, key, name):
        names = db.session.query(Author.name).all()

        if not name:
            raise ValueError("Please enter a name.")
        elif name in names:
            raise ValueError("Please enter a unique name.")
        return name

    @validates("phone_number")
    def validate_phone_number(self, key, numbers):
        if len(numbers) != 10:
            raise ValueError("Phone number must be 10 digits long.")
        return numbers

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

    @validates("title")
    def validate_post(self, key, title):
        clickbait_titles = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError("Please enter a title")
        elif (clickbait not in title for clickbait in clickbait_titles):
            raise ValueError("Please enter Clickbaity title.")
        return title

    @validates("content", "summary")
    def validate_content(self, key, post_content):
        if key == "content":
            if len(post_content) <= 250:
                raise ValueError("Post content must be at least 250 characters long.")
        if key == "summary":
            if len(post_content) >= 250:
                raise ValueError("Post summary must be at most 250 characters long.")
        return post_content
    
    @validates("category")
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Category must be either Fick or Non-Fiction.")
        return category
