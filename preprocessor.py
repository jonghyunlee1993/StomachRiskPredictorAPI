import pickle
from konlpy.tag import Mecab
from py_hanspell.hanspell import spell_checker


def encode_center(center_string):
    center_dict = {
        '공군항공우주의료원': 0,
        '계룡대지구병원': 1,
        '국군수도병원': 2,
        '국군부산병원': 3,
        '국군함평병원': 4,
        '국군대구병원': 5,
        '해군해양의료원': 6,
        '국군대전병원': 7,
        '국군원주병원': 8,
        '국군구리병원': 9,
        '육군훈련지구병원': 10,
        '국군강릉병원': 11,
        '국군춘천병원': 12,
        '국군홍천병원': 13,
        '국군포천병원': 14,
        '국군양주병원': 15,
        '국군고양병원': 16,
        '해군포항병원': 17
    }
    
    return center_dict[center_string]

def check_gender(gender):
    if gender == "1" or "2":
        return int(gender)
    elif gender in ["M", "F"]:
        if gender == "M":
            return 1
        else:
            return 0

def morph_text(symtom):
    clean_text = spell_checker.check(symtom).as_dict()['checked']
    mecab = Mecab()
    morphs = mecab.pos(clean_text)
    morph = [morph[0] for morph in morphs]
    
    return morph

def encode_text(morph):
    with open("./data/vocab.pkl", "rb") as f:
        vocab_stoi = pickle.load(f)
    
    return [vocab_stoi[d] if d in vocab_stoi.keys() else vocab_stoi[''] for d in morph]
    

def calc_bmi(height, weight):
    return weight / ((height / 100) ** 2)

def get_bmi_group(bmi):
    if bmi < 25:
        bmi_group = 1
    elif bmi < 30:
        bmi_group = 2
    else:
        bmi_group = 3 
        
    return bmi_group

def get_temperature_flag(temperature):
    if temperature < 36 or temperature >= 38:
        is_temperature = 1
    else:
        is_temperature = 0
        
    return is_temperature

def get_pulse_flag(pulse):
    if pulse <= 100:
        is_pulse = 1
    else:
        is_pulse = 0
        
    return is_pulse

def get_respiration_flag(respiration):
    if respiration >= 20:
        is_respiration = 1
    else:
        is_respiration = 0
        
    return is_respiration