from flask_app import app,cap,date_hrs_subtraction,phone_format,convert_from_tuple,states
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.carrier_model import Carrier
from flask_app.models.shipper_model import Shipper
from flask_app.models.carrier_address import CarrierAddress
from flask_app.models.truck_model import Truck
from flask_app.models.shipper_address import ShipperAddress
from flask_app.models.load_model import Load
from flask_app.models.broker_model import Broker
from flask_app.models.broker_address import BrokerAddress
from flask_app import bcrypt
from datetime import datetime

#Index page where they select which sign-up they want
@app.route('/')
def index():
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")
  try:
    if 'user_id' in session:
      lu = User.get_by_id({"user_id": session['user_id']})
      load = Load.get_all_loads_list()
      sl = sorted(load.list, key=lambda l:l.created_at, reverse=True)

      truck = Truck.get_trucks()
      st = sorted(truck.list, key=lambda t:t.created_at, reverse=True)
      return render_template("index.html",
        lu=lu,
        loads=sl,
        trucks=st,
        cap=cap,
        date_hrs_subtraction=date_hrs_subtraction,
        now=now,
        convert_from_tuple=convert_from_tuple
      )
    else:
      load = Load.get_all_loads_list()
      sl = sorted(load.list, key=lambda l:l.created_at, reverse=True)

      truck = Truck.get_trucks()
      st = sorted(truck.list, key=lambda t:t.created_at, reverse=True)
      return render_template("index.html",
        loads=sl,
        trucks=st,
        cap=cap,
        date_hrs_subtraction=date_hrs_subtraction,
        now=now,
        convert_from_tuple=convert_from_tuple
      )
  
  except:
    try:
      if 'user_id' in session:
        lu = User.get_by_id({"user_id": session['user_id']})

        load = Load.get_all_loads_list()
        sl = sorted(load.list, key=lambda l:l.created_at, reverse=True)

        truck = Truck.get_trucks()
        st = sorted(truck.list, key=lambda t:t.created_at, reverse=True)

        return render_template("index.html",
          lu=lu,
          loads=sl,
          trucks=st,
          cap=cap,
          date_hrs_subtraction=date_hrs_subtraction,
          now=now,
          convert_from_tuple=convert_from_tuple
        )
      else:
        load = Load.get_all_loads_list()
        sl = sorted(load.list, key=lambda l:l.created_at, reverse=True)

        truck = Truck.get_trucks()
        st = sorted(truck.list, key=lambda t:t.created_at, reverse=True)

        return render_template("index.html",
          loads=sl,
          trucks=st,
          cap=cap,
          date_hrs_subtraction=date_hrs_subtraction,
          now=now,
          convert_from_tuple=convert_from_tuple
        )
    except:
      if "user_id" in session:
        lu = User.get_by_id({"user_id": session['user_id']})
        return render_template("index.html",
          lu=lu,
          cap=cap,
          date_hrs_subtraction=date_hrs_subtraction,
          now=now,
          convert_from_tuple=convert_from_tuple
        )
      else:
        return render_template("index.html",
          cap=cap,
          date_hrs_subtraction=date_hrs_subtraction,
          now=now,
          convert_from_tuple=convert_from_tuple
        )


#Log in page with email and pass required/ links to register if they dont have an account
@app.route('/login')
def log_in():
  if 'user_id' in session:
    return redirect('/')
  return render_template('login.html')

@app.route('/login/user', methods=['POST'])
def log_in_user():
  data = {
    "email": request.form['email']
  }
  #using the data object to search for the user, then storing it's user_id in session
  try:
    user_in_db = User.get_by_email(data)
    session['user_id'] = user_in_db.user_id
    #reasigning data to store session
    data = {
      "user_id" : session['user_id']
    }
  except:
    flash('Not a registered email.')
    return redirect('/login')

  #using data obj to search for carrier by user_id
  try:
    #if its a carrier do all of this
      # add the carrier_id to session
    carrier_in_db = Carrier.get_by_user_id(data)
    session['carrier_id'] = carrier_in_db.carrier_id
      #add the carrier's address_id to session
    address_in_db = CarrierAddress.get_address_by_id({"carrier_id":carrier_in_db.carrier_id})
    session['address_id'] = address_in_db.carrier_id
      # add the trucks avaiable to a list of trucks
    all_trucks = Truck.get_all_trucks({"carrier_id": carrier_in_db.carrier_id})
    #loop thru truck list then grab the id from the trucks
    for truck in all_trucks:
        #set the truck_id in session equal to the truck's id
      truck_in_db = truck.truck_id
    if len(all_trucks) < 1:
      truck_in_db = 0
    if truck_in_db == False or truck_in_db == None:
      session['truck_id'] = 0
    session['truck_id'] = truck_in_db
  except:
    pass

  try:
    shipper_in_db = Shipper.get_by_user_id(data)
    session['shipper_id'] = shipper_in_db.shipper_id

    address_in_db = ShipperAddress.get_address_by_id({'shipper_id':shipper_in_db.shipper_id})
    session['address_id'] = address_in_db.shipper_id

    # this returns the list as an attribute inside a load object
      #access the loads with the .load attribute
    all_loads = Load.get_my_loads_list_shipper({'shipper_id':shipper_in_db.shipper_id}).loads
    for load in all_loads:
      load_in_db = load.load_id
    if len(all_loads) < 1:
      load_in_db = 0
    if load_in_db == False or load_in_db == None:
      session['load_id'] = 0
    session['load_id'] = load_in_db
  except:
    pass
  
  try:
    broker_in_db = Broker.get_by_user_id(data)
    session['broker_id'] = broker_in_db.broker_id

    address_in_db = BrokerAddress.get_address_by_broker_id({'broker_id':broker_in_db.broker_id})
    session['address_id'] = address_in_db.broker_id

    all_loads = Load.get_my_loads_list_broker({'broker_id':broker_in_db.broker_id}).loads
    for load in all_loads:
      load_in_db = load.load_id
    if len(all_loads) < 1:
      load_in_db = 0
    if load_in_db == False or load_in_db == None:
      session['load_id'] = 0
    session['load_id'] = load_in_db
  except:
    pass

  if "carrier_id" in session:
    return redirect('/carrier/dashboard')
  elif "shipper_id" in session:
    return redirect('/shipper/dashboard')
  elif 'broker_id' in session:
    return redirect('/broker/dashboard')

#logout all
@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

@app.route('/start_over')
def start_over():
  user = User.get_by_id({'user_id':session['user_id']})
  User.delete_user({"user_id":user.user_id})
  session.clear()
  return redirect('/')