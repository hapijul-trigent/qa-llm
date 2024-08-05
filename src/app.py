import streamlit as st
from utils import get_openai_api_key, load_LLM
from streamlit_option_menu import option_menu
from utils import generateBlog, extractKeyInfo, create_db, qa_chain
from prompts import prompt_rewrite
import os

# Application
def build():
    """Streamlit application"""
    # Define the options and corresponding prompts
    options = {
        "Rewriter": "Provide the text you want rewritten:",
        "Blogger": "Provide the topic you want to blog about:",
        "Extractor": "Provide the text from which you want to extract information:",
        "PDF QA": "Upload the PDF for QA:",
        "CSV QA": "Upload the CSV for QA:"
    }

    
    #Input OpenAI API Key
    st.markdown("## Enter Your OpenAI API Key")
    openai_api_key = get_openai_api_key()

    # Select Option
    with st.sidebar:
        option = option_menu(
            "Rewriter", list(options.keys()), 
                icons=[], menu_icon="cast", default_index=0
            )

    # Display the corresponding prompt based on the selected option
    st.write(f"### {option}")
    if option in ["TextFile Summarizer", "PDF QA", "CSV QA"]:
        uploaded_file = st.file_uploader("Choose a file", type=["pdf" if option == "PDF QA" else ("csv" if option=='CSV QA' else "txt")])
        if uploaded_file is not None:
            
            # Define the save path
            save_path = os.path.join("uploaded_files", uploaded_file.name)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save the file
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.write(f"File saved to: {save_path}")
    else:
        user_input = st.text_area(options[option])




    llm = None
    if openai_api_key:
        # st.warning('Please insert OpenAI API Key. \
        #     Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
        #     icon="⚠️")
        # Load
        llm = load_LLM(openai_api_key=openai_api_key)

        # Prompt template tunning options
        if option == 'Rewriter':
            if user_input:
                if len(user_input.split(" ")) > 700:
                    st.write("Please enter a shorter text. The maximum length is 700 words.")
                    st.stop()
                
                col1, col2 = st.columns(2)
                with col1:
                    option_tone = st.selectbox(
                        'Which tone would you like your redaction to have?',
                        ('Formal', 'Informal'))
                    
                with col2:
                    option_dialect = st.selectbox(
                        'Which English Dialect would you like?',
                        ('American', 'British'))
                st.markdown("### Your Re-written text:")

                # get Output
                prompt_with_draft = prompt_rewrite.format(
                    tone=option_tone, 
                    dialect=option_dialect, 
                    draft=user_input
                )
                improved_redaction = llm(prompt_with_draft)
                st.write(improved_redaction)

        elif option == 'Blogger':
            # For Blogger
            if user_input:
                response = generateBlog(topic=user_input, llm=llm)
                st.divider()
                st.subheader('Generated Blog')
                st.write(response)
        elif option == 'Extractor':
            if user_input:
                response = extractKeyInfo(review_input=user_input, llm=llm)
                st.divider()
                st.write(response)
        elif option == 'PDF QA':
            if uploaded_file and openai_api_key:
                query = st.text_area(options[option])
                context, embedding = create_db(file=save_path, openai_api_key=openai_api_key)
                response = qa_chain(query=query, context=context, embedding=embedding, llm=llm)
                st.divider()
                st.write('Answer: ', response['result'])
        else:
            if uploaded_file and openai_api_key:
                query = st.text_area(options[option])
                context, embedding = create_db(file=save_path, openai_api_key=openai_api_key)
                response = qa_chain(query=query, context=context, embedding=embedding, llm=llm)
                st.divider()
                st.write('Answer: ', response['result'])
