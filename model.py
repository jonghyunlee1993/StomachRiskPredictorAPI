# import tensorflow as tf
# from tensorflow.keras import Model, Sequential
# from tensorflow.keras import layers as nn
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
# from tensorflow.keras.preprocessing.sequence import pad_sequences

# def define_model():
#     RNN_model = Sequential([
#         nn.Embedding(8080, 256, input_shape=(None,)), 
#         nn.Bidirectional(nn.LSTM(256, return_sequences=True)),
#         nn.Bidirectional(nn.LSTM(256, return_sequences=False)),
#         nn.Dense(64, activation="relu")
#     ])
    
#     meta_model = Sequential([
#         nn.Dense(32, activation='relu', input_shape=(21,)),
#         nn.Dense(64, activation='relu')
#     ])

#     concated = nn.concatenate([RNN_model.output, meta_model.output])
#     concated = nn.Dropout(0.1)(concated)
#     concated = nn.Dense(64, activation='relu')(concated)
#     concated = nn.Dense(32, activation='relu')(concated)
#     concated = nn.Dense(1, activation='sigmoid')(concated)

#     model = Model([RNN_model.input, meta_model.input], concated)

#     return model

# def compute_risk(X_token, X_meta):   
#     model = define_model()
#     model = tf.keras.models.load_model("data/stomach_net.h5")
#     model.compile(optimizer=Adam(lr=0.0005),
#                   loss='binary_crossentropy',
#                   metrics=['accuracy', tf.keras.metrics.AUC()])
#     X_token = tf.expand_dims(tf.convert_to_tensor(X_token), axis=0)
#     X_meta = tf.expand_dims(tf.convert_to_tensor(X_meta), axis=0)
#     prob = tf.math.sigmoid(model.predict([X_token, X_meta]))[0][0].numpy()
    
#     return round(float(prob), 4)

import pickle
import numpy as np

def compute_risk(X_token, X_meta):
    with open("data/counter_vectorizer.pkl", "rb") as f:
        counter_vectorizer = pickle.load(f)
    
    print(counter_vectorizer.transform([" ".join(X_token)]))
    X_token = counter_vectorizer.transform(X_token).toarray().tolist()
    
    X = X_meta + X_token[0]
    X = np.array(X).reshape(1, -1)
    
    with open("data/stomach_tree.pkl", "rb") as f:
        model = pickle.load(f)
        
    return model.predict_proba(X)[0][0]
        
        
def compute_meta_risk(x):
    risk = 0
    risk += x['pain_NRS'] * 0.1
    
    if x["temperature"] > 37 and x["temperature"] <= 38:
        risk += 0.3
    elif x["temperature"] > 38 and x["temperature"] <= 39:
        risk += 0.6
    else:
        risk += 1
    
    if x["pulse"] > 80 and x["pulse"] <= 90:
        risk += 0.3
    elif x["pulse"] > 90 and x["pulse"] <= 100:
        risk += 0.6
    elif x["pulse"] > 100:
        risk += 1
        
    if x["respiration"] > 16 and x["respiration"] <= 18:
        risk += 0.3
    elif x["respiration"] > 18 and x["respiration"] <= 20:
        risk += 0.6
    elif x["respiration"] > 20:
        risk += 1
        
    if x["is_operation"] == 1:
        risk += 0.3
        
    if x["is_medical_history"] == 1:
        risk += 0.3
        
    if x["is_alertness"] == 0:
        risk += 1
        
    if x["is_digestive"] == 1:
        risk += 0.3
        
    if x["is_hemoptysis"] == 1:
        risk += 0.5
        
    if x["is_bloody_excrement"] == 1:
        risk += 0.8
        
    if risk > 1:
        risk = 1
        
    return risk