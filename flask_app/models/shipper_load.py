from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class ShipperLoad:
  def __init__(self,data):
    self.load_id = data['load_id']
    self.shipper_id = data['shipper_id']

  @classmethod
  def create_shipper_load(cls,data):
    query = "INSERT INTO shipper_load (load_id,shipper_id) VALUES (%(load_id)s,%(shipper_id)s);"
    return connectToMySQL(DATABASE).query_db(query,data)
