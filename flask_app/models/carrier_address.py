from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class CarrierAddress:
  def __init__(self,data):
    self.address_id = data['address_id']
    self.carrier_id = data['carrier_id']

  @classmethod
  def create_carrier_address(cls,data):
    query = "INSERT INTO carrier_address(address_id,carrier_id) VALUES (%(address_id)s,%(carrier_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

#getters
  @classmethod
  def get_address_by_id(cls,data):
    query = "SELECT * FROM address LEFT JOIN carrier_address ON address.address_id = carrier_address.address_id LEFT JOIN carriers ON carriers.carrier_id = carrier_address.carrier_id WHERE carriers.carrier_id =  %(carrier_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    address = cls(results[0])
    return address
