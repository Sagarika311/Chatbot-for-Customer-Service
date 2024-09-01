import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template_string
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO)

# Create the FAQ dataset and save it to a CSV file
def create_faq_data():
    faq_data = {
        "question": [
            "What are your business hours?",
            "How can I reset my password?",
            "What is your return policy?",
            "How do I contact customer support?",
            "Where can I find product information?",
            "Do you offer international shipping?",
            "How can I track my order?",
            "What payment methods do you accept?",
            "Can I change my order after it has been placed?",
            "How do I unsubscribe from the newsletter?"
        ],
        "answer": [
            "We are open from 9 AM to 5 PM, Monday to Friday.",
            "You can reset your password by clicking on 'Forgot Password' on the login page.",
            "Our return policy allows returns within 30 days of purchase.",
            "You can contact customer support via email at support@example.com or call us at 1-800-555-0199.",
            "Product information can be found on the product page on our website.",
            "Yes, we offer international shipping to select countries.",
            "You can track your order using the tracking link provided in your confirmation email.",
            "We accept Visa, MasterCard, American Express, and PayPal.",
            "Yes, you can change your order by contacting customer support before it ships.",
            "To unsubscribe, click the 'unsubscribe' link at the bottom of our emails."
        ]
    }

    faq_df = pd.DataFrame(faq_data)
    faq_df.to_csv('faq_data.csv', index=False, quoting=1)  # Use quoting to ensure proper CSV formatting
    logging.info("FAQ data CSV file created successfully.")

# Load and preprocess the data
def load_and_preprocess_data():
    try:
        # Try to read the CSV file
        data = pd.read_csv('faq_data.csv')
        # Check if the data has the expected columns
        if 'question' not in data.columns or 'answer' not in data.columns:
            raise ValueError("CSV file does not have the expected columns")
        data['question'] = data['question'].str.lower()
        return data
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as e:
        # If any error occurs, log it and create a new FAQ data file
        logging.error(f"Error loading FAQ data: {str(e)}. Creating a new one.")
        if os.path.exists('faq_data.csv'):
            os.remove('faq_data.csv')  # Remove the problematic file
        create_faq_data()
        return load_and_preprocess_data()  # Try loading again
# Perform NLP tasks
def vectorize_data(data):
    nltk.download('punkt', quiet=True)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data['question'])
    return vectorizer, X

# Implement the chatbot logic
def get_response(user_input, vectorizer, X, data):
    user_input_vector = vectorizer.transform([user_input.lower()])
    similarities = cosine_similarity(user_input_vector, X)
    closest_index = similarities.argmax()
    confidence = similarities[0][closest_index]
    
    if confidence > 0.5:
        return data['answer'].iloc[closest_index], confidence
    else:
        return "I'm sorry, I don't have enough information to answer that question accurately. Can you please rephrase or ask something else?", confidence

# HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Chatbot</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 400px;
            max-width: 100%;
        }
        .chat-header {
            background-color: #4a69bd;
            color: #ffffff;
            padding: 20px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-size: 1.2em;
            font-weight: bold;
        }
        #chatbox {
            height: 400px;
            overflow-y: scroll;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        .message {
            max-width: 80%;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 20px;
            line-height: 1.4;
        }
        .user-message {
            align-self: flex-end;
            background-color: #0084ff;
            color: #ffffff;
        }
        .bot-message {
            align-self: flex-start;
            background-color: #e4e6eb;
            color: #050505;
        }
        .input-area {
            display: flex;
            padding: 20px;
            border-top: 1px solid #e4e6eb;
        }
        #user_input {
            flex-grow: 1;
            padding: 10px 15px;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            background-color: #f0f2f5;
        }
        #send_button {
            background-color: #4a69bd;
            color: #ffffff;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            margin-left: 10px;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #send_button:hover {
            background-color: #3c5aa6;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">Interactive Chatbot</div>
        <div id="chatbox"></div>
        <div class="input-area">
            <input type="text" id="user_input" placeholder="Type your message here...">
            <button id="send_button">➤</button>
        </div>
    </div>

    <script>
        function addMessage(sender, message) {
            const messageDiv = $("<div>").addClass("message").text(message);
            if (sender === "You") {
                messageDiv.addClass("user-message");
            } else {
                messageDiv.addClass("bot-message");
            }
            $("#chatbox").append(messageDiv);
            $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
        }

        $("#send_button").click(function() {
            var user_input = $("#user_input").val();
            if (user_input.trim() !== "") {
                addMessage("You", user_input);
                $.ajax({
                    url: "/chat",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({"message": user_input}),
                    success: function(response) {
                        addMessage("Bot", response.response);
                    }
                });
                $("#user_input").val("");
            }
        });

        $("#user_input").keypress(function(e) {
            if (e.which == 13) {
                $("#send_button").click();
            }
        });

        addMessage("Bot", "Hello! How can I assist you today?");
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    response, confidence = get_response(user_input, vectorizer, X, data)
    
    # Log the interaction
    logging.info(f"User: {user_input}")
    logging.info(f"Bot: {response} (confidence: {confidence:.2f})")
    
    return jsonify({'response': response})

if __name__ == '__main__':
    data = load_and_preprocess_data()
    vectorizer, X = vectorize_data(data)
    app.run(debug=True)