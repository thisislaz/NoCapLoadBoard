from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class ShipperAddress:
  def __init__(self,data):
    self.address_id = data['address_id']
    self.shipper_id = data['shipper_id']

  @classmethod
  def create_shipper_address(cls,data):
    query = "INSERT INTO shipper_address(address_id, shipper_id) VALUES (%(address_id)s,%(shipper_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def get_address_by_id(cls,data):
    query = 'SELECT * FROM address LEFT JOIN shipper_address ON address.address_id = shipper_address.address_id LEFT JOIN shippers ON shippers.shipper_id = shipper_address.shipper_id WHERE shippers.shipper_id = %(shipper_id)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    address = cls(results[0])
    return address