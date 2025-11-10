from flask import Flask, render_template, request, jsonify
from chatbot import ChatbotKreyol
from database import Database

app = Flask(__name__)
chatbot = ChatbotKreyol()
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/produits')
def produits():
    produits_list = db.get_produits()
    return render_template('produits.html', produits=produits_list)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    message = request.json.get('message', '')
    result = chatbot.process_message(message)
    return jsonify(result)

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('q', '')
    produits = db.search_produits(query)
    return jsonify(produits)

if __name__ == '__main__':
    app.run(debug=True)
