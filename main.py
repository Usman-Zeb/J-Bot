from flask import Flask, request, jsonify
import bot

app= Flask(__name__)

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        message = json.get('prompt')
        return jsonify(bot.Chat(message))
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    bot.BotInitialize()
    app.run(debug=True)
