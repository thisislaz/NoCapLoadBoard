from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE,flash
from flask_app.models import user_model,shipper_model, load_model,broker_model
from datetime import datetime

class Load:
  def __init__(self,data):
    self.load_id = data['load_id']
    self.load_number = data['load_number']
    self.origin_city = data['origin_city']
    self.origin_state = data['origin_state']
    self.destination_city = data['destination_city']
    self.destination_state = data['destination_state']
    self.pickup_date = data['pickup_date']
    self.delivery_date = data['delivery_date']
    self.equipment_type = data['equipment_type']
    self.rate_per_mile = data['rate_per_mile']
    self.weight = data['weight']
    self.size = data['size']
    self.length = data['length']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @classmethod
  def create_load(cls,data):
    query = "INSERT INTO loads (load_number,origin_city,origin_state,destination_city,destination_state,pickup_date,delivery_date,equipment_type,rate_per_mile,weight,size,length) VALUES (%(load_number)s,LOWER(%(origin_city)s),LOWER(%(origin_state)s),LOWER(%(destination_city)s),LOWER(%(destination_state)s),%(pickup_date)s,%(delivery_date)s,%(equipment_type)s,%(rate_per_mile)s,%(weight)s,%(size)s,%(length)s);"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def get_load_by_shipper_id(cls,data):
    query = "SELECT * FROM loads LEFT JOIN shipper_load ON loads.load_id = shipper_load.load_id LEFT JOIN shippers ON shipper_load.shipper_id = shippers.shipper_id LEFT JOIN users ON shippers.user_id = users.user_id WHERE loads.load_id = %(load_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    row = results[0]
    this_load = cls(row)
    shipper_data = {
      **row,
      'load_id': row['load_id'],
      'shipper_id': row['shipper_id'],
      'created_at': row['created_at'],
      'updated_at': row['updated_at']
    }
    user_data = {
      **row,
      'user_id': row['user_id'],
      "created_at" : row['created_at'],
      'updated_at' : row['updated_at']
    }
    postee = shipper_model.Shipper(shipper_data)
    user_instance = user_model.User(user_data)
    this_load.postee = postee
    this_load.user = user_instance
    return this_load

  @classmethod
  def get_load_by_broker_id(cls,data):
    query = "SELECT * FROM loads LEFT JOIN broker_load ON loads.load_id = broker_load.load_id LEFT JOIN brokers ON broker_load.broker_id = brokers.broker_id LEFT JOIN users ON brokers.user_id = users.user_id WHERE loads.load_id = %(load_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    row = results[0]
    this_load = cls(row)
    broker_data = {
      **row,
      'load_id': row['load_id'],
      'broker_id': row['broker_id'],
      'created_at': row['created_at'],
      'updated_at': row['updated_at']
    }
    user_data = {
      **row,
      'user_id': row['user_id'],
      "created_at" : row['created_at'],
      'updated_at' : row['updated_at']
    }
    postee = broker_model.Broker(broker_data)
    user_instance = user_model.User(user_data)
    this_load.postee = postee
    this_load.user = user_instance
    return this_load

  @classmethod
  def get_my_loads_list_shipper(cls,data):
    query = "SELECT * FROM shippers LEFT JOIN shipper_load ON shipper_load.shipper_id = shippers.shipper_id LEFT JOIN loads ON shipper_load.load_id = loads.load_id LEFT JOIN users ON shippers.user_id = users.user_id WHERE shippers.shipper_id =  %(shipper_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1: 
      return False
    shipper = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      if row['shipper_id'] == None:
        break
      load_data = {
        **row,
        "shipper_id": row['shipper_id'],
        'created_at': row['loads.created_at'],
        'updated_at': row['loads.updated_at']
      }
      shipper_data = {
        **row,
        'load_id': row['load_id'],
        'shipper_id': row['shipper_id'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
      }
      user_data = {
        **row,
        'user_id': row['user_id'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
      }
      postee = shipper_model.Shipper(shipper_data)
      user_instance = user_model.User(user_data)
      this_load = load_model.Load(load_data)
      this_load.postee = postee
      this_load.user = user_instance
      list_of_loads.append(this_load)
    shipper.loads = list_of_loads
    return shipper

  @classmethod
  def get_my_loads_list_broker(cls,data):
    query = "SELECT * FROM brokers LEFT JOIN broker_load ON broker_load.broker_id = brokers.broker_id LEFT JOIN loads ON broker_load.load_id = loads.load_id LEFT JOIN users ON brokers.user_id = users.user_id WHERE brokers.broker_id =  %(broker_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1: 
      return False
    broker = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      if row['broker_id'] == None:
        break
      load_data = {
        **row,
        "broker_id": row['broker_id'],
        'created_at': row['loads.created_at'],
        'updated_at': row['loads.updated_at']
      }
      broker_data = {
        **row,
        'load_id': row['load_id'],
        'broker_id': row['broker_id'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
      }
      user_data = {
        **row,
        'user_id': row['user_id'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
      }
      postee = broker_model.Broker(broker_data)
      user_instance = user_model.User(user_data)
      this_load = load_model.Load(load_data)
      this_load.postee = postee
      this_load.user = user_instance
      list_of_loads.append(this_load)
    broker.loads = list_of_loads
    return broker

  @classmethod
  def get_shipper_by_load_id(cls,data):
    query = "SELECT * FROM shipper_load INNER JOIN loads ON shipper_load.load_id = loads.load_id INNER JOIN shippers ON shippers.shipper_id = shipper_load.shipper_id WHERE loads.load_id = %(load_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return results[0]

  @classmethod
  def get_broker_by_load_id(cls,data):
    query = "SELECT * FROM broker_load INNER JOIN loads ON broker_load.load_id = loads.load_id INNER JOIN brokers ON brokers.broker_id = broker_load.broker_id WHERE loads.load_id = %(load_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    return results[0]
  
  @classmethod
  def delete_shipper_load(cls,data):
    query = "DELETE shipper_load, loads FROM shipper_load INNER JOIN loads ON shipper_load.load_id = loads.load_id WHERE loads.load_id = %(load_id)s;"
    return connectToMySQL(DATABASE).query_db(query,data)

  @classmethod
  def delete_broker_load(cls,data):
    query = "DELETE broker_load, loads FROM broker_load INNER JOIN loads ON broker_load.load_id = loads.load_id WHERE loads.load_id = %(load_id)s;"
    return connectToMySQL(DATABASE).query_db(query,data)
  
  @classmethod
  def get_all_loads_list_no_limit(cls,data):
    query = "SELECT * FROM loads;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads=cls(results[0])
    list_of_loads=[]
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_loads_by_rate(cls,data):
    query = "SELECT * FROM loads WHERE loads.rate_per_mile >= %(rate_per_mile)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_loads_by_origin_city(cls,data):
    query = "SELECT * FROM loads WHERE loads.origin_city = %(origin_city)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_loads_by_origin_state(cls,data):
    query = "SELECT * FROM loads WHERE loads.origin_state = %(origin_state)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_loads_by_destination_city(cls,data):
    query = "SELECT * FROM loads WHERE loads.destination_city = %(destination_city)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_loads_by_destination_state(cls,data):
    query = "SELECT * FROM loads WHERE loads.destination_state = %(destination_state)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_loads_by_equipment_type(cls,data):
    query = "SELECT * FROM loads WHERE loads.equipment_type = %(equipment_type)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_loads_by_size(cls,data):
    query = "SELECT * FROM loads WHERE loads.size = %(size)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def get_load_by_id(cls,data):
    query = "SELECT * FROM loads LEFT JOIN broker_load ON loads.load_id = broker_load.load_id LEFT JOIN shipper_load ON  loads.load_id = shipper_load.load_id LEFT JOIN shippers ON shipper_load.shipper_id = shippers.shipper_id LEFT JOIN brokers ON broker_load.broker_id = brokers.broker_id LEFT JOIN users AS broker_users ON brokers.user_id = broker_users.user_id LEFT JOIN users AS shipper_users ON shippers.user_id = shipper_users.user_id WHERE loads.load_id = %(load_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    row = results[0]
    if row['broker_id'] != None:
      broker_data = {
        **row,
        'broker_id':row['broker_id'],
        'company_name':row['brokers.company_name'],
        'company_phone':row['brokers.company_phone'],
        'us_dot':row['us_dot'],
        'mc_number':row['mc_number'],
        'created_at':row['brokers.created_at'],
        'updated_at':row['brokers.updated_at'],
        'user_id':row['brokers.user_id']
      }
      user_data = {
        **row,
        'user_id':row['broker_users.user_id'],
        'email':row['email'],
        'first_name':row['first_name'],
        'last_name':row['last_name'],
        'created_at':row['broker_users.created_at'],
        'updated_at':row['broker_users.updated_at'],
      }
      postee = broker_model.Broker(broker_data)
      user_instance = user_model.User(user_data)
      this_load = cls(row)
      this_load.postee = postee
      this_load.user = user_instance
      return this_load
    elif row['broker_id'] == None:
      shipper_data = {
        **row,
        'shipper_id':row['shipper_id'],
        'company_name':row['company_name'],
        'company_phone':row['company_phone'],
        'created_at':row['shippers.created_at'],
        'updated_at':row['shippers.updated_at'],
        'user_id':row['shipper_users.user_id']
      }
      user_data = {
        **row,
        'user_id':row['shipper_users.user_id'],
        'email':row['shipper_users.email'],
        'first_name':row['shipper_users.first_name'],
        'last_name':row['shipper_users.last_name'],
        'created_at':row['shipper_users.created_at'],
        'updated_at':row['shipper_users.updated_at'],
      }
      postee = shipper_model.Shipper(shipper_data)
      user_instance = user_model.User(user_data)
      this_load = cls(row)
      this_load.postee = postee
      this_load.user = user_instance
      return this_load
  
  @classmethod
  def get_postees_other_loads(cls,data):
    query = "SELECT * FROM loads LEFT JOIN broker_load ON loads.load_id = broker_load.load_id LEFT JOIN shipper_load ON loads.load_id = shipper_load.load_id LEFT JOIN shippers ON shipper_load.shipper_id = shippers.shipper_id LEFT JOIN brokers ON  broker_load.broker_id = brokers.broker_id LEFT JOIN users AS broker_users ON  brokers.user_id = broker_users.user_id LEFT JOIN users AS shipper_users ON shippers.user_id = shipper_users.user_id WHERE shipper_users.user_id = %(user_id)s OR broker_users.user_id = %(user_id)s;"
    results = connectToMySQL(DATABASE).query_db(query,data)
    if len(results) < 1:
      return False
    loads = cls(results[0])
    list_of_loads = []
    for row in results:
      print('********** row',row)
      if row['broker_id'] == None:
        shipper_data = {
        **row,
        'shipper_id':row['shippers.shipper_id'],
        'company_name':row['company_name'],
        'company_phone':row['company_phone'],
        'created_at':row['shippers.created_at'],
        'updated_at':row['shippers.updated_at'],
        }
        user_data = {
          **row,
          'user_id':row['user_id'],
          'email':row['shipper_users.email'],
          'first_name':row['shipper_users.first_name'],
          'last_name':row['shipper_users.last_name'],
          'created_at':row['shipper_users.created_at'],
          'updated_at':row['shipper_users.updated_at'],
        }
        print('---------shipper_user_data',user_data)
        this_load = cls(row)
        postee = shipper_model.Shipper(shipper_data)
        user_instance = user_model.User(user_data)
        this_load.postee = postee
        this_load.user = user_instance
        list_of_loads.append(this_load)
        loads.list = list_of_loads
      if row['broker_id'] != None:
        broker_data = {
        **row,
        'broker_id':row['broker_id'],
        'company_name':row['brokers.company_name'],
        'company_phone':row['brokers.company_phone'],
        'us_dot':row['us_dot'],
        'mc_number':row['mc_number'],
        'created_at':row['brokers.created_at'],
        'updated_at':row['brokers.updated_at'],
        }
        user_data = {
          **row,
          'user_id':row['brokers.user_id'],
          'email':row['email'],
          'first_name':row['first_name'],
          'last_name':row['last_name'],
          'created_at':row['broker_users.created_at'],
          'updated_at':row['broker_users.updated_at'],
        }
        print('-----------broker_user_data',user_data)
        this_load = cls(row)
        postee = broker_model.Broker(broker_data)
        user_instance = user_model.User(user_data)
        this_load.postee = postee
        this_load.user = user_instance
        list_of_loads.append(this_load)
        loads.list = list_of_loads
    
    return loads
    
  @classmethod
  def get_all_loads_list(cls):
    query = "SELECT * FROM loads LIMIT 25;"
    results = connectToMySQL(DATABASE).query_db(query)
    if len(results) < 1:
      return False
    loads=cls(results[0])
    list_of_loads=[]
    for row in results:
      this_load = cls(row)
      list_of_loads.append(this_load)
    loads.list = list_of_loads
    return loads
  
  @classmethod
  def update(cls,data):
    query = "UPDATE loads SET load_number = %(load_number)s,origin_city = LOWER(%(origin_city)s),origin_state = LOWER(%(origin_state)s),pickup_date = LOWER(%(pickup_date)s),destination_city = LOWER(%(destination_city)s),destination_state = LOWER(%(destination_state)s),delivery_date = LOWER(%(delivery_date)s),equipment_type = LOWER(%(equipment_type)s),weight = LOWER(%(weight)s),length = LOWER(%(length)s),rate_per_mile = LOWER(%(rate_per_mile)s),size = LOWER(%(size)s) WHERE loads.load_id = %(load_id)s;"
    return connectToMySQL(DATABASE).query_db(query,data)


#------------------- staticmethods ========= staticmethods -------------------
  @staticmethod
  def load_validator(ld):
    v = True
    if len(ld['origin_state']) < 1:
      flash('Origin state required')
      v=False
    if len(ld['pickup_date']) < 1:
      flash('Pick up date is required')
      v=False
    if len(ld['destination_state']) < 1:
      flash('Destination state required')
      v=False
    if len(ld['delivery_date']) < 1:
      flash('Delivery date is required')
      v=False
    if len(ld['equipment_type']) < 1:
      flash('Equipment type is required')
      v=False
    if len(ld['length']) < 1:
      flash('Length is required')
      v=False
    if len(ld['size']) < 1:
      flash('Size is required')
      v=False
    return v