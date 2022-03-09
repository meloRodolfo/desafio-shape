from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract, and_
from flask import request

from apis.models.equipment import equipment
from apis.models.vessel import vessel
from apis.models.model import db

import re

equipments_blueprint = Blueprint('equipments', __name__)

@equipments_blueprint.route('/insert_equipment', methods=['POST'])
def insert_equipment():
  
    body = request.get_json()
    e = equipment(code=body["code"], name=body["name"], location=body["location"], active=True)
    vessel_code = body["vessel_code"]
    
    if(check_parameters(e, vessel_code)):
      if(check_vessel_code_pattern(vessel_code)):
        ve = check_exists_vessel(vessel_code)
        if(ve):
          if(check_equipment_code(e.code)):
            if(check_parameters_format):
                if(check_equipament_exists(e.code)):
                  return {'message':'REPEATED_CODE'}, 409
                
                else:
                  e.vessel_id = ve.id
                  db.session.add(e)
                  db.session.commit()
                  return {'message':'OK'}, 201
              
            else:
              return {'message':'WRONG_FORMAT'}, 400
      
          else:
            return {'message':'WRONG_FORMAT'}, 400
          
        else:
          {'message':'NO_VESSEL'}, 409
      
      else:
        return {'message':'WRONG_FORMAT'}, 400
      
    else:
      return {'message':'MISSING_PARAMETER'}, 400

@equipments_blueprint.route('/update_equipment_status', methods=['PUT'])
def update_equipment_status():

    body = request.get_json()
    code = body["code"]
    
    if(code):
      if(check_equipment_code(code)):
        if(check_equipament_exists(code)):
          e = equipment.query.filter_by(code=code).first()
          e.active = False
          db.session.add(e)
          db.session.commit()
          
          return {'message':'OK'}, 201
        
        else:
          return {'message':'NO_CODE'}, 409
      
      else:
        return {'message':'WRONG_FORMAT'}, 400
      
    else:
      return {'message':'MISSING_PARAMETER'}, 400

@equipments_blueprint.route('/active_equipments', methods=['GET'])
def active_equipment():
  
    body = request.get_json()
    vessel_code = body["code"]
  
    if(vessel_code):
      if(check_vessel_code_pattern(vessel_code)):
        v = check_exists_vessel(vessel_code)
        if(v):
          equipments = equipment.query.filter_by(vessel_id=v.id, active=True).all()
          names = []
          for obj in equipments:
            names.append(obj.name)
            
          return jsonify(message='OK', status=200, equipments=names)
         
        else:
          return  {'message':'NO_VESSEL'}, 409
        
      else:
        return  {'message':'WRONG_FORMAT'}, 400
      
    else:
      return {'message':'MISSING_PARAMETER'}, 400

@equipments_blueprint.route('/all_equipments', methods=['GET'])
def all_equipments():
    equipments = equipment.query.all()
    equipments_list = []
    
    for obj in equipments:
      v = vessel.query.filter_by(id=obj.vessel_id).first()
      pair = ["", ""]
      pair[0] = "Equipment name: " + obj.name
      pair[1] = "Vessel code: " + v.code
      equipments_list.append(pair)
      
    return jsonify(message='OK', status=200, equipments_list=equipments_list)
  
def list_to_json(e):
  
  return {"id": e.id, "vessel_id": e.vessel_id, "name": e.name, "code": e.code, "location": e.location, e.active:"active"}

def check_parameters(eq, vessel_code):
    if(vessel_code and eq.code and eq.name and eq.location):
      return True
    else:
      return False
    
def check_vessel_code_pattern(id):
    v_resultado = re.match("[M][V]+[0-9]", id)
    return bool(v_resultado)

def check_exists_vessel(id):
    return vessel.query.filter_by(code=id).first()
  
def check_equipment_code(code):
    e_resultado = re.match("[0-9][0-9][0-9][0-9]+", code)
    return bool(e_resultado)
  
def check_parameters_format(e):
    return type(e.location) == str and type(e.name) == str
  
def check_equipament_exists(code):
  e = equipment.query.filter_by(code=code).first()
  if(e): 
    return True
  
  return False
      