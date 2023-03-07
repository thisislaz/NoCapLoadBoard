from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE,get_broker,remove_white_space as rws
from flask import flash
from flask_app import EMAIL_REGEX, re
from datetime import datetime
from flask_app.models import address_model, user_model

class Broker:
  def __init__(self,data):
    self.broker_id = data['broker_id']
    self.company_name = data['company_name']
    self.company_phone = data['company_phone']
    self.us_dot = data['us_dot']
    self.mc_number = data['mc_number']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']

#creating the bokers
  @classmethod
  def create_broker_user(cls,data):
    query = "INSERT INTO users (email,first_name,last_name,password) VALUES (LOWER(%(email)s),LOWER(%(first_name)s),LOWER(%(last_name)s),%(password)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def create_broker_info(cls,data):
    query = "INSERT INTO brokers (company_name, company_phone, us_dot,mc_number, user_id) VALUES (%(company_name)s, %(company_phone)s,%(us_dot)s,%(mc_number)s, %(user_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)
    
#getters
  @classmethod
  def get_by_id(cls,data):
    query = 'SELECT * FROM brokers WHERE broker_id = %(broker_id)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_by_user_id(cls,data):
    query = 'SELECT * FROM brokers WHERE brokers.user_id = %(user_id)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_by_company_name(cls,data):
    query = 'SELECT * FROM brokers WHERE brokers.company_name = %(company_name)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_company_phone(cls,data):
    query = 'SELECT * FROM brokers WHERE brokers.company_phone = %(company_phone)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_us_dot(cls,data):
    query = 'SELECT * FROM brokers WHERE brokers.us_dot = %(us_dot)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  
  @classmethod
  def get_by_mc_number(cls,data):
    query = 'SELECT * FROM brokers WHERE brokers.mc_number = %(mc_number)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])
  

#------------------- staticmethods --------------- staticmethods ---------------------
  @staticmethod
  def broker_validator(broker_data):
    is_valid = True
    if len(broker_data['company_name']) < 1:
      flash("Company name is required!")
      is_valid = False
    elif len(broker_data['company_name']) > 1:
      cn = Broker.get_by_company_name({'company_name':broker_data['company_name']})
      if cn:
        flash('Company name is already registered, so company might already be a user.')
        is_valid = False
    if len(broker_data['company_phone']) < 10:
      flash("Company phone number is required! US 10 digit.")
      is_valid = False
    if len(broker_data['address_line_one']) < 10:
      flash("Address is required!")
      is_valid = False
    if len(broker_data['city']) < 1:
      flash("City is required!")
      is_valid = False
    if len(broker_data['state']) < 1:
      flash("State is required!")
      is_valid = False
    if len(broker_data['postal_code']) < 5:
      flash("Postal code is required!")
      is_valid = False
    if len(broker_data['us_dot']) < 1:
      flash("Broker DOT number is required!")
      is_valid = False
    elif len(broker_data['us_dot']) == 7:
      data ={'us_dot':broker_data['us_dot']}
      dot = Broker.get_by_us_dot(data)
      if dot:
        flash('Broker already registered!')
        is_valid = False
    if len(broker_data['mc_number']) < 1:
      flash("Broker's MC Number is required!")
      is_valid = False
    elif len(broker_data['mc_number']) == 6:
      mc = Broker.get_by_mc_number({'mc_number':broker_data['mc_number']})
      if mc: 
        flash('MC Number already registered')
        is_valid = False
    api_broker = get_broker(broker_data['us_dot'])      
    if api_broker:
      if api_broker['company_name'] != broker_data['company_name'].upper():
        flash("Names do not match.")
        is_valid = False
      elif api_broker['address_line_one'] != rws(broker_data['address_line_one']).upper():
        flash("Addresses do not match.")
        is_valid = False
      elif api_broker['state'] != broker_data['state'].upper():
        flash("State does not match.")
        is_valid = False
      elif api_broker['city'] != broker_data['city'].upper():
          flash('Cities do not match')
          is_valid = False
      elif api_broker['postal_code'] != broker_data['postal_code']:
          flash('Postal codes do not matach.')
          is_valid = False
      elif api_broker['us_dot'] != int(broker_data['us_dot']):
          flash('US DOT numbers do not matach.')
          is_valid = False
      elif api_broker['mc_number'] != int(broker_data['mc_number']):
        flash('MC numbers do not matach.')
        is_valid = False
      else:
        is_valid = True
    else:
        flash('This is not a real company registered with the US DOT FMCSA. Please try again, as you may have entered inaccurate info. Please feel free to reach out to me if this error persists.')
        is_valid = False
    return is_valid
