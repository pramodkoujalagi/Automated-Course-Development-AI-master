import os
import json
import openai
from dotenv import load_dotenv
from all_prompts_stream import TABLER_SYSTEM_PROMPT, DICTATOR_PROMPT, USER_SAYS_SYSTEM_PROMPT, MAKEMODS_SYSTEM_PROMPT, get_prompt
from generator_functions_stream import make_course_content
# from generator_functions_stream_new_approach import make_course_content
import streamlit as st

# Loading the API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#Defining a singular function to call the API
def load_api(messages):

  response = openai.ChatCompletion.create(
    model="gpt-4o",
    temperature=0.3,  # Low temperature for less randomness
    top_p=0.8,  # Moderate top-p for some diversity
    messages=messages)

  response_content = response.choices[0].message.content
  
  return response_content

#Function to generate course outline based on user inputs
def get_course_outline(course_name, target_audience_edu_level, difficulty_level, num_modules, course_duration, course_credit):
  
  PROMPTER_PROMPT = get_prompt(course_name, target_audience_edu_level, difficulty_level, num_modules, course_duration, course_credit)

  # Create the messages list with the system prompt - Prompter
  prompter_messages = [{"role": "system", "content": PROMPTER_PROMPT}]

  # Loading the API and saving the content of the above obtained response as tabler's user prompt 
  tabler_user_prompt = load_api(prompter_messages) 

  # Creating the messages list with the system prompt - Tabler 
  tabler_messages = [{"role": "system", "content": TABLER_SYSTEM_PROMPT}]

  # Adding the generated user prompt to the messages list
  tabler_messages.append({"role": "user", "content": tabler_user_prompt})

  course_overview = load_api(tabler_messages)

  return course_overview

#Function to make modifications to an existing course outline
def modify_course_outline(course_overview, user_feedback):

  with st.spinner("Modifying the course outline based on your feedback..."):
  
    original_and_feedback = f"""Original Content:\n {course_overview} \n\nUser Feedback: {user_feedback}"""

    # Creating the messages list with the system prompt - UserSays 
    mods_messages = [{"role": "system", "content": MAKEMODS_SYSTEM_PROMPT}]
    mods_messages.append({"role": "user", "content": original_and_feedback})

    modified_outline = load_api(mods_messages)

    return modified_outline

#Function to generate the full course content
def gen_full_course(course_name, course_overview):

  # Creating the messages list with the system prompt - DICTator 
  dictator_messages = [{"role": "system", "content": DICTATOR_PROMPT}]

  # Adding the course outline to the messages list as a user
  dictator_messages.append({"role": "user", "content": course_overview})

  # Loading the API and saving the response
  dictator_response = load_api(dictator_messages)

  # Converting this response to a dictionary
  module_lesson_dict = json.loads(dictator_response)

  #Calling the Course Generator function
  make_course_content(course_name, module_lesson_dict)

  # Set a flag in the session state to indicate that the course content has been generated
  st.session_state["course_content_generated"] = True

  return
