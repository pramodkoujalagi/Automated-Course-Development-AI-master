from loop_prompts_stream import quizzy_prompt, quizzy_prompt_latex, pointnary_prompt, make_coursify_prompt, make_coursify_ppt_prompt, make_coursify_prompt_latex
from all_prompts_stream import MARKER_SYSTEM_PROMPT
from ppt_generation import ppt_generator
import json 
import openai 
from dotenv import load_dotenv
import os
import io
import re
from pylatex import Document,Package
from pylatex.utils import NoEscape
import streamlit as st
import tempfile

@st.cache_data()

def filter_latex_document(latex_content):
    """
    Filters the LaTeX content to remove all instances of \begin{document} and \end{document}
    except the first \begin{document} and the last \end{document}.
    Also removes intermediate triple quotes and occurrences of 'latex'.
    """
    # Remove intermediate triple quotes and occurrences of 'latex'
    filtered_content = re.sub(r'```latex', '', latex_content)
    filtered_content = re.sub(r'```', '', filtered_content)
    filtered_content = re.sub(r'latex', '', filtered_content)

    # Split the content into lines
    lines = filtered_content.split('\n')
    
    # Find the positions of all \begin{document} and \end{document}
    begin_positions = [i for i, line in enumerate(lines) if '\\begin{document}' in line]
    end_positions = [i for i, line in enumerate(lines) if '\\end{document}' in line]
    
    # Keep the first \begin{document} and the last \end{document}
    if begin_positions and end_positions:
        first_begin = begin_positions[0]
        last_end = end_positions[-1]
        
        # Filter out other \begin{document} and \end{document}
        for i in range(len(lines)):
            if i in begin_positions[1:] or i in end_positions[:-1]:
                lines[i] = ''
    
    # Join the filtered lines back into a single string
    filtered_content = '\n'.join(lines)
    return filtered_content

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def generate_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}_V{counter}{ext}"
    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{base}_V{counter}{ext}"
    return new_filename

def generate_pdf_latex(course_name, latex_str, filename):
    # Filter out the initial 'latex' line if present
    if latex_str.startswith("latex\n"):
        latex_str = latex_str[len("latex\n"):]

    # Create a new document with specific documentclass and packages
    doc = Document(documentclass='article')
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('hyperref'))
    doc.packages.append(Package('geometry', options=['margin=1in']))
    doc.packages.append(Package('parskip', options=['*']))

    # Add title page with course name in the center, bold, and capitalized
    doc.preamble.append(NoEscape(r'\title{\vspace{3in}\textbf{\uppercase{' + course_name + '}}}'))
    doc.preamble.append(NoEscape(r'\date{}'))
    doc.preamble.append(NoEscape(r'\author{}'))
    doc.append(NoEscape(r'\maketitle'))
    doc.append(NoEscape(r'\newpage'))

    # Preprocess the LaTeX string to add space before and after sections and subsections
    formatted_latex_str = latex_str.replace(r'\section*', r'\vspace{1em}\section*')
    formatted_latex_str = formatted_latex_str.replace(r'\subsection*', r'\vspace{0.5em}\subsection*')
    formatted_latex_str = formatted_latex_str.replace(r'\subsubsection*', r'\vspace{0.5em}\subsubsection*')
    formatted_latex_str = formatted_latex_str.replace(r'\textbf', r'\vspace{0.5em}\textbf')

    # Ensure proper spacing around lists
    for i in range(1, 11):
        formatted_latex_str = formatted_latex_str.replace(f'\n{i}. ', f'\n\n{i}. ')

    # Ensure proper formatting for quizzes
    formatted_latex_str = re.sub(r'(\d+\.\s[^\n]+)\n', r'\1\n\n', formatted_latex_str)  # Add extra newline after each question
    formatted_latex_str = re.sub(r'(\([a-e]\)\s[^\n]+)', r'\n\1\n', formatted_latex_str)  # Add newline before and after each option

    # Add the formatted LaTeX string to the document
    doc.append(NoEscape(formatted_latex_str))
    
    # Generate the .tex file
    tex_file = 'temp_output'
    try:
        doc.generate_tex(tex_file)
        tex_file += '.tex'
    except Exception as e:
        print(f"Error generating .tex file: {e}")
        return

    # Check if the .tex file was created successfully
    if not os.path.exists(tex_file):
        print("Error: The .tex file was not created successfully.")
        return

    # Use pdflatex to convert the .tex file to a .pdf file
    os.system(f'pdflatex -interaction=nonstopmode {tex_file}')
    
    # Determine the name of the generated PDF
    generated_pdf = tex_file.replace('.tex', '.pdf')
    
    # Check if the PDF was created successfully
    if os.path.exists(generated_pdf):
        # Sanitize the desired filename
        # print("Sanitizing file name")
        sanitized_filename = sanitize_filename(filename)

        # Generate a unique filename if it already exists
        if os.path.exists(sanitized_filename):
            sanitized_filename = generate_unique_filename(sanitized_filename)
        
        # print("Sanitized file name - ", sanitized_filename)
        # Rename and move the generated PDF to the desired filename
        os.rename(generated_pdf, sanitized_filename)
        st.success("Your PDF File has been generated successfully! \nKindly view it in the app source folder.")
    
    else:
        print("Error: The PDF file was not generated successfully.")
        print("Error File Name: ", generated_pdf)
        st.error("An Error Occured while trying to generate your PDF :( \nPlease try again in some time.")

    # Clean up auxiliary files
    for ext in ['aux', 'log', 'out', 'tex']:
        aux_file = tex_file.replace('.tex', f'.{ext}')
        if os.path.exists(aux_file):
            os.remove(aux_file)


