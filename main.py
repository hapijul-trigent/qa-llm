from langchain import PromptTemplate
from app import build
import streamlit as st



# Set main panel
st.set_page_config(
    page_title="Toy Demo2 - Trigent",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
# Build App
build()