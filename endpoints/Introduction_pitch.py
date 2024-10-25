from fastapi import APIRouter,Query
from app.utils import generate_dynamic_questions
from models.models import select_tone
from database.database import get_session_data_by_id

introduction_pitch_router=APIRouter(prefix="/introdduction_generator",tags=["pitch"],responses={404:{'description':'user data is not passed'}})

@introduction_pitch_router.post("/questions",response_model=str)

async def generate_introduction(answer1:str,answer2:str,answer3:str,answer4:str,answer5:str,answer6:str,tone:select_tone=Query()):
    