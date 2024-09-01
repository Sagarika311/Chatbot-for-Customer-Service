import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify

app = Flask(__name__)

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
    faq_df.to_csv('faq_data.csv', index=False)
    print("FAQ data CSV file created successfully.")

# Load and preprocess the data
def load_and_preprocess_data():
    data = pd.read_csv('faq_data.csv')
    data['question'] = data['question'].str.lower()
    return data

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
    return data['answer'].iloc[closest_index]

@app.route('/')
def index():
    return "Welcome to the Chatbot! Use the /chat endpoint to interact with the chatbot."

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    response = get_response(user_input, vectorizer, X, data)
    return jsonify({'response': response})

if __name__ == '__main__':
    create_faq_data()
    data = load_and_preprocess_data()
    vectorizer, X = vectorize_data(data)
    app.run(debug=True)