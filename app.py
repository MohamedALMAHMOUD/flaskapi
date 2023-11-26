from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd
from passeword import passeword

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize model artifact files. This will be loaded at the start of Flask model server.
lgbm = joblib.load(open("model_loans.joblib", "rb"))
features = joblib.load(open("features.joblib", "rb"))

# This structure will be used for JSON validation.
class Data:
    def __init__(self, SK_ID_CURR, YEARS_BIRTH, YEARS_EMPLOYED, ANNUITY_INCOME_PERC, EXT_SOURCE_2, AMT_CREDIT, AMT_ANNUITY, INSTAL_DPD_MEAN, INSTAL_AMT_PAYMENT_SUM):
        self.SK_ID_CURR = SK_ID_CURR
        self.YEARS_BIRTH = YEARS_BIRTH
        self.YEARS_EMPLOYED = YEARS_EMPLOYED
        self.ANNUITY_INCOME_PERC = ANNUITY_INCOME_PERC
        self.EXT_SOURCE_2 = EXT_SOURCE_2
        self.AMT_CREDIT = AMT_CREDIT
        self.AMT_ANNUITY = AMT_ANNUITY
        self.INSTAL_DPD_MEAN = INSTAL_DPD_MEAN
        self.INSTAL_AMT_PAYMENT_SUM = INSTAL_AMT_PAYMENT_SUM

@app.route('/doc')
@auto.doc()
def documentation():
    '''
    return API documentation page
    '''
    return auto.html()

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

# ML API endpoint for making prediction against the request received from the client
@app.route("/predict", methods=["POST"])
def predict():
    # Extract data from request
    data = request.get_json()
    data_obj = Data(**data)
    
    # Convert data to a DataFrame
    data_df = pd.DataFrame([data_obj.__dict__])

    # Select features required for making prediction
    data_df = data_df[features]

    # Create prediction
    proba = lgbm.predict_proba(data_df)[0][1]

    # Return response back to the client
    return jsonify({'proba': proba})

if __name__ == '__main__':
  app.run()
