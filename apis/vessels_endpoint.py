from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract, and_
from flasgger .utils import swag_from

from apis.models.vessel import vessel
from apis.models.model import db
from flask import request

import re

vessels_blueprint = Blueprint('vessels', __name__)

@vessels_blueprint.route('/insert_vessel', methods=['POST'])
def insert_vessel():

    padrao = "[M][V]+[0-9]"
    body = request.get_json()
    v = vessel(code=body["code"])
    
    if(v.code):
      
      resultado = re.match(padrao, v.code)
      flag = bool(resultado)
      if(flag):
        if(v.query.filter_by(code=v.code).first()):
          return {'message':'FAIL'}, 409
      
        else:
          db.session.add(v)
          db.session.commit()
          return {'message':'OK'}, 201 
          
      else:
        return {'message':'WRONG_FORMAT'}, 400
      
    else:
      return {'message':'MISSING_PARAMETER'}, 400

@vessels_blueprint.route('/', methods=['GET'])
def list_vessels():
  lista = vessel.query.all()
  codes = []
  for obj in lista:
    codes.append(obj.code)
  
  return jsonify(message='OK', status=200, vessels=codes)