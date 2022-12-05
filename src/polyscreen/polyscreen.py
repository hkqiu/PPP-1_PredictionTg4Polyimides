import glob,os
import pandas as pd
import deepchem as dc
import numpy as np
import tensorflow as tf
import rdkit
import tkinter as tk
import tkinter.messagebox
import webbrowser
import re
import ttkbootstrap as ttk

class PolyScreen:
    def __init__(self,width=500,height=300):
        self.w = width
        self.h = height
        self.title = 'PolyScreen'

        self.window = ttk.Window(
                    title=self.title,       
                    themename="darkly",    
                    # size=(1066,600),       
                    # size=(1600,1200),       
                    position=(100,100),    
                    minsize=(0,0),          
                    maxsize=(1920,1080),  
                    resizable=None,         
                    alpha=1.0,            
                    )

        # self.window = tk.Tk(className=self.title)

        self.url = tk.StringVar()

        self.n = tk.IntVar()
        self.n.set(1) 

        frame_1 = tk.Frame(self.window)
        frame_2 = tk.Frame(self.window)
        frame_3 = tk.Frame(self.window)

        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        ComboBox = tk.Menu(menu,tearoff=0)
        menu.add_cascade(label='Links',menu=ComboBox) 

        ComboBox.add_command(label='Github', command=lambda: webbrowser.open('https://github.com/HKQiu/PPP-1_PredictionTg4Polyimides'))

        lab = tk.Label(frame_1,text='Choose one property to predict',padx=15,pady=15)
        channel1 = tk.Radiobutton(frame_1,text='Tg',variable=self.n,value=1,width=5,height=3)
        channel2 = tk.Radiobutton(frame_1,text='Coming soon...',variable=self.n,value=2,width=15,height=3)

        lab1 = tk.Label(frame_2,text='The absolute path to the file: ')
        lab2 = tk.Label(frame_2,text='')
        lab3 = tk.Label(frame_2,text='')
        entry = tk.Entry(frame_2,textvariable=self.url,highlightcolor='Fuchsia',width=35)
        play = tk.Button(frame_2, text="Run", font=('Times New Roman', 12), fg='Purple', width=2, height=1, command=self.run)

        label_explain = tk.Label(frame_3, fg='red', font=('Times New Roman', 14),
        #                                  text='Using GNN to predict polymer properties. \n Please close the window after "Run"!')
                                 text='Using GNN to predict polymer properties. \n ')

        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        lab.grid(row=0, column=0)
        channel1.grid(row=0, column=1)
        channel2.grid(row=0, column=2)
        lab1.grid(row=0, column=0)
        lab2.grid(row=0, column=2)
        lab3.grid(row=0, column=4)
        entry.grid(row=0, column=1)
        play.grid(row=0, column=3, ipadx=10, ipady=10)
        label_explain.grid(row=1, column=0,ipady=30)
        # label_warning.grid(row=2, column=0)

    def run(self):

        print("Filepath:", self.url.get())
        

    def center(self):
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (self.w / 2))
        y = int((hs / 2) - (self.h / 2))
        self.window.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))
    
    def predict_Tg(self):
        DATASET_FILE = self.url.get()
        MODEL_DIR = '../0PI/GNN_model-R2=0.86/'  # File path in my PC. Change this before using.

        featurizer = dc.feat.ConvMolFeaturizer()
        loader = dc.data.CSVLoader(tasks=[], feature_field="Smiles", featurizer=featurizer)
        testset = loader.create_dataset(DATASET_FILE, shard_size=10000)

        model = dc.models.GraphConvModel(1, mode="regression", model_dir=MODEL_DIR)
        model.restore()

        test_pred = model.predict(testset)
        res = pd.DataFrame(test_pred)
        res.columns = ['Pred']
        
        file_path = self.url.get()
        root_path = file_path.split('.', 1)[0]
        save_path = root_path + '_result.csv'
        res.to_csv(save_path)

    def loop(self):
        self.window.resizable(False,False)
        self.center()
        self.window.mainloop()
        pass
if __name__ == '__main__':
    app = PolyScreen()
    app.loop()
    if app.url.get() != '':
        app.predict_Tg()