#Function to load equations and symbols in appropriate format in Streamlit
def render_markdown_with_latex(content):
    # Split the content into parts where LaTeX and Markdown are separated
    parts = re.split(r'(\$\$.*?\$\$|\$.*?\$)', content, flags=re.DOTALL)
    
    for part in parts:
        if part.startswith('$$') and part.endswith('$$'):
            # This is a block LaTeX equation
            st.latex(part[2:-2])
        elif part.startswith('$') and part.endswith('$'):
            # This is an inline LaTeX equation
            st.latex(part[1:-1])
        else:
            # This is a regular Markdown text
            st.markdown(part, unsafe_allow_html=True)

# Loading the API key from the .env file
load_dotenv()
openai.api_key = os.getenv("TE_OPENAI_KEY")

#Defining a singular function to call the API
def load_api(messages):

  response = openai.ChatCompletion.create(
    model="gpt-4o",
    temperature=0.3,  # Low temperature for less randomness
    top_p=0.8,  # Moderate top-p for some diversity
    messages=messages)

  response_content = response.choices[0].message.content
  
  return response_content

def make_course_content(course_name, module_lesson_dict):

  course_content = ""
  module_num = 0

  #Looping through the modules
  for module_name in module_lesson_dict:
    
    #Saving the module number for PPT File name
    module_num+=1

    #Initiating an empty string to store the PDF Content
    module_content = ""

    #Creating an empty dictionary to store the PPT content information
    ppt_input_dict = {}

    #Storing the course name in the PPT Dict
    ppt_input_dict['title'] = course_name
    ppt_input_dict['content'] = {}

    #Initiating an empty dictionary for the module to store PPT Content
    ppt_input_dict['content'][module_name] = {}
    
    #Looping through the lessons
    for lesson_name in module_lesson_dict[module_name]:
      
        with st.spinner(f"Generating content for {module_name}, {lesson_name}"):

            #CONTENT FOR PDF

            #Generating the prompt for lesson content for the PDF using Coursify
            # coursify_prompt = make_coursify_prompt(course_name, module_name, lesson_name)
            coursify_prompt = make_coursify_prompt_latex(course_name, module_name, lesson_name)

            coursify_messages = [{"role": "system", "content": coursify_prompt}]

            #Calling the client instance for the generated prompt - Course (Lesson) Content in LaTex format 
            course_completion = load_api(coursify_messages)

            #Converting the LaTex output to Markdown for readability - Using Marker
            marker_messages = [{"role": "system", "content": MARKER_SYSTEM_PROMPT}]
            marker_messages.append({"role": "user", "content": course_completion})
            
            #Loading the generated content in a displayable format.
            display_course_content = load_api(marker_messages)

            st.success(f"Generated content for {module_name}, {lesson_name}")
            
            with st.expander("Click to view!"):
                st.markdown(display_course_content)  
                #   render_markdown_with_latex(display_course_content)  

        #Appending the lesson content to the module content
        module_content +=  course_completion + "\n"*2

        #CONTENT FOR PPT

        #Generating the prompt for lesson content for the PPT using Coursify_PPT
        coursify_ppt_prompt = make_coursify_ppt_prompt(course_name, module_name, lesson_name)
        
        coursify_ppt_messages = [{"role": "system", "content": coursify_ppt_prompt}]

        #Calling the client instance for the generated prompt
        lesson_ppt_content = load_api(coursify_ppt_messages)
        
        #Converting the generated PPT Content to dictionary using the PointNary prompt   
        pointnary_messages = [{"role": "system", "content": pointnary_prompt}]
        pointnary_messages.append({"role": "user", "content": lesson_ppt_content})

        lesson_ppt_info = load_api(pointnary_messages)

        lesson_ppt_dict = json.loads(lesson_ppt_info.strip())

        #Storing the dictionary within the lesson dictionary
        ppt_input_dict['content'][module_name][lesson_name] = lesson_ppt_dict
    

    #DISPLAY MODULE CONTENT -> Add Buttons
    
    # Generating PPT for the module - CREATE BUTTON
    # ppt_yes_no = input("Do you want the PPT for this module?(Yes/No): ")
    st.session_state['ppt_button_visible'] = True

    if 'ppt_button_visible' in st.session_state and st.session_state['ppt_button_visible']:
        filename = f"{course_name} - Module {module_num}.pptx"
        ppt_bytes = ppt_generator(ppt_input_dict, filename)

        if ppt_bytes:
            st.download_button(
                label=f"Download PPT for {module_name}",
                data=ppt_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                help="Click here to download the PPTx file for the module."
            )
        else:
            st.error(f"Failed to generate PPT for {module_name}")


    # Generating the quiz content using the Quizzy prompt
    quizzy_prompt_final = quizzy_prompt_latex + module_content

    with st.spinner(f"Generating quiz questions for {module_name}"):
      quizzy_messages = [{"role": "system", "content": quizzy_prompt_final}]
      quiz = load_api(quizzy_messages)

      #Converting the LaTex output to Markdown for readability - Using Marker
      marker_messages_quiz = [{"role": "system", "content": MARKER_SYSTEM_PROMPT}]
      marker_messages_quiz.append({"role": "user", "content": quiz})
      
      #Loading the generated content in a displayable format.
      display_quiz_content = load_api(marker_messages_quiz)

      #Converting the generated quiz into a displayable format - Using Marker
      st.success(f"Quiz time! Generated quiz questions for {module_name}")
      
      with st.expander("Click to view!"):
        st.markdown(display_quiz_content)

    module_content = module_content + '\n'*2 + quiz

    course_content += module_content + '\n'*5
  
  if "pdf" not in st.session_state:
    #Filtering the generated course content to form a uniform document
    filtered_content = filter_latex_document(course_content)
    st.success("Your content is ready to be downloaded!")

  button_label = "Download Course PDF"
  pdf_gen_button = st.button(button_label, help="Click here to download the generated course content in PDF.")

  if pdf_gen_button:

    with st.spinner("Please wait while we generate your PDF..."):

        generate_pdf_latex(course_name, filtered_content, f'{course_name}.pdf')


  return

    

