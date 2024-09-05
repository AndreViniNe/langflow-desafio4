MAX_FILE_SIZE = 1 * 1024 * 1024 #1Mb

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
import requests
# from datetime import datetime
# import time
# import os
from database_infos import DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USERNAME

# password = os.environ["DATABASE_PASSWORD"]
# username = os.environ["DATABASE_USERNAME"]
# host = os.environ["DATABASE_HOST"]

#-----------DATABASE CONNECTION-----------

@st.cache_resource
def get_connection():
    engine = create_engine(f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/postgres")
    Session = sessionmaker(bind=engine)
    return Session()
    
# session = get_connection()
# session.close()


#-----------STREAMLIT SIDEBAR-----------
st.sidebar.markdown("## User informations for job search")

user_name = st.sidebar.text_input("**Your name**", value="...")

st.sidebar.divider()

job_preferences = st.sidebar.text_input("**Job Preferences (work modality, posting date, localization etc)**", value="My preferences are...")

st.sidebar.divider()

def reset_file_uploader():
    st.session_state['cv_file'] = None

cv_file = st.sidebar.file_uploader(f"Attach your CV **here** ({MAX_FILE_SIZE / (1024 * 1024)}MB limit):", type=["png", "jpg", "pdf", "docx", "doc"])

if cv_file is not None:
    file_size = cv_file.size

    if file_size > MAX_FILE_SIZE:
        st.error(f"The file is too large! The maximum allowed size is {MAX_FILE_SIZE / (1024 * 1024)}MB.\nChoose another file!")
        reset_file_uploader()
    else:
        st.sidebar.write("File name:", cv_file.name)

linkedin_url = st.sidebar.text_input("**Enter your LinkedIn profile link**")

if st.sidebar.button('Submit'):
    if user_name and job_preferences and linkedin_url:
        session = get_connection()
        try:
            session.execute(
                text("""
                    INSERT INTO user_infos (user_name, job_preferences, linkedin_url, cv_file)
                    VALUES (:name, :job_preferences, :linkedin_url, :cv_file)
                """),
                {
                    'name': user_name,
                    'job_preferences': job_preferences,
                    'linkedin_url': linkedin_url,
                    'cv_file': cv_file.read() if cv_file else None
                }
            )
            session.commit()
        finally:
            session.close()
            st.sidebar.success('Information successfully submitted!')
    else:
        st.sidebar.error('Please fill in all required fields.')


st.sidebar.divider()

#-----------STREAMLIT PRINCIPAL PAGE-----------
st.markdown("## Estagio Delivery ")
if st.button("Find the jobs you need based on your preference"):

    session = get_connection()
    session.execute(
        text("""
            UPDATE user_infos
            SET status = 'Processing...'
            WHERE user_name = :user_name;
        """),
        {
            'user_name': user_name,
        }
    )
    session.commit()

    st.write("Processing...")

    #API LANGFLOW
    r = requests.get('http://127.0.0.1:7860/api/v1/run/dd54d39d-380b-4892-9269-7cc578452059?stream=false')
    st.write(r)

    st.success("Processed")
    session.execute(
        text("""
            UPDATE user_infos
            SET status = 'Processed!'
            WHERE user_name = :user_name;
        """),
        {
            'user_name': user_name,
        }
    )
    session.commit()
