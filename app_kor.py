from preprocessor import *
from model import compute_risk
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
import googletrans

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

    return render_template('index_kor.html',
                           prediction_text=f"Probability: {round(float(prob), 4)}")

# @app.route('/predict')
# def main():
#     verbosity = request.args.get('verbose', type=int)
    
#     center = request.args.get('center')
#     center = encode_center(center)
#     age = request.args.get('age', type=int)
#     gender = request.args.get('gender')
#     gender = check_gender(gender)
    
#     height = request.args.get('height', type=float)
#     weight = request.args.get('weight', type=float)
#     pain_nrs = request.args.get('pain_nrs', type=int)
#     temperature = request.args.get('temperature', type=float)
#     pulse = request.args.get('pulse', type=int)
#     respiration = request.args.get('respiration', type=int)
#     symtom = request.args.get('symtom')
#     symtom = morph_text(symtom)
#     encoded_symtom = encode_text(symtom)
    
#     is_operation = request.args.get('is_operation', type=int)
#     is_pain = request.args.get('is_pain', type=int)
#     is_medical_history = request.args.get('is_medical_history', type=int)
#     is_alertness = request.args.get('is_alertness', type=int)
#     is_digestive = request.args.get('is_digestive', type=int)
#     is_hemoptysis = request.args.get('is_hemoptysis', type=int)
#     is_blood_excrement = request.args.get('is_blood_excrement', type=int)
    
#     bmi = calc_bmi(height, weight)
#     bmi_group = get_bmi_group(bmi)
#     is_temperature = get_temperature_flag(temperature)
#     is_pulse = get_pulse_flag(pulse)
#     is_respiration = get_respiration_flag(respiration)
    
#     meta = [center, age, gender, height, weight, bmi, bmi_group,
#             is_operation, is_pain, pain_nrs, is_medical_history, 
#             is_alertness, is_temperature, is_pulse, is_respiration, 
#             is_digestive, is_hemoptysis, is_blood_excrement, 
#             pulse, temperature, respiration]
    
#     prob = predict(encoded_symtom, meta)
    
#     if verbosity == 1:
#         return_data = {
#             'prob': prob,
#             'center': center,
#             'age': age,
#             'gender': gender,
#             'height': height,
#             'weight': weight,
#             'pain_nrs': pain_nrs,
#             'temperature': temperature,
#             'pulse': pulse,
#             'respiration': respiration,
#             'symtom': symtom,
#             'encoded_symtom': encoded_symtom,
#             'is_operation': is_operation,
#             'is_pain': is_pain,
#             'is_medical_history': is_medical_history,
#             'is_alertness': is_alertness, 
#             'is_medical_history': is_medical_history,
#             'is_alertness': is_alertness, 
#             'is_digenstive': is_digestive,
#             'is_hemoptysis': is_hemoptysis,
#             'is_blood_excrement': is_blood_excrement,
#             'bmi': bmi,
#             'bmi_group': bmi_group,
#             'is_temperature': is_temperature,
#             'is_pulse': is_pulse,
#             'is_respiration': is_respiration        
#         }
#     else:
#         return_data = {
#             'prob': prob
#         }
    
#     return jsonify(return_data)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(host="0.0.0.0", port="16022")
    app.run(debug=True, port="16022")