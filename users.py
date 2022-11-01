from mysqlconnection import connectToMySQL 
from flask import flash
import re
# IMPORTING FROM mysqlconnection file, IMPORTING class name 'connectToMySQL'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) <= 0:
            flash("First name cannot be left blank!")
            is_valid = False
        if len(user['last_name']) <= 0:
            flash("Last name cannot be left blank!")
            is_valid = False
        if len(user['email']) <= 0:
            flash("Valid email is required!")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is in the wrong format!")
            is_valid = False
        return is_valid


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []
        for user in results: #type: ignore
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );" # type: ignore
        return connectToMySQL('users_schema').query_db( query, data ) 

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL('users_schema').query_db(query, data)
        return cls(result[0]) #type:ignore

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query,data)