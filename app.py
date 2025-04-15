from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Load environment variables from .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a Flask application instance
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Serves chat UI

def ask_chatgpt(prompt):
    # Send API request to OpenAI ChatCompletion endpoint
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt} # Pass the user prompt
        ]
    )
    # Extract and return the response content from API result
    return response.choices[0].message.content


# Define an API route for /ask endpoint
@app.route("/ask", methods=["POST"])  # Only accepts POST requests
def chat():
    # Read the incoming JSON data (payload from user)
    data = request.json

    # Extract 'prompt' from the received JSON
    prompt = data.get("prompt", "")

    # If prompt is empty, return error
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Call the function to ask ChatGPT and get reply
    reply = ask_chatgpt(prompt)

    # Return the reply as a JSON response
    return jsonify({"reply": reply})


# Run the Flask application in development mode
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for easier troubleshooting