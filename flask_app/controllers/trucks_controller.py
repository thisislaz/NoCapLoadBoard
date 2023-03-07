from flask_app import app,cap,date_hrs_subtraction,phone_format,convert_from_tuple,states
from flask import render_template, redirect, request, session, flash
from flask_app.models.truck_model import Truck
from flask_app.models.truck_encoder import TruckEncoder
from datetime import datetime
import json

@app.route('/truck/<int:truck_id>')
def carrier_truck_view(truck_id):
  if 'user_id' not in session:
    flash("You must log in first.")
    return redirect('/login')

  truck = Truck.get_truck_by_id({'truck_id':truck_id})

  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")
  
  trucks = Truck.get_postees_other_trucks({'truck_id':truck_id})
  ts = trucks.list
  sts = sorted(ts, key=lambda t:t.created_at, reverse=True)


  return render_template("truck_details.html",
    truck=truck,
    trucks=sts,
    convert_from_tuple=convert_from_tuple,
    date_hrs_subtraction=date_hrs_subtraction, 
    now=now,
    cap=cap,
    phone_format=phone_format
  )



@app.route('/find_trucks')
def find_trucks():
  if 'user_id' not in session :
    flash("You must log in first.")
    return redirect('/login')
  elif 'carrier_id' in session:
    flash("You must log in as a shipper or broker.")
    return redirect('/login') 

    
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")

  try:
    strung_truck_list = session['searched_trucks_list']
    truck_dict = json.loads(strung_truck_list)
    std = sorted(truck_dict, key=lambda t:t['created_at'], reverse=True)

    return render_template('find_trucks.html',
      now=now,
      states=states,
      truck_dictionary=std,
      cap=cap,
      date_hrs_subtraction=date_hrs_subtraction,
      convert_from_tuple=convert_from_tuple
    )
  except:
    return render_template('find_trucks.html',
      now=now,
      states=states,
      cap=cap,
      date_hrs_subtraction=date_hrs_subtraction,
      convert_from_tuple=convert_from_tuple
    )

@app.route('/process_searched_trucks',methods=['POST'])
def process_searched_trucks():
  search = {
    **request.form
  }
  for k,v in search.items():
    if k == "origin_city":
      if v == "":
        continue
      else:
        trucks = Truck.get_trucks_by_origin_city(search)
  #if the input type is not a select/option tag
  #you must do this step, because the query will return false
  #if there are trucks with the origin that is entered
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string
    if k == "origin_state":
      if v == "":
        continue
      else:
        trucks = Truck.get_trucks_by_origin_state(search)
  #if the input type is not a select/option tag
  #you must do this step, because the query will return false
  #if there are trucks with the origin that is entered
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string
    elif k == "equipment_type":
      if v=="":
        continue
      else:
        trucks = Truck.get_trucks_by_equipment_type(search)
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string
    elif k == 'weight':
      if v == '':
        continue
      else:
        search['weight'] = int(search['weight'])
        trucks = Truck.get_trucks_by_weight(search)
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string
    elif k == 'rate_per_mile' :
      if v == '':
        continue
      else:
        search['rate_per_mile'] = float(search['rate_per_mile'])
        trucks = Truck.get_trucks_by_rate(search)
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string
    elif k == 'destination_city' :
      if v == '':
        continue
      else:
        trucks = Truck.get_trucks_by_destination_city(search)
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string
    elif k == 'destination_state' :
      if v == '':
        continue
      else:
        trucks = Truck.get_trucks_by_destination_state(search)
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string
    elif k == "all" :
      if v == "" :
        continue
      else:
        trucks = Truck.get_all_trucks_list(search)
        if trucks == False:
          session['searched_trucks_list'] = None
          print('query failed')
          continue
        else:
          trucks_as_string = json.dumps(trucks.list, cls=TruckEncoder)
        session['searched_trucks_list'] = trucks_as_string    

  return redirect('/find_trucks')