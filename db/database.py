from bson.objectid import ObjectId
import motor.motor_asyncio
from config import settings
from db.db_helper import (
                            add_user_helper, fetch_user_helper, get_user_helper,
                            # get_all_docs_as_per_user_id, get_all_rfp_types_and_due_dates, get_all_rfp_filter, add_rfp_helper, add_rfp_remarks, add_rfp_comments, update_rfp_helper, add_doc_details_helper,
                            # get_all_prompts_helper, update_prompt_helper, insert_prompt_helper, delete_prompt_helper, get_specific_content_helper
                        )

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB)

database = mongo_client["Smart_Pitch"]

# Fetch OpemAI AIP Key
async def key_api() -> str:
    result = await database.openai_api_key.find_one({"_id": ObjectId('671bdef163fb8e6133c7c28d')}, {"_id": 0})
    return result['key']

# Users Section
async def add_user(data) -> bool:
    await database.users.insert_one(add_user_helper(data))
    return True

async def fetch_user(data) -> bool:
    result = await database.users.find_one(fetch_user_helper(data))
    return result

async def get_user(data, flag) -> list:
    result = None
    try:
        result = await database.users.find_one(get_user_helper(data, flag))
        result['id'] = str(result['_id'])
        del result['_id']
    except: pass
    return result






















# async def set_session_data(session_id:str,session_data:dict):
#     await session_collection.update_many({'session_id':session_id},{'$set': session_data},upsert=True)

# async def get_last_session_id():
#     last_session = await session_collection.find_one({},sort=[('created_at', -1)])
#     print(last_session)
#     if last_session:
#         if 'session_id' in last_session:
#             return last_session['session_id']
#         else:
#             print(f"'session_id' is not found in last_session: {last_session}")
#             return None

# async def get_session_data_by_id(session_id: str):
#     session_data = await session_collection.find_one({"session_id": session_id})
#     if session_data:
#         return session_data
#     else:
#         return "There is no session data"
    
# async def session_questions(questions:list[str]):
#     last_session = await session_collection.find_one({},sort=[('created_at', -1)])
#     await session_collection.update_one(
#             {'session_id': last_session['session_id']},
#             {'$set': {'questions': questions}}           
#         )
            
# # async def get_session_questions():
# #     last_session = await session_collection.find_one({},sort=[('created_at', -1)])
# #     if last_session and 'session_id' in last_session:
# #         session_id = last_session['session_id']
# #         session_with_questions = await session_collection.find_one({"session_id": session_id}, {"questions": 1})
# #     if session_with_questions and 'questions' in session_with_questions:
# #         questions=session_with_questions['questions']
# #         return questions

    
# async def type_of_tone(tone:str):
#     last_session = await session_collection.find_one({},sort=[('created_at', -1)])
#     await session_collection.update_one({'session_id': last_session['session_id']},{'$set':{'tone_type':tone}})

