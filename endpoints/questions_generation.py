from fastapi import APIRouter
from models.models import questions_generator
from app.utils import generate_dynamic_questions
from database.database import session_questions

gpt_questions_generating_router=APIRouter(prefix="/questions_generator",tags=["pitch"],responses={404:{'description':'user data is not passed'}})


@gpt_questions_generating_router.post("/questions",response_model=questions_generator)
async def generate_questions():
    response_text = await generate_dynamic_questions()
    await session_questions(response_text)
    return questions_generator(response_text=response_text)
