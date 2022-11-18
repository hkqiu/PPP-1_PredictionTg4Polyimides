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

        # style = ttk.Style()
        # style = ttk.Style(theme='sandstone') #想要切换主题，修改theme值即可，有以下这么多的主题，自己尝试吧：
        # ['vista', 'classic', 'cyborg', 'journal', 'darkly', 'flatly', 'clam', 
        # 'alt', 'solar', 'minty', 'litera', 'united', 'xpnative', 'pulse',
        # 'cosmo', 'lumen', 'yeti', 'superhero', 'winnative', 'sandstone', 'default']
        # TOP6 = style.master
        self.window = ttk.Window(
                    title=self.title,        #设置窗口的标题
                    themename="darkly",     #设置主题
                    # size=(1066,600),        #窗口的大小
                    # size=(1600,1200),        #窗口的大小
                    position=(100,100),     #窗口所在的位置
                    minsize=(0,0),          #窗口的最小宽高
                    maxsize=(1920,1080),    #窗口的最大宽高
                    resizable=None,         #设置窗口是否可以更改大小
                    alpha=1.0,              #设置窗口的透明度(0.0完全透明）
                    )

        # self.window = tk.Tk(className=self.title)

        # 获取文件路径
        self.url = tk.StringVar()

        # 变量（原播放源）
        self.n = tk.IntVar()
        self.n.set(1) # 默认1

        # Frame空间
        frame_1 = tk.Frame(self.window)
        frame_2 = tk.Frame(self.window)
        frame_3 = tk.Frame(self.window)

        # Menu菜单
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)# 在窗口添加菜单栏
        ComboBox = tk.Menu(menu,tearoff=0)
        menu.add_cascade(label='Links',menu=ComboBox) # 在菜单栏添加下拉菜单

        # 在下拉菜单添加各个网站链接
        # Lambda的使用: Lambda xx:xx 左边为定义,右边为执行语句
        ComboBox.add_command(label='Github', command=lambda: webbrowser.open('https://github.com/HKQiu/PPP-1_PredictionTg4Polyimides'))
        #         ComboBox.add_command(label='文章链接', command=lambda: webbrowser.open('https://github.com/HKQiu/ViscosityPredOfEpoxyResin/'))

        # 设置控件
        # frame1
        lab = tk.Label(frame_1,text='Choose one property to predict',padx=15,pady=15)
        channel1 = tk.Radiobutton(frame_1,text='Tg',variable=self.n,value=1,width=5,height=3)
        channel2 = tk.Radiobutton(frame_1,text='Coming soon...',variable=self.n,value=2,width=15,height=3)

        # frame_2
        lab1 = tk.Label(frame_2,text='The absolute path to the file: ')
        lab2 = tk.Label(frame_2,text='')
        lab3 = tk.Label(frame_2,text='')
        entry = tk.Entry(frame_2,textvariable=self.url,highlightcolor='Fuchsia',width=35)
        play = tk.Button(frame_2, text="Run", font=('Times New Roman', 12), fg='Purple', width=2, height=1, command=self.run)

        # frame_3
        label_explain = tk.Label(frame_3, fg='red', font=('Times New Roman', 14),
        #                                  text='Using GNN to predict polymer properties. \n Please close the window after "Run"!')
                                 text='Using GNN to predict polymer properties. \n ')
        # label_warning = tk.Label(frame_3, fg='blue', font=('楷体', 12), text='\nauthor: hkqiu\nqiuhaoke1999@163.com')

        # 控件布局
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
        # D:\0研究生\1聚酰亚胺\0PI\Tg模型\pred\0预测结果整合\5exp_smiles.csv
        MODEL_DIR = '/0研究生/1聚酰亚胺/0PI/GNN_model-R2=0.86/'

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
        # 禁止修改窗口大小
        self.window.resizable(False,False)
        # 窗口居中
        self.center()
        self.window.mainloop()
        pass
if __name__ == '__main__':
    app = PolyScreen()
    app.loop()
    if app.url.get() != '':
        app.predict_Tg()