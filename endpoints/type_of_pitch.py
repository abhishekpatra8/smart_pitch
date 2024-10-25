from fastapi import Query
from fastapi.routing import APIRouter
from models.models import select_occasion,select_profession,select_professional_category,intro_type_generator
import uuid
from database.database import set_session_data
from app.utils import get_intro_type_of_pitch
from datetime import datetime
import pytz 

gpt_type_of_intro_router=APIRouter(prefix="/select_occasion",tags=["pitch"],responses={404:{'description':'user data is not passed'}})


@gpt_type_of_intro_router.post("/type_of_intro_pitch",response_model=intro_type_generator)

async def type_of_introduction_pitch_selection(user_name: str,profession: select_profession,occasion: select_occasion = Query(),professional_category: select_professional_category = Query()):
    type_of_intro_pitch = get_intro_type_of_pitch(occasion, profession, professional_category)

    session_id = str(uuid.uuid4())

    india_timezone = pytz.timezone('Asia/Kolkata')
    
    await set_session_data(session_id,{
        "User_name":user_name,
        "session_id":session_id,
        "profession": profession.role,
        "occasion": occasion,
        "professional_category": professional_category,
        "intro_type": type_of_intro_pitch.strip(),
        "created_at":datetime.now(india_timezone)
    })

    return {"response_text":type_of_intro_pitch.strip()}

