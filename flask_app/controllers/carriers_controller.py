from flask_app import app,cap,date_hrs_subtraction,convert_from_tuple,states
from flask import render_template, redirect, request, flash, session, jsonify
from flask_app.models.user_model import User
from flask_app.models.carrier_model import Carrier
from flask_app.models.address_model import Address
from flask_app.models.carrier_address import CarrierAddress
from flask_app.models.truck_model import Truck
from datetime import datetime
from flask_app import bcrypt
import us

#New user as a carrier form
@app.route('/carrier/sign_up')
def new_carrier_user():
  if 'user_id' in session:
    return redirect('/')
  return render_template('carrier_sign_up.html')

#New user as a carrier form submisson
@app.route('/carrier/sign_up/new_carrier', methods=['POST'])
def process_carrier_user():
  if 'user_id' in session:
    return redirect('/carrier/sign_up')
  if not User.user_validator(request.form):
    return redirect('/carrier/sign_up')
  hashed_pw = bcrypt.generate_password_hash(request.form['password'])
  data = {
    **request.form,
    'password' : hashed_pw
  }
  #this next line returns the "user_id" from "users" tables
  session['user_id'] = Carrier.create_carrier_user(data)
  return redirect('/carrier/company_info')

#Entering company info for carriers
@app.route('/carrier/company_info')
def carrier_company_info():
  if 'broker_id' in session or 'carrier_id' in session or 'shipper_id' in session:
    return redirect('/')
  return render_template('carrier_info.html',states=states)

#Processing the company info for carriers
@app.route('/carrier/register', methods=['POST'])
def carrier_register():
  if not Carrier.carrier_validator(request.form):
    return redirect('/carrier/company_info')
  data = {
    **request.form,
    'user_id' : session['user_id']
  }
  session['carrier_id'] = Carrier.create_carrier_info(data)
  session['address_id'] = Address.create_address(data)
  carrier_ids = {
    'address_id' : session['address_id'],
    'carrier_id' : session['carrier_id']
  }
  session['truck_id'] = 0
  CarrierAddress.create_carrier_address(carrier_ids)
  return redirect('/carrier/dashboard')

@app.route('/carrier/add_truck')
def post_truck():
  if 'carrier_id' not in session or 'user_id' not in session:
    flash('You must be logged in as a carrier.')
    return redirect('/')
  data = {
    'user_id' : session['user_id'],
    'address_id' : session['address_id'],
    'carrier_id' : session['carrier_id']
  }
  log_carrier = Carrier.get_by_id(data)
  log_user = User.get_by_id(data)
  return render_template('truck.html',
    states=states,
    carrier=log_carrier,
    user=log_user,
    cap=cap
  )

@app.route('/carrier/process/truck', methods=['POST'])
def process_truck():
  
  data = {
    **request.form,
    'carrier_id' : session['carrier_id']
  }
  if not Truck.truck_validator(data):
    return redirect('/carrier/add_truck')

  session['truck_id'] = Truck.create_truck(data)
  return redirect('/carrier/dashboard')

#Dashboard for carriers
@app.route('/carrier/dashboard')
def carrier_dashboard():
  if 'carrier_id' not in session:
    flash('You are not signed-in as a carrier')
    return redirect('/login')
  data = {
    'user_id' : session['user_id'],
    'address_id' : session['address_id'],
    'carrier_id' : session['carrier_id'],
    'truck_id' : session['truck_id']
  }
  log_carrier = Carrier.get_by_id(data)
  log_user = User.get_by_id(data)
  log_truck = Truck.get_by_id(data)
  # all_trucks = Truck.get_all_trucks(data)
  my_trucks = Truck.get_my_trucks_list(data)
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")

  # new_trucks = sorted(all_trucks,key=lambda truck: truck.created_at, reverse=True)
  new_t = sorted(my_trucks.tractors,key=lambda t: t.created_at, reverse=True)
  for t in new_t:
    print(t.truck_number,t.destination_state,t.equipment_type,t.length,t.rate_per_mile)
  return render_template('carrier_dashboard.html', 
    _carrier=log_carrier, 
    _user=log_user,
    truck=log_truck,
    # trucks=new_trucks, 
    now=now,
    new_t=new_t,
    date_hrs_subtraction=date_hrs_subtraction,
    cap=cap,
    convert_from_tuple=convert_from_tuple
  )

