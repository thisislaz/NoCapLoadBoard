from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Address:
  def __init__(self,data):
    self.address_id = data["address_id"]
    self.address_line_one = data["address_line_one"]
    self.address_line_two = data["address_line_two"]
    self.city = data["city"]
    self.state = data["state"]
    self.postal_code = data["postal_code"]
    self.created_at = data["created_at"]
    self.updated_at = data["updated_at"]


  @classmethod
  def create_address(cls,data):
    query = "INSERT INTO address(address_line_one, address_line_two,city,state,postal_code) VALUES (LOWER(%(address_line_one)s),LOWER(%(address_line_two)s), LOWER(%(city)s),LOWER(%(state)s),%(postal_code)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

  