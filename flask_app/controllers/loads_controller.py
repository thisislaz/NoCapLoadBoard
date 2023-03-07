from flask_app import app,cap,date_hrs_subtraction,phone_format,convert_from_tuple,states
from flask import render_template, redirect, request, session,flash
from flask_app.models.load_model import Load
from flask_app.models.load_encoder import LoadEncoder

from datetime import datetime
import json

@app.route('/load/<int:load_id>')
def get_load(load_id):
  if 'user_id' not in session:
    flash("You must log in first.")
    return redirect('/login')
  load = Load.get_load_by_id({'load_id':load_id})
  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")

  print(session)
  try:
    loads = Load.get_postees_other_loads({'user_id':Load.get_load_by_id({'load_id':load_id}).user.user_id})
    ls = loads
    sls = sorted(ls.list, key=lambda l:l.created_at, reverse=True)
      
      # for l in sls:
      #   print("------- load.user.user_id",load.user.user_id)
      #   print("------- l.user.user_id",l.user.user_id)
      #   print("------- l.origin_city",l.origin_city)
    return render_template('load_details.html',
        load=load,
        loads=sls,
        now=now,
        date_hrs_subtraction=date_hrs_subtraction,
        cap=cap,
        convert_from_tuple=convert_from_tuple,
        phone_format=phone_format
      )
  
  except:
    print(session)
    return render_template('load_details.html',
      load=load,
      now=now,
      date_hrs_subtraction=date_hrs_subtraction,
      cap=cap,
      convert_from_tuple=convert_from_tuple,
      phone_format=phone_format
    )

@app.route('/find_loads')
def find_loads():
  if 'user_id' not in session:
    flash("You must log in first.")
    return redirect('/login')
  elif 'shipper_id' in session:
    flash('Currently, shippers cannot search for other loads.')
    return redirect('/')

  ndt = datetime.now()
  now = ndt.strftime("%Y-%m-%d %H:%M:%S")
  try:
      #stringfied load list
    sll = session['string_load_list']
      #load dictionary
    ld = json.loads(sll)
      #sorted list of loads by created time, then reversed to show newst first
    sorted_sll = sorted(ld, key=lambda l:l['created_at'], reverse=True)
    print(ld)
    return render_template('find_loads.html',
    now=now,
    states=states,
    load_dictionary=sorted_sll,
    cap=cap,
    date_hrs_subtraction=date_hrs_subtraction,
    convert_from_tuple=convert_from_tuple
  )
  except:
    return render_template('find_loads.html',
      now=now,
      states=states,
      cap=cap,
      date_hrs_subtraction=date_hrs_subtraction,
      convert_from_tuple=convert_from_tuple
    )
  
@app.route('/process_searched_loads', methods=['POST'])
def process_searched_loads():
  search = {
    **request.form
  }
  print(search)
  for k,v in search.items():
    if k == "all":
      if v== "":
        continue
      else:
        loads = Load.get_all_loads_list_no_limit(search)
        if loads == False:
          session['string_load_list'] = None
          print('the query returned false')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string
    elif k == "origin_city" :
      if v == "":
        continue
      else:
        loads = Load.get_loads_by_origin_city(search)
        if loads == False:
          session['string_load_list'] = None
          print('query failed')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string
    elif k == "origin_state" :
      if v == "":
        continue
      else:
        loads = Load.get_loads_by_origin_state(search)
        if loads == False:
          session['string_load_list'] = None
          print('query failed')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string
    elif k == "destination_city":
      if v == "":
        continue
      else:
        loads = Load.get_loads_by_destination_city(search)
        if loads == False:
          session['string_load_list'] = None
          print('query failed')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string
    elif k == "destination_state":
      if v == "":
        continue
      else:
        loads = Load.get_loads_by_destination_state(search)
        if loads == False:
          session['string_load_list'] = None
          print('query failed')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string
    elif k == 'rate_per_mile' :
      if v == '':
        continue
      else:
        search['rate_per_mile'] = float(search['rate_per_mile'])
        loads = Load.get_loads_by_rate(search)
        if loads == False:
          session['string_load_list'] = None
          print('query failed')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string
    elif k == "equipment_type":
      if v == "":
        continue
      else:
        loads = Load.get_loads_by_equipment_type(search)
        if loads == False:
          session['string_load_list'] = None
          print('query failed')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string
    elif k == "size":
      if v == "":
        continue
      else:
        loads = Load.get_loads_by_size(search)
        if loads == False:
          session['string_load_list'] = None
          print('query failed')
          continue
        else:
          loads_as_string = json.dumps(loads.list, cls=LoadEncoder)
        session['string_load_list'] = loads_as_string

  return redirect('/find_loads')