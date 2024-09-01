from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Chatbot! Use the /chat endpoint to interact with the chatbot."

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_response(user_input)
    return jsonify({'response': response})

def get_response(user_input):
    # Implement your chatbot logic here
    return "This is a test response."

if __name__ == '__main__':
    app.run(debug=True)