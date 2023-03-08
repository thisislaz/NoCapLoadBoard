from flask import Flask, flash
from flask_bcrypt import Bcrypt
from datetime import datetime
import re, requests, json, os
from dotenv import load_dotenv

def configure():
  load_dotenv()

app = Flask(__name__)
app.secret_key = "lookformeintheforest"
DATABASE = "loadboard"
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
states = ['ANY','AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

def cap(phrase):
  b = []
  for temp in phrase.split(" "): 
    b.append(temp.capitalize())
  return " ".join(b)

def convert_from_tuple(a):
  b = a.strftime('%Y-%m-%d %H:%M:%S')
  return b

def date_hrs_subtraction(a,b):
  convert_a = str(a)
  convert_b = str(b)

  dt1 = datetime.strptime(convert_a, "%Y-%m-%d %H:%M:%S")
  dt2 = datetime.strptime(convert_b, "%Y-%m-%d %H:%M:%S")

  sub = dt2 - dt1
  days= sub.days
  hrs=sub.seconds//3600
  mins=(sub.seconds//60)%60

  posted= f'{hrs} hrs {mins} mins'
  if days == 0 and hrs == 0 and mins >=11:
    posted = f'{mins}m'
    return posted
  if days == 0 and hrs == 0 and mins <= 10:
    posted = "Now"
    return posted
  if days == 0 and hrs >= 1:
    posted = f'{hrs}h'
    return posted
  if days >= 1:
    d_ago = f"{days}d"
    return d_ago

def phone_format(phone_number):
    clean_phone_number = re.sub('[^0-9]+', '', phone_number)
    formatted_phone_number = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone_number[:-1])) + clean_phone_number[-1]
    return formatted_phone_number

def remove_white_space(string):
  pattern = re.compile(r'\s+')
  r = re.sub(pattern,' ',string)
  result = "".join(r.rstrip())
  return result

# if carrier does not exist it returns None
def get_carrier(carrier_data):
  configure()
  dot_number = carrier_data

  res_dot = requests.get(f'https://mobile.fmcsa.dot.gov/qc/services/carriers/{dot_number}?webKey={os.getenv("API_KEY_SERVICE")}')
  packages_json = res_dot.json()
  carrier = packages_json['content']

  mc_res = requests.get(f'https://mobile.fmcsa.dot.gov/qc/services/carriers/{dot_number}/docket-numbers?webKey={os.getenv("API_KEY_SERVICE")}')
  mc_package = mc_res.json()
  mc = mc_package['content']

  try:
    cs = json.dumps(carrier['carrier'], indent=2)
    cd = json.loads(cs)

    company_name = cd['legalName']
    address_line_one = remove_white_space(cd['phyStreet'])
    state = cd['phyState']
    city = cd['phyCity']
    postal_code = cd['phyZipcode']
    us_dot = cd['dotNumber']
    
    try:
      mc_number = mc[0]['docketNumber']
      carrier_class = {
        'company_name':company_name,
        'address_line_one':address_line_one,
        'state':state,
        'city': city,
        'postal_code':postal_code,
        'us_dot':us_dot,
        'mc_number':mc_number,
      }
    except:
      carrier_class = {
        'company_name':company_name,
        'address_line_one':address_line_one,
        'state':state,
        'city': city,
        'postal_code':postal_code,
        'us_dot':us_dot,
      }
    return carrier_class
  
  except:
    pass

#if broker does not exist it returns None
def get_broker(carrier_data):
  configure()

  dot_number = carrier_data

  res_dot = requests.get(f'https://mobile.fmcsa.dot.gov/qc/services/carriers/{dot_number}?webKey={os.getenv("API_KEY_SERVICE")}')
  packages_json = res_dot.json()
  carrier = packages_json['content']

  mc_res = requests.get(f'https://mobile.fmcsa.dot.gov/qc/services/carriers/{dot_number}/docket-numbers?webKey={os.getenv("API_KEY_SERVICE")}')
  mc_package = mc_res.json()
  mc = mc_package['content']

  try:
    cs = json.dumps(carrier['carrier'], indent=2)
    cd = json.loads(cs)

    company_name = cd['legalName']
    address_line_one = remove_white_space(cd['phyStreet'])
    state = cd['phyState']
    city = cd['phyCity']
    postal_code = cd['phyZipcode']
    us_dot = cd['dotNumber']
    
    try:
      mc_number = mc[0:][:]
      if mc_number[0]['prefix']=="MC":
        print('mc number')
        carrier_class = {
          'company_name':company_name,
          'address_line_one':address_line_one,
          'state':state,
          'city': city,
          'postal_code':postal_code,
          'us_dot':us_dot,
          'mc_number':mc_number[0]['docketNumber'],
        }
      elif mc[0]['prefix']=="FF":
        print('ff number')
        carrier_class = {
          'company_name':company_name,
          'address_line_one':address_line_one,
          'state':state,
          'city': city,
          'postal_code':postal_code,
          'us_dot':us_dot,
          'mc_number':mc_number[0]['docketNumber'],
        }
    except:
      carrier_class = {
        'company_name':company_name,
        'address_line_one':address_line_one,
        'state':state,
        'city': city,
        'postal_code':postal_code,
        'us_dot':us_dot,
      }
    return carrier_class
  
  except:
    pass