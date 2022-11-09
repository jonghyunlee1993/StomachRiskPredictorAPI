import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras import layers as nn
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.sequence import pad_sequences

def define_model():
    RNN_model = Sequential([
        nn.Embedding(8080, 256, input_shape=(None,)), 
        nn.Bidirectional(nn.LSTM(256, return_sequences=True)),
        nn.Bidirectional(nn.LSTM(256, return_sequences=False)),
        nn.Dense(64, activation="relu")
    ])
    
    meta_model = Sequential([
        nn.Dense(32, activation='relu', input_shape=(21,)),
        nn.Dense(64, activation='relu')
    ])

    concated = nn.concatenate([RNN_model.output, meta_model.output])
    concated = nn.Dropout(0.1)(concated)
    concated = nn.Dense(64, activation='relu')(concated)
    concated = nn.Dense(32, activation='relu')(concated)
    concated = nn.Dense(1, activation='sigmoid')(concated)

    model = Model([RNN_model.input, meta_model.input], concated)

    return model

def predict(X_token, X_meta):   
    model = define_model()
    model = tf.keras.models.load_model("data/stomach_net.h5")
    model.compile(optimizer=Adam(lr=0.0005),
                  loss='binary_crossentropy',
                  metrics=['accuracy', tf.keras.metrics.AUC()])
    X_token = tf.expand_dims(tf.convert_to_tensor(X_token), axis=0)
    X_meta = tf.expand_dims(tf.convert_to_tensor(X_meta), axis=0)
    prob = tf.math.sigmoid(model.predict([X_token, X_meta]))[0][0].numpy()
    pred = 1 if prob >= 0.25 else 0
    
    return round(float(prob), 4), float(pred)