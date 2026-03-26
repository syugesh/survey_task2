SurveyMonkey API Project
What this does
This is a simple Flask API that creates a SurveyMonkey survey from a JSON request.
It will:
* Create a survey
* Add a page
* Add questions
* Give you a shareable survey link

Setup
1. Clone the repo
git clone <your-repo-url>
cd <repo-name>
2. Create virtual environment
python3 -m venv venv
3. Activate it
Mac/Linux:
source venv/bin/activate
Windows:
venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt

Environment variable
Create a .env file in the project folder:
SM_TOKEN=your_token_here

Run the app
python app.py
App will run on:
http://localhost:8080

API Endpoint
Create Survey
curl -X POST http://localhost:8080/create-survey \
-H "Content-Type: application/json" \
-d @questions.json

Response:
If everything works:
{
  "survey_link": "your_generated_link"
}
If something fails:
{
  "server error during survey creation"
}


Notes
* You need a valid SurveyMonkey API token
* Make sure .env is set correctly
* Logs are saved in survey_app.log
