import os
import logging
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    handlers=[logging.FileHandler("survey_app.log"), logging.StreamHandler()]
)
load_dotenv()
TOKEN = os.getenv("SM_TOKEN")
BASE_URL = "https://api.surveymonkey.com/v3"

app = Flask(__name__)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

@app.route('/create-survey', methods=['POST'])
def handle_request():
    data = request.json
    if not data:
        logging.warning("Received request with no JSON body.")
        return jsonify({"No JSON body found"})

    try:
        survey_name = list(data.keys())[0]
        page_name = list(data[survey_name].keys())[0]
        questions_dict = data[survey_name][page_name]
        logging.info(f"Starting creation for survey: {survey_name}")

        res = requests.post(f"{BASE_URL}/surveys", headers=HEADERS, json={"title": survey_name})
        res.raise_for_status() 
        survey_id = res.json()["id"]
        logging.info(f"Survey created ID: {survey_id}")

        res = requests.post(f"{BASE_URL}/surveys/{survey_id}/pages", headers=HEADERS, json={"title": page_name})
        page_id = res.json()["id"]
        logging.info(f"Page created  ID: {page_id}")

        for q_name, q_data in questions_dict.items():
            payload = {
                "family": "single_choice",
                "subtype": "vertical",
                "headings": [{"heading": q_data["Description"]}], 
                "answers": {"choices": [{"text": a} for a in q_data["Answers"]]}
            }
            requests.post(f"{BASE_URL}/surveys/{survey_id}/pages/{page_id}/questions", headers=HEADERS, json=payload)
        logging.info(f"Successfully added  questions")

        res = requests.post(f"{BASE_URL}/surveys/{survey_id}/collectors", headers=HEADERS, json={"type": "weblink"})
        survey_url = res.json().get("url")
        return jsonify({"survey_link": survey_url})

    except Exception as e:
        logging.error(f"Failed to create survey: {str(e)}")
        return jsonify({"server error during survey creation"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)