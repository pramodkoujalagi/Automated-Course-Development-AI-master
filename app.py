<<<<<<< HEAD
import streamlit as st
import shelve
from acd_stream import get_course_outline, modify_course_outline, gen_full_course
=======
from openai import OpenAI, OpenAIError
import streamlit as st
from dotenv import load_dotenv
import os
import json
import shelve
import unicodedata
from fpdf import FPDF # type: ignore
import base64
# from prompts.coursify_prompt import COURSIFY_PROMPT
from prompts.tabler_prompt import TABLER_PROMPT
from prompts.dictator_prompt import DICTATOR_PROMPT
from prompts.quizzy_prompt import QUIZZY_PROMPT


def generate_pdf(content, filename):
    content = unicodedata.normalize('NFKD', content).encode('ascii', 'ignore').decode('ascii')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename, 'F')
    return pdf
>>>>>>> 80ffc79cfed73c088a094f8c43ae950f5a6d9b34

# Customizing the page configuration
st.set_page_config(
    page_title="Automated Course Content Generator",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

<<<<<<< HEAD
st.title("Automated Course Development (ACD) Model 🤖")
=======
load_dotenv()

st.title("Automated Course Content Generator 🤖")
>>>>>>> 80ffc79cfed73c088a094f8c43ae950f5a6d9b34

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

<<<<<<< HEAD
=======
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIError("Please provide OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
except OpenAIError as e:
    st.error(str(e))

# Ensure openai_model is initialized in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

>>>>>>> 80ffc79cfed73c088a094f8c43ae950f5a6d9b34
# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Example of using columns for advanced layouts
col1, col2 = st.columns(2)

<<<<<<< HEAD
col1, col_divider, col2 = st.columns([3.0, 0.1, 7.0])

with col1:
    st.header("Course Details 📋")
    
    # Function to create mandatory label with red asterisk
    def mandatory_label(label):
        return f"{label} <span style='color:red;'>*</span>"

    # Interactive widgets for course details
    st.markdown(mandatory_label("Course Name"), unsafe_allow_html=True)
    course_name = st.text_input("Enter the name of the course you'd like to generate")
    
    target_audience_edu_level = st.selectbox(
        "Target Audience Edu Level",
        ["N/A", "Primary", "High School", "Diploma", "Bachelors", "Masters"]
    )
    
    difficulty_level = st.radio(
        "Course Difficulty Level",
        ["N/A", "Beginner", "Intermediate", "Advanced"]
    )
    
    st.markdown(mandatory_label("No. of Modules"), unsafe_allow_html=True)
    num_modules = st.slider(
        "Use the slider to choose the number of modules (Max. 15)",
        min_value=1, max_value=15,
    )
    
=======
col1, col_divider, col2 = st.columns([3.0,0.1,7.0])

with col1:
    st.header("Course Details 📋")
    # Interactive widgets for course details
    course_name = st.text_input("Course Name")
    target_audience_edu_level = st.selectbox(
        "Target Audience Edu Level",
        ["Primary", "High School", "Diploma", "Bachelors", "Masters"]
    )
    difficulty_level = st.radio(
        "Course Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"]
    )
    num_modules = st.slider(
        "No. of Modules",
        min_value=1, max_value=15
    )
>>>>>>> 80ffc79cfed73c088a094f8c43ae950f5a6d9b34
    course_duration = st.text_input("Course Duration")
    course_credit = st.text_input("Course Credit")

    # Save widget states in session_state
    st.session_state.course_name = course_name
    st.session_state.target_audience_edu_level = target_audience_edu_level
    st.session_state.difficulty_level = difficulty_level
    st.session_state.num_modules = num_modules
    st.session_state.course_duration = course_duration
    st.session_state.course_credit = course_credit

<<<<<<< HEAD
    # Check if mandatory fields are filled
    if not course_name:
        st.warning("Please enter the Course Name.")
    if num_modules is None or num_modules < 1:
        st.warning("Please select the Number of Modules.")
=======

>>>>>>> 80ffc79cfed73c088a094f8c43ae950f5a6d9b34

    button1, button2 = st.columns([1, 0.8])
    with button1:
        generate_button = st.button("Generate Course Outline", help="Click me to generate course outline!😁")
    with button2:
        if "pdf" in st.session_state:
            new_course_button = st.button("Start a New Course", help="Click me to start a new course!💡")
            if new_course_button:
                st.session_state.course_name = ""
                st.session_state.target_audience_edu_level = ""
                st.session_state.difficulty_level = ""
                st.session_state.num_modules = 1
                st.session_state.course_duration = ""
                st.session_state.course_credit = ""
                st.session_state.pdf = False
                st.experimental_rerun()
                
    
<<<<<<< HEAD
=======


>>>>>>> 80ffc79cfed73c088a094f8c43ae950f5a6d9b34
with col2:
    st.header("Generated Course Content 📝")
    # Display the generated content here
    if generate_button and "pdf" not in st.session_state:
<<<<<<< HEAD

        with st.spinner("Generating course outline..."):
            
            course_outline = get_course_outline(course_name, target_audience_edu_level, difficulty_level, num_modules, course_duration, course_credit)

            st.success("Course outline generated successfully!")

            st.session_state['course_outline'] = course_outline
            st.session_state['buttons_visible'] = True

    if 'course_outline' in st.session_state and "pdf" not in st.session_state:
        st.session_state['modifications'] = True

        with st.expander("Course Outline", expanded=True):
            st.write(st.session_state['course_outline'])

            if 'buttons_visible' in st.session_state and st.session_state['buttons_visible']:
                complete_course_button = st.button(
                    "Looks good. Generate complete course!",
                    help="Click here to generate complete course!😍",
                    key="complete_course_button"
                )
                modifications_button = st.button(
                    "Wait! I need to make some modifications.",
                    help="Click here to modify the course outline!🧐",
                    key="modifications_button"
                )

                if modifications_button or st.session_state.get('modifications_pending', False):
                    modifications = st.text_area("Please enter the modifications you'd like to make:", key="modifications_input")
                    submit_modifications = st.button("Submit Modifications", key="submit_modifications")

                    if submit_modifications:
                        st.session_state['course_outline'] = modify_course_outline(
                            st.session_state['course_outline'], modifications
                        )
                        st.session_state['modifications_pending'] = False
                        st.rerun()  # Comment this line to avoid full reload

                    # Keep showing the modifications text area until they are submitted
                    st.session_state['modifications_pending'] = True
  
                if complete_course_button:
                    st.session_state['complete_course'] = True
                    st.session_state['modifications'] = False

        if 'complete_course' in st.session_state and st.session_state['complete_course']:
            with st.spinner("Generating complete course..."):
                gen_full_course(course_name, st.session_state['course_outline'])
                    
=======
        # Include user selections in the message history
        user_selections = f"Course Name: {course_name}\nTarget Audience Edu Level: {target_audience_edu_level}\nDifficulty Level: {difficulty_level}\nNo. of Modules: {num_modules}\nCourse Duration: {course_duration}\nCourse Credit: {course_credit}"
        st.session_state.messages.append({"role": "user", "content": user_selections})

        PROMPT=f"You are Prompter, the world's best Prompt Engineer. I am using another GenAI tool, Tabler, that helps in generating a course outline for trainers and professionals for the automated course content generation for their courses. Your job is to strictly use the only following inputs: 1) Course Name: {course_name} 2) Target Audience Edu Level: {target_audience_edu_level} 3) Course Difficulty Level: {difficulty_level} 4) No. of Modules: {num_modules} 5) Course Duration: {course_duration} 6) Course Credit: {course_credit}.  to generate a prompt for Tabler so that it can produce the best possible outputs. The prompt that you generate must be comprehensive and strictly follow the above given inputs and also mention the given inputs in the prompt you generate. Moreover, it is your job to also identify if the course name is appropriate and not gibberish."

        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": PROMPT},
            ]
        )
        generated_prompt = response.choices[0].message.content
        # st.success("Prompt generated successfully!")
        # st.write(generated_prompt)
        
        
        with st.spinner("Generating course outline..."):
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": TABLER_PROMPT},
                    {"role": "user", "content": generated_prompt},
                ]
            )
            Course_outline = response.choices[0].message.content
            st.success("Course outline generated successfully!")

            # with st.expander("Course Outline"):
            #     st.write(Course_outline)

            st.session_state['course_outline'] = Course_outline
            st.session_state['buttons_visible'] = True

    
    if 'course_outline' in st.session_state and "pdf" not in st.session_state:
        with st.expander("Course Outline"):
            st.write(st.session_state['course_outline'])

        if 'buttons_visible' in st.session_state and st.session_state['buttons_visible']:
            button1, button2 = st.columns([1, 2])
            with button1:
                complete_course_button = st.button("Looks cool. Generate complete course!", help="Click me to generate complete course!😍")
            with button2:
                modifications_button = st.button("Wai wait..!, I need to make some modifications", help="Click me to modify the course outline!🧐")

            # Handle button actions
            if complete_course_button:
                st.session_state['complete_course'] = True
                st.session_state['modifications'] = False
            elif modifications_button:
                st.session_state['modifications'] = True
                st.session_state['complete_course'] = False

            if 'complete_course' in st.session_state and st.session_state['complete_course']:
                with st.spinner("Generating complete course..."):
                    response = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": "system", "content": DICTATOR_PROMPT},
                            {"role": "user", "content": st.session_state['course_outline']},
                        ]
                    )
                    Dict = response.choices[0].message.content
                    # st.success("DICTator is here!")
                    # st.write(Dict)

                    
                    module_lessons = json.loads(Dict)
                    # st.write(module_lessons)

                    for module_name in module_lessons:
                        module_content = ""

                        for lesson_name in module_lessons[module_name]:
                            module_lesson_prompt =f"""You are Coursify, an AI assistant specialized in generating high-quality educational content for online courses. Your knowledge spans a wide range of academic and professional domains, allowing you to create in-depth and engaging material on any given topic. For this task, you will be generating detailed content for the lesson '{lesson_name}' which is part of the module '{module_name}' in the course '{course_name}'. Your goal is to provide a comprehensive and learner-friendly exploration of this specific topic, covering all relevant concepts, theories, and practical applications, as if you were an experienced instructor teaching the material.

                            To ensure the content is effective and aligns with best practices in instructional design, you will follow Bloom's Taxonomy approach. This means structuring the material in a way that progressively builds learners' knowledge and skills, starting from foundational concepts and working up to higher-order thinking and application. Your response should be verbose, with in-depth explanations, multiple examples, and a conversational tone that mimics an instructor's teaching style.

                            The structure of your response should include (but NOT limited to) the following elements:

                            1) Introduce the topic and provide context, explaining its relevance and importance within the broader course and domain, as an instructor would do in a classroom setting.
                            2) Define and clarify key terms, concepts, and principles related to the topic, with detailed explanations, analogies, and examples to aid comprehension.
                            3) Present thorough, step-by-step explanations of the concepts, using real-world scenarios, visual aids, and analogies to ensure learners grasp the material.
                            4) Discuss real-world applications, case studies, or scenarios that demonstrate the practical implications of the topic, drawing from industry best practices and authoritative sources.
                            5) Incorporate interactive elements, such as reflective questions, exercises, or problem-solving activities, to engage learners and reinforce their understanding, as an instructor would do in a classroom.
                            6) Seamlessly integrate relevant tangential concepts or background information as needed to provide a well-rounded learning experience, ensuring learners have the necessary foundational knowledge.
                            7) Maintain a conversational, approachable tone while ensuring accuracy and depth of content, as if you were an experienced instructor teaching the material.

                            Remember, the goal is to create a comprehensive and self-contained learning resource on the specified topic, with the level of detail and instructional quality that one would expect from an expert instructor. Your output should be formatted using Markdown for clarity and easy integration into course platforms.
                            Note: Add a blank line at the end of the course content.
                            Make sure the content generated is easily convertible to a sensible using HTML Tags.
                            """
                            with st.spinner(f"Generating content for {module_name}, {lesson_name}"):
                                response = client.chat.completions.create(
                                    model=st.session_state["openai_model"],
                                    messages=[
                                        {"role": "system", "content": module_lesson_prompt},
                                        # {"role": "user", "content": st.session_state['course_outline']},
                                    ]
                                )
                                complete_course = response.choices[0].message.content
                                st.success(f"Generated content for {module_name}, {lesson_name}")

                                with st.expander("Click to view!"):
                                    st.write(complete_course)
                                
                                module_content +=  complete_course + "\n"*2
                        quizzy_prompt_final = QUIZZY_PROMPT + module_content
                        with st.spinner(f"Generating quiz questions for {module_name}"):
                            res = client.chat.completions.create(
                                model=st.session_state["openai_model"],
                                messages=[
                                    {"role": "system", "content": quizzy_prompt_final},
                                    # {"role": "user", "content": st.session_state['course_outline']},
                                ]
                            )
                            quiz_questions = res.choices[0].message.content

                            st.success(f"Quiz time!! Generated quiz questions for {module_name}")
                            with st.expander("Click to view!"):
                                st.write(quiz_questions)

                            if "pdf" not in st.session_state:
                                complete_course_content = module_content + "\n\n" + quiz_questions
                                st.session_state.pdf = generate_pdf(complete_course_content, "course.pdf")
                                b64 = base64.b64encode(st.session_state.pdf.output(dest="S").encode('latin1')).decode()
                                st.success("Your PDF file is ready!")

                            button_label = "Download PDF"
                            st.download_button(label=button_label, data=b64, file_name="course.pdf", mime="application/pdf", key="download_pdf_button")
                                    

                        break

                
            elif 'modifications' in st.session_state:
                modifications = st.text_input("Please enter the modifications you'd like to make:")
                if modifications:
                    st.session_state.modifications = modifications
                    Mod = f""" I have provided you with the "course outline" and "modifications". Your task is to modify the existing course outline using modifications provided, and give complete modified course outline as the output. 
                    modifications:
                    {st.session_state.modifications} 
                    course outline:
                    {st.session_state['course_outline']}"""

                    response = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": "system", "content": TABLER_PROMPT},
                            {"role": "user", "content": Mod},
                        ]
                    )
                    Mod_CO = response.choices[0].message.content

                    with st.spinner("Generating complete course with the specified modifications..."):
                        response = client.chat.completions.create(
                            model=st.session_state["openai_model"],
                            messages=[
                                {"role": "system", "content": DICTATOR_PROMPT},
                                {"role": "user", "content": Mod_CO},
                            ]
                        )
                        Dict = response.choices[0].message.content
                        # st.success("DICTator is here!")
                        # st.write(Dictt)

                        
                        module_lessons = json.loads(Dict)
                        # st.write(module_lessons)

                        for module_name in module_lessons:
                            module_content = ""

                            for lesson_name in module_lessons[module_name]:
                                module_lesson_prompt =f"""You are Coursify, an AI assistant specialized in generating high-quality educational content for online courses. Your knowledge spans a wide range of academic and professional domains, allowing you to create in-depth and engaging material on any given topic. For this task, you will be generating detailed content for the lesson '{lesson_name}' which is part of the module '{module_name}' in the course '{course_name}'. Your goal is to provide a comprehensive and learner-friendly exploration of this specific topic, covering all relevant concepts, theories, and practical applications, as if you were an experienced instructor teaching the material.

                                To ensure the content is effective and aligns with best practices in instructional design, you will follow Bloom's Taxonomy approach. This means structuring the material in a way that progressively builds learners' knowledge and skills, starting from foundational concepts and working up to higher-order thinking and application. Your response should be verbose, with in-depth explanations, multiple examples, and a conversational tone that mimics an instructor's teaching style.

                                The structure of your response should include (but NOT limited to) the following elements:

                                1) Introduce the topic and provide context, explaining its relevance and importance within the broader course and domain, as an instructor would do in a classroom setting.
                                2) Define and clarify key terms, concepts, and principles related to the topic, with detailed explanations, analogies, and examples to aid comprehension.
                                3) Present thorough, step-by-step explanations of the concepts, using real-world scenarios, visual aids, and analogies to ensure learners grasp the material.
                                4) Discuss real-world applications, case studies, or scenarios that demonstrate the practical implications of the topic, drawing from industry best practices and authoritative sources.
                                5) Incorporate interactive elements, such as reflective questions, exercises, or problem-solving activities, to engage learners and reinforce their understanding, as an instructor would do in a classroom.
                                6) Seamlessly integrate relevant tangential concepts or background information as needed to provide a well-rounded learning experience, ensuring learners have the necessary foundational knowledge.
                                7) Maintain a conversational, approachable tone while ensuring accuracy and depth of content, as if you were an experienced instructor teaching the material.

                                Remember, the goal is to create a comprehensive and self-contained learning resource on the specified topic, with the level of detail and instructional quality that one would expect from an expert instructor. Your output should be formatted using Markdown for clarity and easy integration into course platforms.
                                Note: Add a blank line at the end of the course content.
                                Make sure the content generated is easily convertible to a sensible using HTML Tags.
                                """
                                with st.spinner(f"Generating content for {module_name}, {lesson_name}"):
                                    response = client.chat.completions.create(
                                        model=st.session_state["openai_model"],
                                        messages=[
                                            {"role": "system", "content": module_lesson_prompt},
                                            # {"role": "user", "content": st.session_state['course_outline']},
                                        ]
                                    )
                                    complete_course = response.choices[0].message.content
                                    st.success(f"Generated content for {module_name}, {lesson_name}")

                                    with st.expander("Click to view!"):
                                        st.write(complete_course)
                                    
                                    module_content +=  complete_course + "\n"*2
                            quizzy_prompt_final = QUIZZY_PROMPT + module_content
                            with st.spinner(f"Generating quiz questions for {module_name}"):
                                res = client.chat.completions.create(
                                    model=st.session_state["openai_model"],
                                    messages=[
                                        {"role": "system", "content": quizzy_prompt_final},
                                        # {"role": "user", "content": st.session_state['course_outline']},
                                    ]
                                )
                                quiz_questions = res.choices[0].message.content

                                st.success(f"Quiz time!! Generated quiz questions for {module_name}")
                                with st.expander("Click to view!"):
                                    st.write(quiz_questions)


                                if "pdf" not in st.session_state:
                                    complete_course_content = module_content + "\n\n" + quiz_questions
                                    st.session_state.pdf = generate_pdf(complete_course_content, "course.pdf")
                                    b64 = base64.b64encode(st.session_state.pdf.output(dest="S").encode('latin1')).decode()
                                    st.success("Your PDF file is ready!")

                                button_label = "Download PDF"
                                st.download_button(label=button_label, data=b64, file_name="course.pdf", mime="application/pdf", key="download_pdf_button", help="Click me to download PDF 😌")

                            break


>>>>>>> 80ffc79cfed73c088a094f8c43ae950f5a6d9b34
    else:
        st.write("Your generated content will appear here.")

# Save chat history after each interaction
save_chat_history(st.session_state.messages)
