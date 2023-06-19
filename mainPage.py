import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
from lstm import Lstm

class main_page:
 
    def __init__(self):     
        self.root = ctk.CTk()      
        self.root.geometry("980x540")
        ctk.set_appearance_mode("Dark")

        self.title_label = ctk.CTkLabel(self.root, text="Agricultural Forecast Application", font= ('Montserrat', 24))
        self.title_label.pack(padx=10,pady=10)

        self.uploadcsv_label = ctk.CTkLabel(self.root, text= "Upload CSV", font = ('Montserrat', 18))
        self.uploadcsv_label.pack(padx=10, pady=10)

        self.csv_button = ctk.CTkButton(master= self.root, text= "search files...", width=120, height=25, command=self.load_data)
        self.csv_button.pack(padx=10, pady=10)

        self.plot_csv_label = ctk.CTkLabel(self.root, text= "Plot CSV", font = ('Montserrat', 18))
        self.plot_csv_label.pack(padx=10, pady=10)

        self.plot_csv_button = ctk.CTkButton(master= self.root, text= "plot csv", width=80, height=25, command=self.plot_csv)
        self.plot_csv_button.pack(padx=10, pady=10)

        self.train_lstm_label = ctk.CTkLabel(self.root, text= "Train LSTM", font = ('Montserrat', 18))
        self.train_lstm_label.pack(padx=10, pady=10)

        self.train_lstm_button = ctk.CTkButton(master= self.root, text= "train", width=80, height=25, command=self.train_lstm)
        self.train_lstm_button.pack(padx=10, pady=10)
        
        self.root.mainloop()

    def plot_csv(self):
        plt.plot(self.df["Fecha"], self.df["Frec"])
        plt.show()

    def convert_csv(self, file):
        df = pd.read_csv(file)
        return df

    def load_data(self):
        self.file = askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if self.file:
            self.df = self.convert_csv(self.file)
            self.df["Fecha"] = pd.to_datetime(self.df['Fecha'])
            self.df = self.df.groupby('Fecha')['Frec'].mean().reset_index()

    def train_lstm(self):
        self.lstm = Lstm(self.df)
        self.lstm.create_time_series()
        #self.lstm.test_plot_series()
        self.lstm.model_prediction()
        
        
mp = main_page()
    






