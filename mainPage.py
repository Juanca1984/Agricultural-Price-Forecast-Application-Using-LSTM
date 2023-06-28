import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename
from lstm import Lstm
from os import listdir

class main_page():
 
    def __init__(self): 

        #initiate the root of the gui

        self.root = ctk.CTk()      
        self.root.geometry("1100x580")
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        ctk.set_appearance_mode("Dark")

        self.dataframe_directory = "dataframes"

        #initiate all the frames of the page

        self.create_sidebar_frame()
        self.create_main_page_frame()
        self.create_dataframe_choose_frame()
        self.create_graph_properties_frame()
        self.create_graph_frame()        

        #self.train_lstm_label = ctk.CTkLabel(self.root, text= "Train LSTM", font = ('Montserrat', 18))
        #self.train_lstm_label.pack(padx=10, pady=10)

        #self.train_lstm_button = ctk.CTkButton(master= self.root, text= "train", width=80, height=25, command=self.train_lstm)
        #self.train_lstm_button.pack(padx=10, pady=10)
        
        self.root.mainloop()


    def create_sidebar_frame(self):
        self.sidebar_frame = ctk.CTkFrame(self.root, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


    def create_main_page_frame(self):
        self.mainpage_frame = ctk.CTkFrame(self.root, width=960, height=580)
        self.mainpage_frame.grid(row=0, column=1,sticky="nsew")
        self.mainpage_frame.grid_columnconfigure(0, weight=1, minsize=180)
        self.mainpage_frame.grid_columnconfigure(2, weight=2)  # Allow the row containing the graph to expand
        self.mainpage_frame.grid_rowconfigure(0, weight=1)
        self.mainpage_frame.grid_rowconfigure(1, weight=1)
        self.mainpage_frame.grid_rowconfigure(2, weight=1)
        self.mainpage_frame.grid_rowconfigure(3, weight=1)

        #creating the title label for the page in the mainpage_frame

        self.title_label = ctk.CTkLabel(self.mainpage_frame, text="Agricultural Forecast Application", 
                                        font= ('Montserrat', 24), anchor='center')
        self.title_label.grid(row=0, column=0, pady=10, sticky= "ew", columnspan=3)


    def create_dataframe_choose_frame(self):
        self.dataframe_choose_frame = ctk.CTkFrame(self.mainpage_frame, width=200)
        self.dataframe_choose_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.dataframe_choose_frame.grid_columnconfigure(0, weight=1)
        self.dataframe_choose_frame.grid_columnconfigure(1, weight=1)
        self.dataframe_choose_frame.grid_rowconfigure(1, weight=1)

        self.choose_ap_label = ctk.CTkLabel(self.dataframe_choose_frame, text = "Choose agricultural product", 
                                            font = ('Montserrat', 16), anchor='center')
        self.choose_ap_label.grid(row=0, column=0, pady=10, padx=0, sticky= "nsew")

        self.csv_dropdown_optionmenu_var = ctk.StringVar(value="aguacate_hass_primera_2012-2022.csv")
        self.csv_dropdown_optionmenu = ctk.CTkOptionMenu(self.dataframe_choose_frame, 
                                                         values = self.get_dataframe_names(), 
                                                         command=self.load_data, variable=self.csv_dropdown_optionmenu_var,
                                                         width=180, anchor='center')                                  
        self.csv_dropdown_optionmenu.grid(row = 1,column=0, padx=10, pady=10)


    def create_graph_properties_frame(self):
        self.graph_properties_frame = ctk.CTkFrame(self.mainpage_frame, width=300)
        self.graph_properties_frame.grid(row=2, column=0, padx=10,pady=10,sticky="nsew", rowspan=2)
        self.graph_properties_frame.grid_columnconfigure(0, weight=1)
        self.graph_properties_frame.grid_columnconfigure(1, weight=1)

        self.select_graph_properties_label = ctk.CTkLabel(self.graph_properties_frame,
                                                           text="Select graph properties", font= ('Montserrat', 16))
        self.select_graph_properties_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.min_checkbox_var = ctk.StringVar(value = "off")
        self.min_checkbox = ctk.CTkCheckBox(self.graph_properties_frame, text="Min",
                                            command=lambda: self.plot_csv(self.min_checkbox_var.get()),
                                            variable=self.min_checkbox_var, onvalue="Min", offvalue="off")
        self.min_checkbox.grid(row=1,column=0,padx=10,pady=10)

        self.max_checkbox_var = ctk.StringVar(value="off")
        self.max_checkbox = ctk.CTkCheckBox(self.graph_properties_frame, text= "Max", 
                                            command=lambda: self.plot_csv(self.max_checkbox_var.get()),
                                            variable=self.max_checkbox_var, onvalue="Max", offvalue="off")
        self.max_checkbox.grid(row=2,column=0,padx=0,pady=10)

        self.frec_checkbox_var = ctk.StringVar(value="off")
        self.frec_checkbox = ctk.CTkCheckBox(self.graph_properties_frame, text= "Frec", 
                                            command=lambda: self.plot_csv(self.frec_checkbox_var.get()),
                                                variable=self.frec_checkbox_var, onvalue="Frec", offvalue="off")
        self.frec_checkbox.grid(row=3,column=0,padx=0,pady=10)

        self.smooth_min_checkbox_var = ctk.StringVar(value="off")
        self.smooth_min_checkbox = ctk.CTkCheckBox(self.graph_properties_frame, text= "Smooth Min", 
                                            command=lambda: self.smooth_graph(self.smooth_min_checkbox.get()),
                                                variable=self.smooth_min_checkbox_var, onvalue="Min", offvalue="off")
        self.smooth_min_checkbox.grid(row=1,column=1,padx=10,pady=10)

        
    def create_graph_frame(self):
        self.graph_frame = ctk.CTkFrame(self.mainpage_frame, width=800)
        self.graph_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew',rowspan=3, columnspan=2)
        self.graph_frame.grid_columnconfigure(1, weight=3)  
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(2, weight=1)
        print(str(self.graph_frame.size()))

        self.create_graph()


    def create_graph(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)  
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    
    def load_data(self, filename):
        self.df = pd.read_csv(f"dataframes/{filename}")
        self.df["Fecha"] = pd.to_datetime(self.df['Fecha'])


    def plot_csv(self, price_column):
        self.ax.plot(self.df["Fecha"], self.df[price_column])
        self.canvas.draw()

    def smooth_graph(self, smoothparameter):
        N = 100

        self.df['Smooth'] = self.df[smoothparameter].rolling(window=N).mean()
        plt.plot(self.df['Fecha'], self.df['Smooth'])

    def get_dataframe_names(self)->list:
        return listdir(self.dataframe_directory)
    

    def convert_csv(self, file):
        df = pd.read_csv(file)
        return df
    

    def train_lstm(self):
        self.lstm = Lstm(self.df)
        self.lstm.create_time_series()
        #self.lstm.test_plot_series()
        self.lstm.model_prediction()
        
        
mp = main_page()
    






