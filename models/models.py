from pydantic import BaseModel
from typing import List
from enum import Enum

class user_registration(BaseModel):
    email:str
    password:str

class user_response(BaseModel):
    response_text:str

#### models_for_input_module ################
class select_occasion(str,Enum):
    Industry_conference='Industry conference'
    Social_Gathering='Social Gathering' 
    Networking_Event='NetworkingEvent' 
    Professional_Conference='Professional Conference'
    Job_Interview='Job Interview'
    Casual_Meet_and_Greet='Casual Meet and Greet'
    Wedding_Reception='Wedding Reception' 
    Graduation_Ceremony='Graduation Ceremony'
    Team_Building_Event='Team Building Event' 
    Business_Meeting='Business Meeting' 
    Interview_Panel='Interview Panel'
    Community_Event='Community Event' 
    Family_Gathering='Family Gathering'
    Entrepreneurial_Pitch ='Entrepreneurial Pitch'
    Educational_Seminar='Educational Seminar'

class select_professional_category(str,Enum):
    Leadership="Leadership"
    Specialized="Specialized"
    Enterpreneurial="Entrepreneurial"
    Creative_and_social="Creative & Social"
    Academic_and_research="Academic & Research"
    Entry_level="Entry-Level"
    Sales_and_marketing="Sales & Marketing"

class select_profession(BaseModel):
    role:str

class intro_type_generator(BaseModel):
    response_text: str

##### model_for_questions_generator #######
class questions_generator(BaseModel):
    response_text:List[str]

##### model for tone selection ##########
class select_tone(str,Enum):
    Confident="Confident"
    Casual="Casual"
    Formal="Formal"
    Friendly="Friendly"

# class select_questions(BaseModel):
#     question1:str
#     question2:str
#     question3:str
#     question4:
