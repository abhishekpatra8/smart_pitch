import pymongo
from bson.objectid import ObjectId
import motor.motor_asyncio
from config import settings

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB)
db = mongo_client["Smart_Pitch"]
session_collection = db["users"]
# session_collection2=db["Questions"]
# session_collection3=db["Ans"]


async def user_signup(email:str,password:str):
    signup={"emailid":email,"password":password}
    db.session_collection.insert_one(signup)
    return "Successfully registered"

async def set_session_data(session_id:str,session_data:dict):
    await session_collection.update_many({'session_id':session_id},{'$set': session_data},upsert=True)

async def get_last_session_id():
    last_session = await session_collection.find_one({},sort=[('created_at', -1)])
    print(last_session)
    if last_session:
        if 'session_id' in last_session:
            return last_session['session_id']
        else:
            print(f"'session_id' is not found in last_session: {last_session}")
            return None

async def get_session_data_by_id(session_id: str):
    session_data = await session_collection.find_one({"session_id": session_id})
    if session_data:
        return session_data
    else:
        return "There is no session data"
    
async def session_questions(questions:list[str]):
    last_session = await session_collection.find_one({},sort=[('created_at', -1)])
    await session_collection.update_one(
            {'session_id': last_session['session_id']},
            {'$set': {'questions': questions}}           
        )
            
# async def get_session_questions():
#     last_session = await session_collection.find_one({},sort=[('created_at', -1)])
#     if last_session and 'session_id' in last_session:
#         session_id = last_session['session_id']
#         session_with_questions = await session_collection.find_one({"session_id": session_id}, {"questions": 1})
#     if session_with_questions and 'questions' in session_with_questions:
#         questions=session_with_questions['questions']
#         return questions

    
async def type_of_tone(tone:str):
    last_session = await session_collection.find_one({},sort=[('created_at', -1)])
    await session_collection.update_one({'session_id': last_session['session_id']},{'$set':{'tone_type':tone}})

