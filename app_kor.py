from preprocessor import *
from model import compute_risk
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)

def compute_meta_risk(pain_nrs, temperature, pulse, respiration, 
                      is_operation, is_medical_history, is_alertness, 
                      is_digestive, is_hemoptysis, is_blood_excrement):
    risk = 0
    risk += pain_nrs * 0.1
    
    if temperature > 37 and temperature <= 38:
        risk += 0.3
    elif temperature > 38 and temperature <= 39:
        risk += 0.6
    elif temperature > 39:
        risk += 1
    
    if pulse > 80 and pulse <= 90:
        risk += 0.3
    elif pulse > 90 and pulse <= 100:
        risk += 0.6
    elif pulse > 100:
        risk += 1
        
    if respiration > 16 and respiration <= 18:
        risk += 0.3
    elif respiration > 18 and respiration <= 20:
        risk += 0.6
    elif respiration > 20:
        risk += 1
        
    if is_operation == 1:
        risk += 0.3
        
    if is_medical_history == 1:
        risk += 0.3
        
    if is_alertness == 0:
        risk += 1
        
    if is_digestive == 1:
        risk += 0.3
        
    if is_hemoptysis == 1:
        risk += 0.5
        
    if is_blood_excrement == 1:
        risk += 0.8
        
    if risk > 1:
        risk = 1
        
    return risk

app = Flask(__name__)

@app.route("/")
def idle():
    return render_template('index_kor.html')

@app.route("/", methods=['POST'])
def predict():
    # translator = googletrans.Translator()
    center = "국군수도병원"
    center = encode_center(center)
    age = int(request.form['age'])
    gender = request.form['gender']
    gender = check_gender(gender)
    
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    pain_nrs = int(request.form['pain_nrs'])
    temperature = float(request.form['temperature'])
    pulse = int(request.form['pulse'])
    respiration = int(request.form['respiration'])
    symtom = request.form['symtom']
    # symtom = translator.translate(symtom, dest="ko").text
    symtom = morph_text(symtom)
    # encoded_symtom = encode_text(symtom)
    
    is_operation = int(request.form['is_operation'])
    is_pain = int(request.form['is_pain'])
    is_medical_history = int(request.form['is_medical_history'])
    is_alertness = int(request.form['is_alertness'])
    is_digestive = int(request.form['is_digestive'])
    is_hemoptysis = int(request.form['is_hemoptysis'])
    is_blood_excrement = int(request.form['is_blood_excrement'])
    
    bmi = calc_bmi(height, weight)
    bmi_group = get_bmi_group(bmi)
    is_temperature = get_temperature_flag(temperature)
    is_pulse = get_pulse_flag(pulse)
    is_respiration = get_respiration_flag(respiration)
    
    meta = [center, age, gender, height, weight, bmi, bmi_group,
            is_operation, is_pain, pain_nrs, is_medical_history, 
            is_alertness, is_temperature, is_pulse, is_respiration, 
            is_digestive, is_hemoptysis, is_blood_excrement, 
            pulse, temperature, respiration]
    
    prob = compute_risk(symtom, meta)

    meta_risk = compute_meta_risk(pain_nrs, temperature, pulse, respiration, 
                      is_operation, is_medical_history, is_alertness, 
                      is_digestive, is_hemoptysis, is_blood_excrement)
    
    final_prob = (prob + meta_risk) / 2

    return render_template('index_kor.html',
                           prediction_text=f"Probability: {round(float(final_prob), 4)}")

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(host="0.0.0.0", port="16022")
    app.run(debug=True, port="16022")