import json
from flask_app.models.load_model import Load
from datetime import datetime, date


class LoadEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
      return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, Load):
      return {
        'load_id': obj.load_id, 
        'load_number': obj.load_number, 
        'origin_city': obj.origin_city, 
        'origin_state': obj.origin_state, 
        'destination_city': obj.destination_city,
        'destination_state': obj.destination_state,
        'pickup_date':obj.pickup_date.strftime("%m/%d/%y"),
        'delivery_date':obj.delivery_date.strftime("%m/%d/%y"),
        'equipment_type':obj.equipment_type,
        'rate_per_mile':obj.rate_per_mile,
        'weight':obj.weight,
        'size':obj.size,
        'length':obj.length,
        'created_at':obj.created_at,
        'updated_at':obj.updated_at,
      }
    return json.JSONEncoder.default(self,obj)