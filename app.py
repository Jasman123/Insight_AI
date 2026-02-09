import streamlit as st

pages = {
    "System Option": [
        st.Page("pages/chat.py", title="Assist with PDF Chatbot"),
        st.Page("pages/pdf_upload.py", title="PDF ingestion and management"),
        
    ]
}

pg = st.navigation(pages)
pg.run()

#create streamtlit shortcut
# cmd.exe /k "F:\python_project\.venv\Scripts\python.exe -m streamlit run F:\python_project\Stremlit_project_dashboard\app.py --server.headless true"