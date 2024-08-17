from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os
import json
import openai


app = Flask(__name__)


# Load environment variables from the .env.local file
load_dotenv(dotenv_path='.env.local')


# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Load the JSON file
json_file_path = os.path.join('data', 'ruby_hackathon_data.json')
with open(json_file_path, 'r') as file:
    json_data = json.load(file)


@app.route('/')
def home():
    return "Hello Flask with OpenAI & JSON!"


@app.route('/json-data')
def show_json_data():
    # Replace 'some_key' with an actual key from your JSON file
    some_data = json_data.get('some_key')
    return jsonify({"data": some_data})


@app.route('/analyze', methods=['POST'])
def analyze_complaint():
    data = request.json  # Get the JSON data from the request
    complaint_text = data.get('text')  # Extract the text from the JSON data
   
    if not complaint_text:
        return jsonify({"error": "No text provided"}), 400  # Return an error if no text is provided


    # Use OpenAI to analyze the text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Is the following text a complaint? If so, summarize it: {complaint_text}",
        max_tokens=50  # Limit the response length
    )
   
    # Extract the response text
    analysis = response.choices[0].text.strip()
   
    return jsonify({"analysis": analysis})  # Return the analysis as JSON


if __name__ == '__main__':
    app.run(debug=True)



