import json
import tensorflow as tf

from consts import INPUT, OUTPUT, WINDOW
from dto import PreparedData
import numpy as np
from utils import getXPrepared, getYPrepared
from sklearn.preprocessing import StandardScaler
import joblib


def studyData(preparedFileData, modelFile, skaledXFile, scaledYFile):
    print(tf.config.list_physical_devices('GPU'))

    preparedData: list[PreparedData]
    with open(preparedFileData, 'r', encoding='utf-8') as f:
        preparedData = [PreparedData(**item) for item in json.load(f)]

    print("len:", len(preparedData))
    print("next open delta [0]:", preparedData[0].avgOpenNext)

    raw_X = np.array(getXPrepared(preparedData))  # (N, INPUT)
    raw_y = np.array(getYPrepared(preparedData))  # (N, OUTPUT)

    X = []
    y = []

    for i in range(len(raw_X) - WINDOW):
        X.append(raw_X[i:i + WINDOW])
        y.append(raw_y[i + WINDOW])

    X = np.array(X)  # (samples, WINDOW, INPUT)
    y = np.array(y)  # (samples, OUTPUT)

    print("X shape:", X.shape)
    print("y shape:", y.shape)

    # ===== Scaling X =====
    X_reshaped = X.reshape(-1, X.shape[2])
    scaler_X = StandardScaler()
    X_scaled = scaler_X.fit_transform(X_reshaped)
    X_scaled = X_scaled.reshape(X.shape)

    # ===== Scaling y =====
    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y)

    # ===== MODEL (GRU) =====
    model = tf.keras.Sequential([
        tf.keras.layers.GRU(
            64,
            return_sequences=True,
            input_shape=(WINDOW, INPUT)
        ),
        tf.keras.layers.Dropout(0.2),

        tf.keras.layers.GRU(64),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(OUTPUT, activation="linear")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss=tf.keras.losses.Huber(delta=1.0),
        metrics=["mae"]
    )

    model.summary()

    # ===== TRAIN =====
    model.fit(
        X_scaled,
        y_scaled,
        epochs=20,
        batch_size=64,
        shuffle=False
    )

    # ===== SAVE =====
    model.save(modelFile)
    joblib.dump(scaler_X, skaledXFile)
    joblib.dump(scaler_y, scaledYFile)
