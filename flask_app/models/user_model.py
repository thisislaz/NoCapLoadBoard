from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app import EMAIL_REGEX, re

class User:
  def __init__(self,data):
    self.user_id = data["user_id"]
    self.email = data["email"]
    self.first_name = data["first_name"]
    self.last_name = data["last_name"]
    self.password = data["password"]
    self.created_at = data["created_at"]
    self.updated_at = data["updated_at"]

  @classmethod
  def get_by_email(cls,data):
    query = "SELECT * FROM users WHERE email = %(email)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM users WHERE user_id = %(user_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_all_users(cls):
    query = """SELECT * FROM users; """
    results = connectToMySQL(DATABASE).query_db(query)
    if len(results) > 0:
      all_users = []
      for row in results:
        this_user = cls(row)
        all_users.append(this_user)
      return all_users
    return []

  @classmethod
  def delete_user(cls,data):
    query = "DELETE FROM users WHERE users.user_id = %(user_id)s;"
    return connectToMySQL(DATABASE).query_db(query,data)

# ----------------  @staticmethods -----------------------------------------------  @staticmethods ---------------------
  @staticmethod
  def user_validator(user_data):
    is_valid = True
    if len(user_data['email']) < 1:
      flash("Email is required!")
      is_valid = False
    elif not EMAIL_REGEX.match(user_data['email']):
      flash("Invalid email format!")
    else:
      data = {
        'email':user_data['email']
      }
      potential_user = User.get_by_email(data)
      if potential_user:
        flash("Email already registered!")
        is_valid = False
    if len(user_data['first_name']) < 1:
      flash("First Name is required!")
      is_valid = False
    if len(user_data['last_name']) < 1:
      flash("Last Name is required!")
      is_valid = False
    if len(user_data['password']) < 1:
      flash("Password is required!")
      is_valid = False
    if len(user_data['password']) < 8:
      flash('Password must be at least 8 characters long!')
      is_valid = False
    if not re.search("[a-z]", user_data['password']):
      flash('Password must have at least one lowercase letter!')
      is_valid = False
    if not re.search('[A-Z]', user_data['password']):
      flash('Password must have at least one capitalized letter!')
      is_valid = False
    if not re.search('[0-9]', user_data['password']):
      flash('Password must contain at least one number!')
      is_valid = False
    if not re.search("(?=.*?[#?!@$%^&*-])", user_data['password']):
      flash('Password must contain one of these characters: #?!@$%^&*-')
      is_valid = False
    if not user_data['password'] == user_data['confirm_pass']:
      flash('Passwords do not match!')
      is_valid = False
    return is_valid