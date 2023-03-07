from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE,get_carrier,remove_white_space as rws
from flask import flash
from flask_app import EMAIL_REGEX, re
from datetime import datetime
from flask_app.models import address_model, user_model

class Carrier:
  def __init__(self,data):
    self.carrier_id = data["carrier_id"]
    self.company_name = data["company_name"]
    self.company_phone = data["company_phone"]
    self.us_dot = data["us_dot"]
    self.mc_number = data["mc_number"]
    self.created_at = data["created_at"]
    self.updated_at = data["updated_at"]
    self.user_id = data["user_id"]

#creating the carrier tables
  @classmethod
  def create_carrier_user(cls,data):
    query = """INSERT INTO users (email,first_name,last_name,password) VALUES (LOWER(%(email)s),LOWER(%(first_name)s),LOWER(%(last_name)s),%(password)s);"""
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def create_carrier_info(cls,data):
    query = "INSERT INTO carriers (company_name, company_phone, us_dot, mc_number, user_id) VALUES (%(company_name)s, %(company_phone)s, %(us_dot)s, %(mc_number)s, %(user_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def create_carrier_address(cls,data):
    query = "INSERT INTO carrier_address (carrier_id) VALUES (%(user_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

# -------     getters    ---------------
  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM carriers WHERE carrier_id = %(carrier_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_user_id(cls,data):
    query = "SELECT * FROM carriers WHERE carriers.user_id = %(user_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_us_dot(cls,data):
    query = "SELECT * FROM carriers WHERE carriers.us_dot = %(us_dot)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    print(results)
    return cls(results[0])
  
  @classmethod
  def get_by_mc_number(cls,data):
    query = "SELECT * FROM carriers WHERE carriers.mc_number = %(mc_number)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    print(results)
    return cls(results[0])
  
  @classmethod
  def get_by_phone_number(cls,data):
    query = "SELECT * FROM carriers WHERE carriers.company_phone = %(company_phone)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    print(results)
    return cls(results[0])
  
  @classmethod
  def get_by_company_name(cls,data):
    query = "SELECT * FROM carriers WHERE carriers.company_name = %(company_name)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    print(results)
    return cls(results[0])

#------------------- staticmethods --------------- staticmethods ---------------------
  @staticmethod
  def carrier_validator(carrier_data):
    is_valid = True
    if len(carrier_data['company_name']) < 1:
      flash("Company name is required!")
      is_valid = False
    elif len(carrier_data['company_name']) > 1:
      cn = Carrier.get_by_company_name({'company_name':carrier_data['company_name']})
      if cn:
        flash('Company name is already registered, so company might already be a user.')
        is_valid = False
    if len(carrier_data['company_phone']) < 10:
      flash("Company phone number is required! US 10 digit.")
      is_valid = False
    if len(carrier_data['address_line_one']) < 10:
      flash("Address is required!")
      is_valid = False
    if len(carrier_data['city']) < 1:
      flash("City is required!")
      is_valid = False
    if len(carrier_data['state']) < 1:
      flash("State is required!")
      is_valid = False
    if len(carrier_data['postal_code']) < 5:
      flash("Postal code is required!")
      is_valid = False
    if len(carrier_data['us_dot']) < 1:
      flash("Carrier DOT number is required!")
      is_valid = False
    elif len(carrier_data['us_dot']) == 7:
      data ={'us_dot':carrier_data['us_dot']}
      dot = Carrier.get_by_us_dot(data)
      if dot:
        flash('Carrier already registered!')
        is_valid = False
    if len(carrier_data['mc_number']) < 1:
      flash("Carrier's MC Number is required!")
      is_valid = False
    elif len(carrier_data['mc_number']) == 6:
      mc = Carrier.get_by_mc_number({'mc_number':carrier_data['mc_number']})
      if mc: 
        flash('MC Number already registered')
        is_valid = False
    api_carrier = get_carrier(carrier_data['us_dot'])      
    if api_carrier:
      if api_carrier['company_name'] != carrier_data['company_name'].upper():
        flash("Names do not match.")
        is_valid = False
      elif api_carrier['address_line_one'] != rws(carrier_data['address_line_one']).upper():
        flash("Addresses do not match.")
        is_valid = False
      elif api_carrier['state'] != carrier_data['state'].upper():
        flash("State does not match.")
        is_valid = False
      elif api_carrier['city'] != carrier_data['city'].upper():
          flash('Cities do not match')
          is_valid = False
      elif api_carrier['postal_code'] != carrier_data['postal_code']:
          flash('Postal codes do not matach.')
          is_valid = False
      elif api_carrier['us_dot'] != int(carrier_data['us_dot']):
          flash('US DOT numbers do not matach.')
          is_valid = False
      elif api_carrier['mc_number'] != int(carrier_data['mc_number']):
        flash('MC numbers do not matach.')
        is_valid = False
      else:
        is_valid = True
    else:
        flash('This is not a real company registered with the US DOT FMCSA. Please try again, as you may have entered inaccurate info. Please feel free to reach out to me if this error persists.')
        is_valid = False
    return is_valid