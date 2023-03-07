from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class BrokerLoad:
  def __init__(self,data):
    self.load_id = data['load_id']
    self.broker_id = data['broker_id']
    
  @classmethod
  def create_broker_load(cls,data):
    query = 'INSERT INTO broker_load (load_id,broker_id) VALUES (%(load_id)s, %(broker_id)s);'
    return connectToMySQL(DATABASE).query_db(query,data)