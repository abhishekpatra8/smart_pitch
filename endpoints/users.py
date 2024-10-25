from fastapi import Depends, APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import math, random
from db.database import add_user, fetch_user, get_user

router = APIRouter(prefix="/smart_pitch", tags=["Users"], responses={404: {"description": "Not found"}})

@router.post("/users/signup", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def user_add(request: Request, from_docs: dict):
    data = await request.json() if from_docs.get("email") is None else from_docs
    try:
        record = await fetch_user(data['email'])
        if record is not None:
            return JSONResponse(status_code=409, content={"status_code": 409, "message": "success", "details": "User already exsists !!"})
        else:
            result = await add_user(data)
            if result:
                return JSONResponse(status_code=200, content={"status_code": 200, "message": "User Added Successfully"})
            else:
                return JSONResponse(status_code=500, content={"status_code": 500, "message": "Issue while adding user"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": 500, "message": f"Problem in endpoint {str(e)}"})


@router.post("/users/login", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def user_login(request: Request, from_docs: dict):
    data = await request.json() if from_docs.get("email") is None else from_docs
    try:
        record = await get_user(data, 1)
        if record is not None: 
            if record['password'] == data['password']:
                return JSONResponse(status_code=200, content={"status_code": 200, "message": "success", "userDetails": jsonable_encoder(record)})
            else:
                return JSONResponse(status_code=401, content={"status_code": 401, "message": "Worng Password !!"})
        else:
            return JSONResponse(status_code=404, content={"status_code": 404, "message": "User not found"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": 500, "message": f"Problem in endpoint {str(e)}"})


# @router.post('/users/me', responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
# async def get_current_user(authorization: str = Header(None)):
#     # data = await request.json() if from_docs.get("email") is None else from_docs
#     # result = decode_access_token(data['token'])
#     result = decode_access_token(authorization.split()[1])
#     record = await get_user({"userid": result['data'].split("|")[1]}, 2)
#     if result['status_code'] == 401:
#         return JSONResponse(status_code=401, content={"status_code": 401, "message": "Token has been expired"})
#     if record is not None:
#         return JSONResponse(status_code=200, content={"status_code": 200, "message": "success", "userDetails": jsonable_encoder(record)})


# @router.post("/users/logout", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
# async def password_set(request: Request, from_docs: dict):
#     data = await request.json() if from_docs.get("userid") is None else from_docs
#     try:
#         return JSONResponse(status_code=200, content={"status_code": 200, "message": "You have been logged out."})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={"status": 500, "message": f"Problem in endpoint {str(e)}"})