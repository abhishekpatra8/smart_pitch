from bson.objectid import ObjectId
import datetime

def add_user_helper(data) -> dict:
    return {"name": data['name'], "email": data['email'], "phone": data['phone'], "password": data['password']}

def fetch_user_helper(data) -> dict:
    return {"email": data}

def get_user_helper(data, flag) -> dict:
    if flag == 1:
        return {"email": data['email']}
    else:
        return {"_id": ObjectId(data['userid'])}