import json
import tensorflow as tf

from consts import INPUT, OUTPUT, WINDOW
from dto import PreparedData
import numpy as np
from utils import getXPrepared, getYPrepared
from sklearn.preprocessing import StandardScaler
import joblib
#from tensorflow.keras.callbacks import EarlyStopping

def studyData(preparedFileData, modelFile, skaledXFile, scaledYFile):
    print(tf.config.list_physical_devices('GPU'))
    preparedData: list[PreparedData]
    with open(preparedFileData, 'r', encoding='utf-8') as f:
        preparedData = [PreparedData(**item) for item in json.load(f)]
    print("len: ", len(preparedData))
    print("next open price [0]: ", preparedData[0].avgOpenNext)

    raw_X = np.array(getXPrepared(preparedData))
    raw_y = np.array(getYPrepared(preparedData))

    X = []
    y = []

    for i in range(len(raw_X) - WINDOW):
        X.append(raw_X[i:i+WINDOW])
        y.append(raw_y[i+WINDOW])

    X = np.array(X)
    y = np.array(y)

    print("X shape:", X.shape)  # (samples, 5, 11)
    print("y shape:", y.shape)  # (samples, 4)

    X_reshaped = X.reshape(-1, X.shape[2])
    scaler_X = StandardScaler()
    X_scaled = scaler_X.fit_transform(X_reshaped)
    X_scaled = X_scaled.reshape(X.shape)

    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y)

    model = tf.keras.Sequential([
    tf.keras.layers.LSTM(
        64,
        return_sequences=True,
        input_shape=(WINDOW, INPUT)
    ),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(OUTPUT, activation="linear")
])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="mse",
        metrics=["mae"]
    )

    model.summary()

    model.fit(
    X_scaled,
    y_scaled,
    epochs=20,
    batch_size=64,
    shuffle=False)

    """split = int(len(X_scaled) * 0.8)

    X_train, X_val = X_scaled[:split], X_scaled[split:]
    y_train, y_val = y_scaled[:split], y_scaled[split:]

    early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=7,
    restore_best_weights=True
    )

    model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=40,
    batch_size=64,
    callbacks=[early_stop],
    shuffle=False)"""

    model.save(modelFile)

    joblib.dump(scaler_X, skaledXFile)
    joblib.dump(scaler_y, scaledYFile)