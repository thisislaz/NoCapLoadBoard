from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class BrokerAddress:
  def __init__(self,data):
    self.address_id = data['address_id']
    self.broker_id = data['broker_id']

  @classmethod
  def create_broker_address(cls,data):
    query = "INSERT INTO broker_address (address_id,broker_id) VALUES (%(address_id)s, %(broker_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def get_address_by_broker_id(cls,data):
    query = 'SELECT * FROM address LEFT JOIN broker_address ON address.address_id = broker_address.address_id LEFT JOIN brokers ON brokers.broker_id = broker_address.broker_id WHERE brokers.broker_id = %(broker_id)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    address = cls(results[0])
    return address