from fastapi import FastAPI
from fastapi import APIRouter
from endpoints.type_of_pitch import gpt_type_of_intro_router
from endpoints.questions_generation import gpt_questions_generating_router
from endpoints.user import user_router



router = APIRouter()
router.include_router(user_router)
router.include_router(gpt_type_of_intro_router)
router.include_router(gpt_questions_generating_router)