import streamlit as st
from langchain_openai import OpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from prompts import prompt_rewrite, prompt_blogger, prompt_extractor, prompt_qacsv
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain.evaluation.qa import QAEvalChain
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import pypdf

#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    # llm_groq_mixtral = ChatGroq(
    #     model="mixtral-8x7b-32768",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     groq_api_key = api_key
    # )
    return llm


def get_openai_api_key():
    input_text = st.text_input(
        label="OpenAI API Key ",  
        placeholder="Ex: sk-2twmA8tfCb8un4...", 
        key="openai_api_key_input", 
        type="password"
    )
    return input_text


def generateBlog(topic: str, llm: OpenAI):
    """Blog Generator"""
    query = prompt_blogger.format(topic=topic)
    response = llm(query, max_tokens=2048)
    return response

def extractKeyInfo(review_input:str, llm):
    """Extract Key Information"""
    prompt_with_review = prompt_extractor.format(
        review=review_input
    )
    key_data_extraction = llm(prompt_with_review)
    return key_data_extraction


def generate_response(txt, llm):
    """To Summarize the Text"""
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce"
    )
    return chain.invoke(docs)



#Input OpenAI API Key
def get_openai_api_key():
    input_text = st.text_input(
        label="OpenAI API Key ",  
        placeholder="Ex: sk-2twmA8tfCb8un4...", 
        key="openai_api_key_input", 
        type="password")
    return input_text



def create_db(file, openai_api_key, type_='pdf'):
    """create Vector db"""
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectordb_file_path = "my_vecdtordb"
    loader = CSVLoader(file_path=file, source_column="prompt") if type_ == 'csv' else PyPDFLoader(file_path=file)
    try:
        documents = loader.load()
    except pypdf.errors.PdfStreamError as e:
        del loader
        loader = CSVLoader(file_path=file, source_column="prompt")
        documents = loader.load()
    vectordb = FAISS.from_documents(documents, embedding)

    # Save vector database locally
    vectordb.save_local(vectordb_file_path)
    
    return vectordb_file_path, embedding


def qa_chain(query: str, context, embedding, llm):
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(context, embedding, allow_dangerous_deserialization=True)
    retriever = vectordb.as_retriever(score_threshold=0.7)

    # Create chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_qacsv}
    )


    # create an eval chain
    eval_chain = QAEvalChain.from_llm(llm=llm)
    # have it grade itself
    graded_outputs = eval_chain.evaluate(
        real_qa,
        predictions,
        question_key="question",
        prediction_key="result",
        answer_key="answer"
    )
    
    response = {
        "predictions": predictions,
        "graded_outputs": graded_outputs
    }
    
    return response

    return chain.invoke(query)


if __name__ == "__main__":
    create_db()
    chain = execute_chain()
    btn = st.button("Private button: re-create database")
    if btn:
        create_db()
    question = st.text_input("Question: ")
    if question:
        chain = execute_chain()
        response = chain(question)
        st.header("Answer")
        st.write(response["result"])