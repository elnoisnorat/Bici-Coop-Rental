from flask import request, jsonify
import jwt
from functools import wraps
from config.encryption import SECRET_KEY, ENC_ALG
from dao.bicycle import BicycleDAO


def isWorker(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json['token']
        print(token)
        if not token:
            return jsonify(Error='Token is missing'), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            if data['Role'] != 'Worker':
                return jsonify(Error='Not a worker'), 403
        except:
            return jsonify(Error='Not a worker'), 403
        return f(*args, **kwargs)
    return decorated

def isAdmin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json['token']
        if not token:
            return jsonify(Error='Token is missing'), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            if data['Role'] != 'Admin':
                return jsonify(Error='Not a admin'), 403
        except:
            return jsonify(Error='Not a admin'), 403
        return f(*args, **kwargs)
    return decorated

def isClient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json['token']
        if not token:
            return jsonify(Error='Token is missing'), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            if data['Role'] != 'Client':
                return jsonify(Error='Not a client'), 403
        except:
            return jsonify(Error='Not a client'), 403
        return f(*args, **kwargs)
    return decorated

def isWorkerOrAdmin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json['token']
        print(token)
        if not token:
            return jsonify(Error='Token is missing'), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            if data['Role'] != 'Worker' or data['Role'] != 'Admin':
                return jsonify(Error='Not a worker or admin'), 403

        except:
            return jsonify(Error='Invalid token.'), 403
        return f(*args, **kwargs)
    return decorated

def hasRole(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json['token']
        print(token)
        if not token:
            return jsonify(Error='Token is missing'), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            if data['Role'] != 'Worker' or data['Role'] != 'Admin' or data['Role'] != 'Client':
                return jsonify(Error='Token does not have a valid role.'), 403
        except:
            return jsonify(Error='Invalid token.'), 403
        return f(*args, **kwargs)
    return decorated

def isDecomissioned(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bDAO = BicycleDAO()
        bStatus = bDAO.getStatusByID(request.json['bid'])
        print(bStatus)
        if bStatus == 'Decomissioned':
            return jsonify(Error="This bicycle is decomissioned")
        return f(*args, **kwargs)
    return decorated