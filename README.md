# FastAPI Backend

This is the FastAPI backend for Codecraft. The backend provides APIs for managing workflows (creation, updating, deletion, starting executions, checking statuses, and retrying executions). It integrates with a database using SQLAlchemy for asynchronous operations and supports file processing, including text, JSON, CSV, PDF, and DOCX files. Additionally, the backend enables the execution of LLM (Large Language Model) operations for analyzing inputs via various models like GPT-3.5, Mistral, and Claude, based on user-provided prompts and data.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Backend](#running-the-backend)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- *check requirements.txt

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Codecraft-Insightgen/Codecraft.git
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Backend

1. Start the FastAPI server using Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```

2. The backend will be running at `http://127.0.0.1:8000`

## API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Creating docker image and running it
docker build -t lcnc_platform .



## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


<font size="0"><span style="color:grey"><br>_This is an Easter Egg. Thanks for reading until the end. <br>
-Sarang Shelke_</span>
