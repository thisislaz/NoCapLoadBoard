from flask_app import app,cap,date_hrs_subtraction,convert_from_tuple,phone_format,states
from flask import render_template, redirect, request, flash, session, jsonify
from flask_app.models.user_model import User
from flask_app.models.carrier_model import Carrier
from flask_app.models.address_model import Address
from flask_app.models.shipper_address import ShipperAddress
from flask_app.models.truck_model import Truck
from flask_app.models.shipper_model import Shipper
from flask_app.models.load_model import Load
from flask_app.models.shipper_load import ShipperLoad
import json
from flask_app.models.truck_encoder import TruckEncoder
from datetime import datetime
from flask_app import bcrypt

#new user as a shipper
@app.route('/shipper/sign_up')
def new_shipper_user():
  if 'user_id' in session:
    return redirect('/')
  return render_template('shipper_sign_up.html')

@app.route('/shipper/sign_up/new_shipper', methods=['POST'])
def process_shipper_user():
  if not User.user_validator(request.form):
    return redirect('/shipper/sign_up')
  hashed_pw = bcrypt.generate_password_hash(request.form['password'])
  data = {
    **request.form,
    'password' : hashed_pw
  }
  session['user_id'] = Shipper.create_shipper_user(data)
  print(session)
  return redirect('/shipper/company_info')

@app.route('/shipper/company_info')
def shipper_company_info():
  if 'broker_id' in session or 'carrier_id' in session or 'shipper_id' in session:
    return redirect('/')
  return render_template('shipper_info.html',states=states)

@app.route('/shipper/register', methods=['POST'])
def shipper_register():
  if not Shipper.shipper_validator(request.form):
    return redirect('/shipper/company_info')
  data = {
    **request.form,
    'user_id' : session['user_id']
  }
  session['shipper_id'] = Shipper.create_shipper_info(data)
  session['address_id'] = Address.create_address(data)
  shipper_ids = {
    'address_id' : session['address_id'],
    'shipper_id' : session['shipper_id']
  }
  session['load_id'] = 0
  ShipperAddress.create_shipper_address(shipper_ids)
  print(session)
  return redirect('/shipper/dashboard')

@app.route('/shipper/dashboard')
def shipper_dashboard():
  if 'shipper_id' not in session:
    flash('You are not signed-in as a shipper')
    return redirect('/login')
  data = {
    'user_id':session['user_id'],
    'address_id':session['address_id'],
    'shipper_id':session['shipper_id'],
    'load_id':session['load_id']
  }

  logged_shipper = Shipper.get_by_id(data)
  logged_user = User.get_by_id(data)
  #this is a Load object which has the attribute ".loads"
    #that attribute is a list of the loads as objects
  my_loads = Load.get_my_loads_list_shipper(data)
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")
  
  sorted_loads = sorted(my_loads.loads,key=lambda l: l.created_at, reverse=True)
  print("------shipper/dashboard",session)

  return render_template('shipper_dashboard.html',
    shipper = logged_shipper,
    user = logged_user,
    my_loads=sorted_loads,
    now=now,
    cap=cap,
    date_hrs_subtraction=date_hrs_subtraction,
    convert_from_tuple=convert_from_tuple
  )

@app.route('/shipper/add_load')
def post_load():
  data = {
    'user_id':session['user_id'],
    "address_id":session['address_id'],
    'shipper_id':session['shipper_id']
  }
  logged_shipper = Shipper.get_by_id(data)
  logged_user = User.get_by_id(data)
  print('------shipper/add_load',session)
  return render_template('shipper_load.html',
    states=states,
    shipper=logged_shipper,
    user=logged_user,
    cap=cap
  )

@app.route('/shipper/process/load', methods=["POST"])
def process_load():
  if not Load.load_validator(request.form):
    return redirect('/shipper/add_load')
  data = {
    **request.form,
    'shipper_id':session['shipper_id'],
  }
  session['load_id'] = Load.create_load(data)
  load_ids = {
    'load_id':session['load_id'],
    'shipper_id':session['shipper_id']
  }
  ShipperLoad.create_shipper_load(load_ids)
  print('------shipper/process/load',session)
  return redirect('/shipper/dashboard')

