from flask import Flask, request, jsonify
import bot
from flask_cors import CORS, cross_origin

app= Flask(__name__)
CORS(app)

@app.route('/post_json', methods=['POST'])
@cross_origin(origin='*',methods=['GET','POST'])
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
