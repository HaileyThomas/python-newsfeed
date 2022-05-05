# creating a User class that inherits from the Base class from db package
from app.db import Base
# classes from sqlalchemy to define table columns and their data types
from sqlalchemy import Column, Integer, String
# for validation
from sqlalchemy.orm import validates
# to encrypt passwords
import bcrypt

salt = bcrypt.gensalt()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    @validates("email")
    def validate_email(self, key, email):
        # make sure the email address contains an @ character
        # assert keyword automatically throws an error if condition is false
        assert "@" in email

        return email

    @validates("password")
    def validate_password(self, key, password):
        # checks to see that password is more than 4 characters
        assert len(password) > 4

        # encrypt password
        return bcrypt.hashpw(password.encode("utf-8"), salt)
