from flask_app import app,cap,date_hrs_subtraction,convert_from_tuple,phone_format,states
from flask import render_template, redirect, request, flash, session, jsonify
from flask_app.models.user_model import User
from flask_app.models.address_model import Address
from flask_app.models.load_model import Load
from flask_app.models.broker_model import Broker
from flask_app.models.broker_address import BrokerAddress
from flask_app.models.broker_load import BrokerLoad
from flask_app.models.truck_model import Truck
from flask_app.models.truck_encoder import TruckEncoder

from datetime import datetime
from flask_app import bcrypt
from flask import json

@app.route('/broker/sign_up')
def new_broker_user():
  if 'user_id' in session:
    return redirect('/')
  return render_template('broker_sign_up.html')

@app.route('/broker/sign_up/new_broker', methods = ['POST'])
def process_broker_user():
  if not User.user_validator(request.form):
    return redirect('/broker/sign_up')
  hashed_pw = bcrypt.generate_password_hash(request.form['password'])
  data = {
    **request.form,
    'password' : hashed_pw
  }
  session['user_id'] = Broker.create_broker_user(data)
  print(session)
  return redirect('/broker/company_info')

@app.route('/broker/company_info')
def broker_company_info():
  if 'broker_id' in session or 'carrier_id' in session or 'shipper_id' in session:
    return redirect('/')
  return render_template('/broker_info.html', states=states)

@app.route('/broker/register', methods=['POST'])
def broker_register():
  if not Broker.broker_validator(request.form):
    return redirect('/broker/company_info')
  data = {
    **request.form,
    'user_id':session['user_id']
  }
  session['broker_id'] = Broker.create_broker_info(data)
  session['address_id'] = Address.create_address(data)
  broker_ids = {
    'address_id':session['address_id'],
    'broker_id':session['broker_id']
  }
  session['load_id'] = 0
  BrokerAddress.create_broker_address(broker_ids)
  return redirect('/broker/dashboard')

@app.route('/broker/dashboard')
def broker_dashboard():
  if 'broker_id' not in session:
    flash('You are not signed-in as a broker')
    return redirect('/login')
  data = {
    'user_id':session['user_id'],
    'address_id':session['address_id'],
    'broker_id':session['broker_id'],
    'load_id':session['load_id']
  }
  logged_broker = Broker.get_by_id(data)
  logged_user = User.get_by_id(data)
  #this is a Load object which has the attribute ".loads"
    #that attribute is a list of the loads as objects
  my_loads = Load.get_my_loads_list_broker(data)
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")
  
  sorted_loads = sorted(my_loads.loads,key=lambda l: l.created_at, reverse=True)
  return render_template('broker_dashboard.html',
    broker=logged_broker,
    user=logged_user,
    my_loads=sorted_loads,
    now=now,
    cap=cap,
    date_hrs_subtraction=date_hrs_subtraction,
    convert_from_tuple=convert_from_tuple
  )

@app.route('/broker/add_load')
def post_broker_load():
  data = {
    'user_id':session['user_id'],
    "address_id":session['address_id'],
    'broker_id':session['broker_id']
  }
  logged_broker = Broker.get_by_id(data)
  logged_user = User.get_by_id(data)

  return render_template('broker_load.html',
    broker=logged_broker,
    states=states,
    user=logged_user,
    cap=cap
  )

@app.route('/broker/process/load', methods=["POST"])
def process_broker_load():
  if not Load.load_validator(request.form):
    return redirect('/broker/add_load')
  data = {
    **request.form,
    'broker_id':session['broker_id']
  }

  session['load_id'] = Load.create_load(data)
  load_ids = {
    'load_id':session['load_id'],
    'broker_id':session['broker_id']
  }
  BrokerLoad.create_broker_load(load_ids)
  return redirect('/broker/dashboard')

@app.route('/broker/load/<int:load_id>')
def broker_load_view(load_id):
  load = Load.get_load_by_broker_id({'load_id':load_id})
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")

  return render_template('load_details.html',
    load = load,
    date_hrs_subtraction=date_hrs_subtraction,
    now=now,
    cap=cap,
    phone_format=phone_format
  )

@app.route('/broker/<int:load_id>/delete')
def delete_broker_load(load_id):
  #checking if there is a broker logged in
  if 'broker_id' not in session:
    flash('You must be signed-in as a broker inorder to do this.')
    if 'carrier_id' in session:
      return redirect('/carrier/dashboard')
    elif 'shipper_id' in session:
      return redirect('/shipper/dashboard')
    else:
      return redirect('/')

  #getting the shippers id and loads corresponding shippers' id
  bid = Broker.get_by_id({'broker_id':session['broker_id']})
  load_bid = Load.get_broker_by_load_id({'load_id':load_id})

  #if load does not exist it returns false, this handles that
  if load_bid == False:
    flash('The load you tried to delete does not exist.')
    return redirect('/broker/dashboard')
  #if the shipper id in session odes not match the loads' shippers' id flash error
  elif bid.broker_id != load_bid['broker_id']:
    flash('You did not post this load, therefore you cannot delete it.')
  else:
    Load.delete_broker_load({'load_id':load_id})
  
  data = {
    'user_id':session['user_id'],
    'address_id':session['address_id'],
    'broker_id':session['broker_id'],
    'load_id':session['load_id']
  }
  my_loads = Load.get_my_loads_list_broker(data)
  if len(my_loads.loads) >= 1:
    session['load_id'] = my_loads.load_id
  else:
    session['load_id'] = 0
  
  return redirect('/broker/dashboard')

@app.route('/broker/<int:load_id>/edit')
def edit_broker_load(load_id):
  if 'broker_id' not in session:
    flash('You must be signed-in as a broker inorder to do this.')
    if 'carrier_id' in session:
      return redirect('/carrier/dashboard')
    elif 'shipper_id' in session:
      return redirect('/shipper/dashboard')
    else:
      return redirect('/')
    
  bid = Broker.get_by_id({'broker_id':session['broker_id']})
  lid = Load.get_load_by_broker_id({'load_id':load_id})

  if lid == False:
    flash("The load you tried to edit does not exist")
    return redirect('/broker/dashboard')
  elif bid.user_id != lid.postee.user_id:
    flash('You did not post the load you are trying to edit')
    return redirect('/shipper/dashboard')
  
  return render_template('/broker_edit_load.html',
    load=lid,
    broker=bid,
    cap=cap,
    date_hrs_subtraction=date_hrs_subtraction,
    convert_from_tuple=convert_from_tuple,
    states=states
  )

@app.route('/broker/<int:load_id>/update', methods=['POST'])
def update_broker_load(load_id):
  if 'broker_id' not in session:
    flash('You must be signed-in as a broker inorder to do this.')
    if 'carrier_id' in session:
      return redirect('/carrier/dashboard')
    elif 'shipper_id' in session:
      return redirect('/shipper/dashboard')
    else:
      return redirect('/')
    
  bid = Broker.get_by_id({'broker_id':session['broker_id']})
  lid = Load.get_load_by_broker_id({'load_id':load_id})

  if lid == False:
    flash("The load you tried to edit does not exist")
    return redirect('/broker/dashboard')
  elif bid.user_id != lid.postee.user_id:
    flash('You did not post the load you are trying to edit')
    return redirect('/shipper/dashboard')
  
  data = {
    **request.form,
    'load_id':load_id
  }

  if not Load.load_validator(data):
    flash('Something went wrong')
    return redirect(f'/broker/{load_id}/edit')
  else:
    Load.update(data)

  return redirect('/broker/dashboard')