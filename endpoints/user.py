from fastapi.routing import APIRouter
from database.database import user_signup
from models.models import user_registration,user_response

user_router=APIRouter(prefix="/registration",tags=["smart_pitch"],responses={404:{'description':'user data is not passed'}})

@user_router.post("/signup",response_model=user_response)

async def registration(input:user_registration):
    email=input.email
    password=input.password
    userdata=await user_signup(email,password)
    return user_response(response_text=userdata)
