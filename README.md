# QA-LLM

## Overview
QA-LLM is a project designed to implement a Question-Answering system using large language models (LLMs). This repository contains the necessary code and resources to build and run a QA system, leveraging modern NLP techniques.
```sh
qa-llm/
├── my_vecdtordb/         # Directory for vector database storage
├── uploaded_files/       # Directory for storing uploaded files
├── app.py                # Flask application for web interface
├── main.py               # Main script to run the QA system
├── prompts.py            # Contains prompt templates for the QA system
├── utils.py              # Utility functions for the project
├── requirements.txt      # Required dependencies
└── README.md             # Project README file
```


## Features
- Implementation of a QA system using state-of-the-art language models.
- Examples and tests to showcase the functionality.
- Easy-to-understand code structure, suitable for educational purposes and extensions.

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/hapijul-trigent/qa-llm.git
    cd qa-llm
    ```
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running the QA System
To start the QA system, run the following command:
```sh
streamlit run main.py

