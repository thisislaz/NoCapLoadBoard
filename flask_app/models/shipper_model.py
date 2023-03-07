from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app import EMAIL_REGEX, re
from datetime import datetime
from flask_app.models import address_model, user_model

class Shipper:
  def __init__(self,data):
    self.shipper_id = data['shipper_id']
    self.company_name = data['company_name']
    self.company_phone = data['company_phone']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']

#creating the shippers
  @classmethod
  def create_shipper_user(cls,data):
    query = "INSERT INTO users (email,first_name,last_name,password) VALUES (LOWER(%(email)s),LOWER(%(first_name)s),LOWER(%(last_name)s),%(password)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def create_shipper_info(cls,data):
    query = "INSERT INTO shippers (company_name, company_phone, user_id) VALUES (%(company_name)s, %(company_phone)s, %(user_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

#getters
  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM shippers WHERE shipper_id = %(shipper_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_user_id(cls,data):
    query = 'SELECT * FROM shippers WHERE shippers.user_id = %(user_id)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_company_name(cls,data):
    query = 'SELECT * FROM shippers WHERE shippers.company_name = %(company_name)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_company_phone(cls,data):
    query = 'SELECT * FROM shippers WHERE shippers.company_phone = %(company_phone)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
#------------------- staticmethods --------------- staticmethods ---------------------
  @staticmethod
  def shipper_validator(shipper_data):
    is_valid = True
    if len(shipper_data['company_name']) < 1:
      flash("Company name is required!")
      is_valid = False
    elif len(shipper_data['company_name']) > 1:
      cn = Shipper.get_by_company_name({'company_name':shipper_data['company_name']})
      if cn:
        flash('Company name is already registered, so company might already be a user.')
        is_valid = False
    if len(shipper_data['company_phone']) < 10:
      flash("Company phone number is required! US 10 digit.")
      is_valid = False
    if len(shipper_data['address_line_one']) < 1:
      flash("Address is required!")
      is_valid = False
    if len(shipper_data['city']) < 2:
      flash("City is required! ")
      is_valid = False
    if len(shipper_data['state']) < 2:
      flash("State is required! Either abbreviated or spelled out.")
      is_valid = False
    if len(shipper_data['postal_code']) < 5:
      flash("Postal code is required!")
      is_valid = False
    return is_valid