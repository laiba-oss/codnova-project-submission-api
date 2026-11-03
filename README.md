# Project Submission API

A REST API built with Python and FastAPI to submit, search, filter, and moderate project submissions.

## Technologies Used
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Features
- Submit project details
- Validate GitHub and demo URLs
- Search projects by title or description
- Filter projects by domain
- Pagination support
- Admin-key protected project moderation
- Approve or reject submissions with feedback

## Installation

1. Clone the repository:

   git clone https://github.com/laiba-oss/codnova-project-submission-api.git

2. Open the project folder.

3. Create and activate a virtual environment:

   python -m venv venv

   venv\Scripts\activate

4. Install dependencies:

   pip install -r requirements.txt

5. Create a `.env` file using the `.env.example` template and set your own admin key.

6. Run the API:

   uvicorn app.main:app --reload

## API Documentation

Open the following URL after starting the server:

http://127.0.0.1:8000/docs

## Main Endpoints

- POST `/projects/` — Submit a project
- GET `/projects/` — List projects
- GET `/projects/?search=AI` — Search projects
- GET `/projects/?domain=Artificial Intelligence` — Filter by domain
- PATCH `/projects/{project_id}/moderate` — Moderate a project

Admin moderation requires the `X-Admin-Key` header.

## Author
Laiba Ghazanfar