from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from passeword import passeword

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://mohamedalmahmoud.github.io/portfolio/templates/competences.html"}})


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/check_password', methods=['POST'])
def check_password():
  data = request.json
  mdp = data.get('mdp')
  resultat = passeword(mdp)
  return jsonify({"resultat": resultat})

@app.route('/result', methods=['POST'])
def result():
  output = request.form.to_dict()
  mdp = output['mdp']
  resultat = passeword(mdp)
  return render_template('result.html', resultat=resultat)

if __name__ == '__main__':
  app.run()