@app.route('/shipper/<int:load_id>/delete')
def delete_load(load_id):
  #checking if there is a shipper logged in
  if 'shipper_id' not in session:
    flash('You must be signed-in as a shipper inorder to do this.')
    if 'carrier_id' in session:
      return redirect('/carrier/dashboard')
    elif 'broker_id' in session:
      return redirect('/broker/dashboard')
    else:
      return redirect('/')

  #getting the shippers id and loads corresponding shippers' id
  sid = Shipper.get_by_id({'shipper_id':session['shipper_id']})
  load_sid = Load.get_shipper_by_load_id({'load_id':load_id})
  
  #if load does not exist it returns false, this handles that
  if load_sid == False:
    flash('The load you tried to delete does not exist.')
    return redirect('/shipper/dashboard')
  #if the shipper id in session does not match the loads' shippers' id flash errors
  elif sid.shipper_id != load_sid['shipper_id']:
    flash('You did not post this load, therefore you cannot delete it.')
  else:
    Load.delete_shipper_load({'load_id':load_id})

  data = {
    'user_id':session['user_id'],
    'address_id':session['address_id'],
    'shipper_id':session['shipper_id'],
    'load_id':session['load_id']
  }
  my_loads = Load.get_my_loads_list_shipper(data)
  print(my_loads)
  if len(my_loads.loads) >= 1:
    session['load_id'] = my_loads.load_id
  else:
    session['load_id'] = 0

  return redirect('/shipper/dashboard')

@app.route('/shipper/load/<int:load_id>')
def shipper_load_view(load_id):
  load = Load.get_load_by_shipper_id({'load_id':load_id})
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")
  print('------ /shipper/load/<int:id>',session)
  

  return render_template('load_details.html',
    load = load,
    date_hrs_subtraction=date_hrs_subtraction,
    now=now,
    cap=cap,
    phone_format=phone_format
  )

@app.route('/shipper/<int:load_id>/edit')
def edit_shipper_load(load_id):
  if 'shipper_id' not in session:
    flash('You must be signed-in as a shipper inorder to do this.')
    if 'carrier_id' in session:
      return redirect('/carrier/dashboard')
    elif 'broker_id' in session:
      return redirect('/broker/dashboard')
    else:
      return redirect('/')
    
  sid = Shipper.get_by_id({'shipper_id':session['shipper_id']})
  lid = Load.get_load_by_shipper_id({'load_id':load_id})

  if lid == False:
    flash("The load you tried to edit does not exist")
    return redirect('/shipper/dashboard')
  elif sid.user_id != lid.postee.user_id:
    flash("You did not post load you are trying to edit")
    return redirect('/shipper/dashboard')
  
  return render_template('/shipper_edit_load.html',
    load=lid,
    shipper=sid,
    cap=cap,
    date_hrs_subtraction=date_hrs_subtraction,
    convert_from_tuple=convert_from_tuple,
    states=states
  )

@app.route('/shipper/<int:load_id>/update', methods=['POST'])
def update_shipper_load(load_id):
  if 'shipper_id' not in session:
    flash('You must be signed-in as a shipper inorder to do this.')
    if 'carrier_id' in session:
      return redirect('/carrier/dashboard')
    elif 'broker_id' in session:
      return redirect('/broker/dashboard')
    else:
      return redirect('/')
    
  sid = Shipper.get_by_id({'shipper_id':session['shipper_id']})
  lid = Load.get_load_by_shipper_id({'load_id':load_id})

  if lid == False:
    flash("The load you tried to edit does not exist")
    return redirect('/shipper/dashboard')
  elif sid.user_id != lid.postee.user_id:
    flash("You did not post load you are trying to edit")
    return redirect('/shipper/dashboard')
  
  data = {
    **request.form,
    'load_id':load_id
  }

  if not Load.load_validator(data):
    flash('Something went wrong')
    return redirect(f'/shipper/{load_id}/edit')
  else:
    Load.update(data)

  return redirect('/shipper/dashboard')