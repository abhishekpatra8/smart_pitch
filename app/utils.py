import re
from openai import OpenAI
from models.models import select_occasion,select_profession,select_professional_category,select_tone
from database.database import get_last_session_id,get_session_data_by_id
from fastapi import HTTPException,Query
from config import settings


def remove_numbers(text: str):
    return re.sub(r'[^a-zA-Z\s]', '', text)

def get_intro_type_of_pitch(occasion: select_occasion, profession: select_profession, professional_category: select_professional_category):
    api_key=settings.OPENAI_API_KEY
    ai_client = OpenAI(api_key=api_key)
    identifying_type_of_introduction_prompt = f'''Based on the user-selected occasion "{occasion}", provide only the 
    type of introduction pitch that matches the occasion.
        Choose from the following three types:
        1) Formal Introduction Pitch
        2) Personal Introduction Pitch
        3) Professional Introduction Pitch
        Do not list multiple options, just return the best match for the given occasion.
    '''              
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": identifying_type_of_introduction_prompt}]
    )
    type_of_introduction_pitch = remove_numbers(response.choices[0].message.content.strip())

    return type_of_introduction_pitch

async def generate_dynamic_questions():
    api_key=settings.OPENAI_API_KEY
    ai_client = OpenAI(api_key=api_key)

    last_session_id =await get_last_session_id()

    if not last_session_id:
        raise HTTPException(status_code=404, detail="No session_id found in Database")
    
    session_data=await get_session_data_by_id(last_session_id)

    if session_data is None:
        return {"message": f"No data found for session ID: {last_session_id}"}
    
    profession = session_data["profession"]
    occasion = session_data["occasion"]
    professional_category = session_data["professional_category"]
    intro_type = session_data["intro_type"]

    parameters_from_occasion_and_role_prompt = f'''
        Based on the occasion "{occasion}","{professional_category}" and the role "{profession}", generate concise important and relevant questions where the question numbers
          should be less than or equal 6,that will help to collect the necessary personal data for creating an {intro_type}.
        
        The questions should be tailored to the occasion and role, with examples like and this format  :
        If the occasion is "Wedding Reception" and the role is "Housewife":
            1) Name
            2) Hometown
            3) Connection to the Wedding Couple
            4) Hobbies
        If the occasion is "Industry Conference" and the role is "CEO":
            1) Name
            2) Years of Experience
            3) Company Focus/Industry
            4) Key Accomplishments / Projects
            5) Relevant Topics of Interest at the Conference
        If the occasion is "Fun Event/Pub" and the role is "Working Professional":
            1) Name
            2) Reason for Being There
            3) Hobbies or Interests
            4) Interest in the Environment
            5) Playful Engagement
        If the occasion is "Job Interview" and the role is "Junior ML Engineer":
            1) Name
            2) Current Role
            3) Years of Experience
            4) Educational Background
            5) Skills
            6) Career Goals
        If the occasion is "Job Interview" and the role is "Graduate Without Experience":
            1) Name
            2) Place of Birth
            3) Educational Background
            4) Relevant Skills
            5) Academic Projects
            6) Internships
            7) Hobbies
            8) Goals
        If the occasion is "Job Interview" and the role is "working professional in any field":
            1) Name
            2) Years of experience
            3) Company name
            4) Key Skills
            5) Industry expertise
            6) Notable Acheivements
        if the occasion is "Business Meeting" and the role is "Business development executive":
            1) Name
            2) Current Company
            3) Roles and responsibilites
            4) Reason for attending this Business Meeting
    
        if the occasion is "Business Meeting" and the role is "CTO":
            1) Name:
            2) Current Company:
            3) Roles and responsibilites:
            4) Reason for attending this Business Meeting:
        
 
        Generate the relevant questions according to the occasion "{occasion}" and the role "{profession}" that a normal person could ask
        for to introduce oneself.Do not include any explanations, commentary, or introductory text—only provide the questions.
    '''
    messages=[
         {'role':"system",'content':'''You are an Introduction pitch generator and your task is to generate appropriate questions
           as per the event'''},
 
        {"role":"user", "content":parameters_from_occasion_and_role_prompt}
 
        ]

    try:
        response = ai_client.chat.completions.create(model="gpt-4o-mini", messages=messages)

        questions = response.choices[0].message.content.strip().split("\n")

        cleaned_questions=[remove_numbers(x) for x in questions]
        stripped_questions=[x.strip() for x in cleaned_questions]

        return stripped_questions
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": "Failed to generate questions. Please check the logs for details."}

# async def generate_intro():
#     questions=await generate_dynamic_questions()

def generate_introduction_pitch():
    session_data=get_session_data_by_id()
    intro_type=session_data['intro_type']
    occasion=session_data['occasion']
    profession=session_data['profession']
    professional_category=session_data['professional_category']
    questions=session_data['questions']

    intro_pitch_prompt = f'''Create an introduction pitch based on the following details:
    Occasion: {occasion}
    Role: {profession}
    questions:{questions}
    Answers: {answers}
    Introduction Type: {intro_type}
    Tone: {tone}

    Please provide a concise and personalized 5 lines of introduction pitch as per the answers that are relevant to Occasion 
    along with Tone.And consier the default second person as a singular noun .'''

    # messages = [{"role": "user", "content": intro_pitch_prompt}]
    # response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content.strip()
