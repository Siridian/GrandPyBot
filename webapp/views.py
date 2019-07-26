from flask import Flask, render_template, request, jsonify
from webapp import parsinger


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/')
def search():
    question = request.args.get('question')
    return parsinger.parse(question)

if __name__ == "__main__":
    app.run()


