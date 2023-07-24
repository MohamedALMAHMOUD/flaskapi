from flask import Flask, render_template, jsonify, request
from passeword import passeword

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
  output = request.form.to_dict()
  mdp = output['mdp']
  resultat = passeword(mdp)
  return render_template('result.html', resultat=resultat)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"mdp": "resultat"}
    return jsonify(data)


if __name__ == '__main__':
  app.run()