@app.route('/carrier/<int:truck_id>/delete')
def delete_truck(truck_id):
#checking if there is a carrier logged in
  if 'carrier_id' not in session:
    flash('You must be signed-in as a carrier inorder to do this.')
    if 'broker_id' in session:
      return redirect('/broker/dashboard')
    elif 'shipper_id' in session:
      return redirect('/shipper/dashboard')
    else:
      return redirect('/')

#getting the carriers id and trucks' corresponding carrier id
  cid = Carrier.get_by_id({'carrier_id':session['carrier_id']})
  tid = Truck.get_by_id({'truck_id':truck_id})

#if truck does not exist it returns false, this handles that
  if tid == False:
    flash('The truck you tried to delete does not exist.')
    return redirect('/carrier/dashboard')
#comparing the carrier id in session to the trucks' carrier id
  elif cid.carrier_id != tid.carrier_id:
    flash('You did not post the truck that you are trying to delete.')
  else:
    Truck.delete({'truck_id':truck_id})
  
  data = {
    'user_id' : session['user_id'],
    'address_id' : session['address_id'],
    'carrier_id' : session['carrier_id'],
    'truck_id' : session['truck_id']
  }
  my_trucks = (Truck.get_my_trucks_list(data))

  if len(my_trucks.tractors) >=1:
    session['truck_id'] = my_trucks.truck_id
  else:
    session['truck_id'] = 0
  
  return redirect('/carrier/dashboard')

@app.route('/carrier/<int:truck_id>/edit')
def edit_truck(truck_id):
  if 'carrier_id' not in session:
    flash('You must be signed-in as a carrier inorder to do this.')
    if 'broker_id' in session:
      return redirect('/broker/dashboard')
    elif 'shipper_id' in session:
      return redirect('/shipper/dashboard')
    else:
      return redirect('/')
    
  cid = Carrier.get_by_id({'carrier_id':session['carrier_id']})
  tid = Truck.get_by_id({'truck_id':truck_id})

#if truck does not exist it returns false, this handles that
  if tid == False:
    flash('The truck you tried to edit does not exist.')
    return redirect('/carrier/dashboard')
#comparing the carrier id in session to the trucks' carrier id
  elif cid.carrier_id != tid.carrier_id:
    flash('You did not post the truck that you are trying to edit.')

  return render_template('/carrier_edit_truck.html',
    truck=tid,
    carrier=cid,
    cap=cap,
    date_hrs_subtraction=date_hrs_subtraction,
    convert_from_tuple=convert_from_tuple,
    states=states,
  )

@app.route('/carrier/<int:truck_id>/update', methods=['POST'])
def update_truck(truck_id):
  if 'carrier_id' not in session:
    flash('You must be signed-in as a carrier inorder to do this.')
    if 'broker_id' in session:
      return redirect('/broker/dashboard')
    elif 'shipper_id' in session:
      return redirect('/shipper/dashboard')
    else:
      return redirect('/')
    
  cid = Carrier.get_by_id({'carrier_id':session['carrier_id']})
  tid = Truck.get_by_id({'truck_id':truck_id})
  
#if truck does not exist it returns false, this handles that
  if tid == False:
    flash('The truck you tried to edit does not exist.')
    return redirect('/carrier/dashboard')
#comparing the carrier id in session to the trucks' carrier id
  elif cid.carrier_id != tid.carrier_id:
    flash('You did not post the truck that you are trying to edit.')

  data = {
    **request.form,
    'truck_id' : truck_id
  }

  if not Truck.truck_validator(data):
    flash('Something went wrong')
    return redirect(f'/carrier/{truck_id}/edit')
  else:
    Truck.update(data)
  
  return redirect('/carrier/dashboard')
