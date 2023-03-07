import json
from flask import Flask,session
from flask_app.models.truck_model import Truck
from flask_app.models.carrier_model import Carrier
import datetime

class TruckEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, Carrier):
            return {
                'carrier_id':obj.carrier_id,
                'company_name':obj.company_name,
                'company_phone':obj.company_phone,
                'us_dot':obj.us_dot,
                'mc_number':obj.mc_number,
                'created_at':obj.created_at,
                'updated_at':obj.updated_at,
                'user_id':obj.user_id,
            }
        elif isinstance(obj, Truck):
            return {
                'truck_id': obj.truck_id, 
                'truck_number': obj.truck_number, 
                'origin_city': obj.origin_city, 
                'origin_state': obj.origin_state, 
                'origin_radius': obj.origin_radius,
                'destination_city': obj.destination_city,
                'destination_state': obj.destination_state,
                'destination_radius':obj.destination_radius,
                'equipment_type':obj.equipment_type,
                'weight':obj.weight,
                'length':obj.length,
                'rate_per_mile':obj.rate_per_mile,
                'created_at':obj.created_at,
                'updated_at':obj.updated_at,
                'carrier_id':obj.carrier_id,
                'postee':obj.postee
            }
        return json.JSONEncoder.default(self, obj)