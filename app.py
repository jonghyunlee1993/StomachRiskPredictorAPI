from preprocessor import *
from model import predict
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/predict')
def main():
    verbosity = request.args.get('verbose', type=int)
    
    center = request.args.get('center')
    center = encode_center(center)
    age = request.args.get('age', type=int)
    gender = request.args.get('gender')
    gender = check_gender(gender)
    
    height = request.args.get('height', type=float)
    weight = request.args.get('weight', type=float)
    pain_nrs = request.args.get('pain_nrs', type=int)
    temperature = request.args.get('temperature', type=float)
    pulse = request.args.get('pulse', type=int)
    respiration = request.args.get('respiration', type=int)
    symtom = request.args.get('symtom')
    symtom = morph_text(symtom)
    encoded_symtom = encode_text(symtom)
    
    is_operation = request.args.get('is_operation', type=int)
    is_pain = request.args.get('is_pain', type=int)
    is_medical_history = request.args.get('is_medical_history', type=int)
    is_alertness = request.args.get('is_alertness', type=int)
    is_digestive = request.args.get('is_digestive', type=int)
    is_hemoptysis = request.args.get('is_hemoptysis', type=int)
    is_blood_excrement = request.args.get('is_blood_excrement', type=int)
    
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
    
    prob, pred = predict(encoded_symtom, meta)
    
    if verbosity == 1:
        return_data = {
            'prob': prob,
            'pred': pred, 
            'center': center,
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'pain_nrs': pain_nrs,
            'temperature': temperature,
            'pulse': pulse,
            'respiration': respiration,
            'symtom': symtom,
            'encoded_symtom': encoded_symtom,
            'is_operation': is_operation,
            'is_pain': is_pain,
            'is_medical_history': is_medical_history,
            'is_alertness': is_alertness, 
            'is_medical_history': is_medical_history,
            'is_alertness': is_alertness, 
            'is_digenstive': is_digestive,
            'is_hemoptysis': is_hemoptysis,
            'is_blood_excrement': is_blood_excrement,
            'bmi': bmi,
            'bmi_group': bmi_group,
            'is_temperature': is_temperature,
            'is_pulse': is_pulse,
            'is_respiration': is_respiration        
        }
    else:
        return_data = {
            'prob': prob,
            'pred': pred
        }
    
    return jsonify(return_data)

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port="16022")
    app.run(port="16022")