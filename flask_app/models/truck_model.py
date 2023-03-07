from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask import session
from flask_app.models import carrier_model,user_model,truck_model

class Truck:
  def __init__(self,data):
    self.truck_id = data['truck_id']
    self.truck_number = data['truck_number']
    self.origin_city = data['origin_city']
    self.origin_state = data['origin_state']
    self.origin_radius = data['origin_radius']
    self.destination_city = data['destination_city']
    self.destination_state = data['destination_state']
    self.destination_radius = data['destination_radius']
    self.equipment_type = data['equipment_type']
    self.weight = data['weight']
    self.length = data['length']
    self.rate_per_mile = data['rate_per_mile']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.carrier_id = data['carrier_id']

#creating the truck table
  @classmethod
  def create_truck(cls,data):
    query = "INSERT INTO trucks (truck_number,origin_city,origin_state,origin_radius,destination_city,destination_state,destination_radius,equipment_type,weight,length,rate_per_mile,carrier_id) VALUES (%(truck_number)s,LOWER(%(origin_city)s),LOWER(%(origin_state)s),%(origin_radius)s,LOWER(%(destination_city)s),LOWER(%(destination_state)s),%(destination_radius)s,LOWER(%(equipment_type)s),%(weight)s,%(length)s,%(rate_per_mile)s,%(carrier_id)s );"
    return connectToMySQL(DATABASE).query_db(query,data)

