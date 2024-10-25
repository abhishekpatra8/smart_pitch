from fastapi import FastAPI,Query
from pydantic import BaseModel,Field
from openai import OpenAI
from enum import Enum
import pymysql
from fastapi.routing import APIRouter
from typing import Optional

new_graduate_pitch_router=APIRouter(prefix="/graduate_pitch",tags=["pitch"],responses={404:{'description':'user data is not passed'}})

server = 'localhost'
port = 3306
database = 'smart_pitch_db'
username = 'root'
password = 'Mit@08052023'

class classify_pitch(str,Enum):
    personal="personal"
    formal="formal"
    professional="professional"

class Industry_conference(BaseModel):
    current_role: Optional[str] = Field(None, description="What is your current role")
    area_of_expertise:Optional[str]=Field(None,description="area of expertise?")
    current_research:Optional[str] = Field(None, description="What are the focus areas of your current projects or research?")
    reason_for_attending: Optional[str] = Field(None, description="Why did you choose to attend this particular conference?")
    sessions_of_interest:Optional[str] = Field(None, description="What specific sessions or topics are you looking forward to?")
    application_of_learning: Optional[str] = Field(None, description="How do you hope to apply what you learn to your work or career?")

    
class Output(BaseModel):
    response_text:str

def connect_mysql():
    return pymysql.connect(
        host=server,
        port=port,
        database=database,
        user=username,
        password=password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_user_input_data(user_name,pitch_type,current_role,current_projects,reason_for_attending,application_of_learning,area_of_expertise,input_prompt, response_text):
    connection = connect_mysql()
    if connection:
        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO industry_conference 
                (full_name,profession,current_research,reason_for_attending,application_of_learning,pitch_type,gpt_prompt, gpt_response,area_of_expertise)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
                """
                cursor.execute(insert_query,(
                    user_name,
                    current_role,
                    current_projects,
                    reason_for_attending,
                    application_of_learning,
                    pitch_type,
                    input_prompt,
                    response_text,
                    area_of_expertise
                ))
            connection.commit()  
        except pymysql.MySQLError as e:
            print(f"Error while inserting data to MySQL: {e}")
        finally:
            connection.close()  
    else:
        print("Failed to connect to the database.")

def gpt_connection1(input_prompt):
    API_KEY = "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"
    ai_client = OpenAI(api_key=API_KEY)

    system_prompt = '''Generate a concise,four-line introduction pitch using the provided details. 
                        Ensure the response varies in tone, phrasing, and structure for each user w.r.t previous response, 
                        even if inputs are similar. Include the user's name naturally and 
                        maintain a professional, networking-appropriate tone.
                        '''
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_prompt}  # Specific user input
        ]
    )
    return response

def gpt_connection2(response,pitch: classify_pitch = Query()):
    pitch_type=pitch
    API_KEY = "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"
    ai_client = OpenAI(api_key=API_KEY)
    
    system_prompt = f'''Generate a concise,four-line {pitch_type} introduction pitch by re-tuning the given {response}.
                        Ensure the response varies in tone, phrasing, and structure should vary for various names w.r.t name given in the response. 
                        '''
    
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt}
        ]
    )
    return response

@new_graduate_pitch_router.post("/graudate_pitch",response_model=Output)

def Industry_conference(user_name: str,input:Industry_conference,pitch: classify_pitch = Query()):
    type_of_pitch=pitch   
    profession=input.current_role
    Area_of_interest=input.area_of_expertise
    Ongoing_projects=input.current_research
    Reason_for_attending=input.reason_for_attending
    Interesting_sessions=input.sessions_of_interest
    Application_of_learning=input.application_of_learning

    input_prompt= f'''Create a {type_of_pitch} pitch using:
                        Profession: {profession}
                        Area of expertise: {Area_of_interest}
                        Current research: {Ongoing_projects}
                        Reason for attending the conference: {Reason_for_attending}
                        What specific sessions or topics are you looking forward to? ans-{Interesting_sessions}
                        How do you hope to apply what you learn to your work or career? ans-{Application_of_learning}
    
                    Ensure it's four lines, includes {user_name}, and varies in structure across users even if inputs are similar.'''

    print(len(input_prompt.split()))

    response_text = gpt_connection1(input_prompt).choices[0].message.content
    final_text=gpt_connection2(response_text).choices[0].message.content
    # Insert input, prompt, and response data into MySQL
    insert_user_input_data(
        user_name=user_name,
        current_role=profession,
        current_projects=Ongoing_projects,
        reason_for_attending=Reason_for_attending,
        application_of_learning=Application_of_learning,
        pitch_type=type_of_pitch.value,
        area_of_expertise=Area_of_interest,
        input_prompt=input_prompt,
        response_text=final_text
    )

    return Output(response_text=final_text) 

