MAX_FILE_SIZE = 1 * 1024 * 1024 #1Mb

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
import requests
import asyncio
import pandas as pd
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
st.markdown("## Job Hero ")
if st.button("Find the jobs you need based on your preference"):
    #API LANGFLOW
    # r = requests.request("POST", "http://127.0.0.1:7860/api/v1/run/853b597d-5d3b-4994-bcb6-48bc20e9821e")
    # st.write(r.text)

    async def langflow_request_background():
        # write processing message with spinner
        with st.spinner(f'Processing API request for {user_name}...'):
            while True:
                await asyncio.sleep(20)

    async def main_request():
        task = asyncio.create_task(langflow_request_background())
        await asyncio.sleep(0)

        result = await asyncio.to_thread(requests.post, "http://127.0.0.1:7860/api/v1/run/853b597d-5d3b-4994-bcb6-48bc20e9821e")

        st.success("Processing finished. Here are their best job recommendations:")


    # task = asyncio.create_task(langflow_request())
    asyncio.run(main_request())

    session = get_connection()
    try:
        query = session.execute(
            text("""
                SELECT ui.user_name, ji.job_title, ji.company, ji.company_url, ji.job_description, ji.posting_date,
                 ji.job_localization, ji.job_search_time, ji.apply_url 
                FROM job_infos ji
                JOIN user_infos ui ON ji.user_id = ui.user_id
                WHERE ui.user_name = :name;
            """),
            {
                'name': user_name,
            }
        )

        df = pd.DataFrame(query.fetchall(), columns=query.keys())
        df = df.drop_duplicates(subset=["job_description"], keep="first")
    finally:
        session.close()

        container = st.container()
        if not df.empty:
            # st.dataframe(df)

            container.data_editor(
                df,
                column_config={
                    "apply_url": st.column_config.LinkColumn(
                        "Job url", display_text="Apply now"
                    ),
                },
                hide_index=True)

        else:
            container.write("0 results.")