#getters
  @classmethod
  def get_by_id(cls,data):
    query = "SELECT * FROM trucks WHERE truck_id = %(truck_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return cls(results[0])

  @classmethod
  def get_by_carrier_id(cls,data):
    query = 'SELECT * FROM trucks LEFT JOIN carriers ON trucks.carrier_id = carriers.carrier_id WHERE trucks.truck_id = %(carrier_id)s;'
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    print(results)
    return cls(results[0])

  @classmethod
  def get_truck_by_id(cls,data):
    query = "SELECT * FROM trucks JOIN carriers on carriers.carrier_id = trucks.carrier_id JOIN users on carriers.user_id = users.user_id WHERE trucks.truck_id = %(truck_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    row = results[0]
    this_truck = cls(row)
    carrier_data = {
      **row,
      'truck_id':row['truck_id'],
      'carrier_id':row['carriers.carrier_id'],
      'created_at':row['created_at'],
      'updated_at':row['updated_at']
    }
    user_data = {
          **row,
          'user_id': row['user_id'],
          "created_at" : row['created_at'],
          'updated_at' : row['updated_at']
        }
    postee = carrier_model.Carrier(carrier_data)
    user_instance = user_model.User(user_data)
    this_truck.user = user_instance
    this_truck.postee = postee
    return this_truck

  @classmethod
  def get_all_trucks(cls,data):
    query = "SELECT * FROM trucks JOIN carriers on trucks.carrier_id = carriers.carrier_id WHERE trucks.carrier_id = %(carrier_id)s ;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) > 0:
      all_trucks=[]
      for row in results:
        this_truck = cls(row)
        creater_data = {
          **row,
          "carrier_id" :row['carrier_id'],
          "created_at" : row['created_at'],
          'updated_at' : row['updated_at']
        }
        
        posted_by = carrier_model.Carrier(creater_data)
        this_truck.postee = posted_by
        all_trucks.append(this_truck)
      return all_trucks
    return []

  @classmethod 
  def get_my_trucks_list(cls,data):
    query = "SELECT * FROM carriers LEFT JOIN trucks on carriers.carrier_id = trucks.carrier_id LEFT JOIN users on carriers.user_id = users.user_id WHERE carriers.carrier_id = %(carrier_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    carrier = cls(results[0])
    list_of_trucks = []
    for row in results:
      this_truck = cls(row)
      if row['carrier_id'] == None:
        break
      truck_data = {
        **row,
        "carrier_id" : row['trucks.carrier_id'],
        "created_at" : row['trucks.created_at'],
        'updated_at' : row['trucks.updated_at']
      }
      carrier_data = {
        **row,
        'truck_id':row['truck_id'],
        'carrier_id':row['carrier_id'],
        'created_at':row['created_at'],
        'updated_at':row['updated_at']
      }
      user_data = {
        **row,
        'user_id': row['user_id'],
        "created_at" : row['created_at'],
        'updated_at' : row['updated_at']
      }
      postee = carrier_model.Carrier(carrier_data)
      user_instance = user_model.User(user_data)
      this_truck = truck_model.Truck(truck_data)
      this_truck.postee = postee
      this_truck.user = user_instance
      list_of_trucks.append(this_truck)
    carrier.tractors = list_of_trucks
    return carrier

  @classmethod
  def delete(cls,data):
    query = "DELETE FROM trucks WHERE truck_id = %(truck_id)s;"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def get_trucks_by_origin_city(cls,data):
    query = "SELECT * FROM trucks INNER JOIN carriers ON trucks.carrier_id = carriers.carrier_id WHERE trucks.origin_city = %(origin_city)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks
  
  @classmethod
  def get_trucks_by_origin_state(cls,data):
    query = "SELECT * FROM trucks INNER JOIN carriers ON trucks.carrier_id = carriers.carrier_id WHERE trucks.origin_state = %(origin_state)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks
  
  @classmethod
  def get_trucks_by_equipment_type(cls,data):
    query = "SELECT * FROM trucks LEFT JOIN carriers ON trucks.carrier_id = carriers.carrier_id WHERE trucks.equipment_type = %(equipment_type)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks
  
  @classmethod
  def get_trucks_by_weight(cls,data):
    query = "SELECT * FROM trucks LEFT JOIN carriers ON trucks.carrier_id = carriers.carrier_id WHERE trucks.weight >= %(weight)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks
  
  @classmethod
  def get_trucks_by_rate(cls,data):
    query = "SELECT * FROM trucks LEFT JOIN carriers ON trucks.carrier_id = carriers.carrier_id LEFT JOIN users ON users.user_id = carriers.user_id WHERE trucks.rate_per_mile <= %(rate_per_mile)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks

  @classmethod
  def get_all_trucks_list(cls,data):
    query = "SELECT * FROM trucks LEFT JOIN carriers ON trucks.carrier_id = carriers.carrier_id LEFT JOIN users ON users.user_id = carriers.user_id;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks
  
  @classmethod
  def get_trucks_by_destination_city(cls,data):
    query = "SELECT * FROM trucks LEFT JOIN carriers ON trucks.carrier_id = carriers.carrier_id LEFT JOIN users ON users.user_id = carriers.user_id WHERE trucks.destination_city = %(destination_city)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks
  
  @classmethod
  def get_trucks_by_destination_state(cls,data):
    query = "SELECT * FROM trucks LEFT JOIN carriers ON trucks.carrier_id = carriers.carrier_id LEFT JOIN users ON users.user_id = carriers.user_id WHERE trucks.destination_state = %(destination_state)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks
  
  @classmethod
  def get_postees_other_trucks(cls,data):
    query = "SELECT * FROM trucks LEFT JOIN carriers ON carriers.carrier_id = trucks.truck_id ;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks = []
    for row in results:
      carrier_data = {
        **row,
        'carrier_id':row['carrier_id'],
      }
      this_truck = cls(row)
      postee = carrier_model.Carrier(carrier_data)
      this_truck.postee = postee
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    return trucks

  @classmethod
  def get_trucks(cls):
    query = "SELECT * FROM trucks LIMIT 25;"
    results = connectToMySQL(DATABASE).query_db(query)
    if len(results) < 1:
      return False
    trucks=cls(results[0])
    list_of_trucks=[]
    for row in results:
      this_truck = cls(row)
      list_of_trucks.append(this_truck)
    trucks.list = list_of_trucks
    print(trucks.list)
    return trucks
  
  @classmethod
  def update(cls,data):
    query = "UPDATE trucks SET truck_number = (%(truck_number)s),origin_city = LOWER(%(origin_city)s), origin_state = LOWER(%(origin_state)s), " \
            "origin_radius = (%(origin_radius)s),destination_city = LOWER(%(destination_city)s),destination_state = LOWER(%(destination_state)s), " \
            "destination_radius = (%(destination_radius)s),equipment_type = (%(equipment_type)s),weight = (%(weight)s),length = (%(length)s),rate_per_mile = (%(rate_per_mile)s) WHERE trucks.truck_id = %(truck_id)s;"
    return connectToMySQL(DATABASE).query_db(query,data)
  

  #---------------- staticmethods  ------------- staticmethods -----------
  @staticmethod
  def truck_validator(td):
    v = True
    if len(td['origin_city']) < 1:
      flash('Origin city is required')
      v = False
    if len(td['origin_state']) < 1:
      flash('Origin state is required')
      v = False
    if len(td['destination_state']) < 1:
      flash('Destination state is required')
      v = False
    if len(td['equipment_type']) < 1:
      flash('Equipment type is required')
      v = False
    if len(td['weight']) < 1:
      flash('Weigth able to be hauled is required')
      v = False
    if len(td['length']) < 1:
      flash('Trailer length is required')
      v = False
    return v