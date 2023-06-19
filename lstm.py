import numpy as np
from random import random
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow import keras

class Lstm:

    def __init__(self, _df) -> None:
        self.df_commodity = _df    
        self.precios = np.c_[self.df_commodity["Frec"]]
    
    def create_time_series(self):
        self.n_steps = 30
        self.X_precios = np.zeros((len(self.precios)-self.n_steps-1, self.n_steps, 1))
        self.y_precios = np.zeros((len(self.precios)-self.n_steps-1, 1))
        for i in range(len(self.precios)-self.n_steps-1):
            X_ejemplo = self.precios[i:i+self.n_steps]
            y_ejemplo = self.precios[i+self.n_steps]
            self.X_precios[i] = X_ejemplo
            self.y_precios[i] = y_ejemplo
        print(self.X_precios.shape, self.y_precios.shape)

    def plot_series(self, series, y=None, y_pred=None, x_label="$t$", y_label="$x(t)$", legend=True):
        plt.plot(series, ".-")
        if y is not None:
            plt.plot(self.n_steps, y, "bo", label="Target")
        if y_pred is not None:
            plt.plot(self.n_steps, y_pred, "rx", markersize=10, label="Prediction")
        plt.grid(True)
        if x_label:
            plt.xlabel(x_label, fontsize=16)
        if y_label:
            plt.ylabel(y_label, fontsize=16, rotation=0)
        plt.hlines(0, 0, 100, linewidth=1)
        plt.axis([0, self.n_steps + 1, 15, 150])
        if legend and (y or y_pred):
            plt.legend(fontsize=14, loc="upper left")
    
    def test_plot_series(self):
        fig, axes = plt.subplots(nrows=1, ncols=3, sharey=True, figsize=(12, 4))
        for col in range(3):
            plt.sca(axes[col])
            self.plot_series(self.X_precios[col, :, 0], self.y_precios[col, 0],
                y_label=("$x(t)$" if col==0 else None),
                legend=(col == 0))
        plt.show()

    def model_prediction(self):
        self.model = keras.models.load_model("modelo.h5")
        ejemplo = 38402
        y_pred = self.model.predict(self.X_precios)
        self.plot_series(self.X_precios[ejemplo, :, 0], self.y_precios[ejemplo, 0], y_pred[ejemplo, 0])
        plt.show()

    

    

