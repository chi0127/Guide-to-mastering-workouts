import tkinter as tk
from tkinter import ttk
#from tkcalendar import Calendar
from tkcalendar import DateEntry
import tkinter.font as tkFont
import dataBase as db
import datetime
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
#
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties #中文字包
from matplotlib.pyplot import MultipleLocator
import numpy as np
import pandas as pd
#隨視窗的滾輪製作參考https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame

from main import GoogleAPIClient
from all_main import Main_data
from googleSheet import GoogleSheets
import pandas as pd


class Aanalyses(tk.Frame):
    todayYear=str(datetime.datetime.now().strftime('%Y-%m-%d')).split('-')[0]
    todayMonth=str(datetime.datetime.now().strftime('%Y-%m-%d')).split('-')[1]
    todayDay=str(datetime.datetime.now().strftime('%Y-%m-%d')).split('-')[2]
    todayWeek=datetime.datetime.now().weekday()
    dateRangeLabel=""
    selectDateLabe2=""
    selectTotalSqu = 0
    selectTotalBri = 0
    selectTotalLun = 0
    selectTotalCa = 0
    monthTotalDay={"1":31,"2":28,"3":31,"4":30,"5":31,"6":30,"7":31,"8":31,"9":30,"10":31,"11":30,"12":31}
    weekCh={1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"日"}
    
    
    def __init__(self,root,user):
        tk.Frame.__init__(self, root)
        #root.destroy()
        self.user=user
        self.analyses_top = tk.Toplevel(root)
        self.analyses_top.title(f'健體端勢【分析結果】- {user}')
        #ttk.Label(analyses_top,text="top").grid(row=1,column=1)
        
        default_font = tkFont.nametofont("TkDefaultFont")  #改原本預設的字型
        default_font.configure(family='Helvetica', size=15)
        
        canvas=tk.Canvas(self.analyses_top,width=200,height=180, bg="yellow",scrollregion=(0,0,520,0)) #創建canvas
        canvas.grid(column=1,row=0, rowspan=3) #放置canvas的位置 ,rowspan=5,columnspan=5
        #中文字包設定
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
        plt.rcParams['axes.unicode_minus'] = False
        
        yearRes=ttk.Button(self.analyses_top, text="年分析",command=self.yearSearch)
        yearRes.grid(row=0,column=0, padx=40, pady=20)
        monthRes=ttk.Button(self.analyses_top, text="月分析",command=self.monthSearch)
        monthRes.grid(row=1,column=0, padx=40, pady=20)
        weekRes=ttk.Button(self.analyses_top, text="周分析",command=self.weekSearch)
        weekRes.grid(row=2,column=0, padx=40, pady=20)

        frame=tk.Frame(canvas) #把frame放在canvas裏
        frame.grid(column=1, row=0, rowspan=3) #frame的長寬，和canvas差不多的,rowspan=5,columnspan=5

    def yearSearch(self):
        analyses_top2 = tk.Toplevel(self.analyses_top)
        analyses_top2.title(f'健體端勢【年分析結果】- {self.user}')
        def search():
            data={"month":[],"深蹲":[],"臀橋":[],"弓步蹲":[],"熱量":[]}
            year=entryY.get()
            
            self.userinfo_database = Main_data()
            self.onlyuser_database = GoogleSheets()
            self.user_email = self.userinfo_database.get_user_info()
            
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )
            
            try:
                y=int(year)
                msg["text"]=""
            except:
                msg["text"]="*請輸入有效數值!"
                return
            self.year_search = self.userinfo_database.get_year_times(
                spreadsheetId=self.user_sheetId,
                sheet_range='工作表1',
                year = str(year),
                )
            
            # prepare data
            f = Figure(figsize=(11, 4), dpi=100)
            f.patch.set_facecolor('#333333') #圖紙的背景顏色
            f_plot = f.add_subplot(111)
            f_plot.clear()
            if self.year_search != False:
                res = self.year_search
                for i in range(len(res)):
                    month=res[i][0]
                    squat=res[i][1]
                    bridge=res[i][2]
                    lunge=res[i][3]
                    cal=Decimal(Decimal(0.32) * squat + Decimal(0.3) * bridge + Decimal(0.5) * lunge).quantize(Decimal('.00'), ROUND_HALF_UP)
                    data["month"].append(month)
                    data["深蹲"].append(int(squat))
                    data["臀橋"].append(int(bridge))
                    data["弓步蹲"].append(int(lunge))
                    data["熱量"].append(float(cal))
                        
                #圖表                
                m1_t = pd.DataFrame(data)
                #長條圖製作
                bar = m1_t[['深蹲','臀橋','弓步蹲']].plot(kind='bar', width = .45, stacked=True,ax=f_plot,color=["#96ceb4","#ffad60","#d9534f"])
                #折線圖製作
                #bar.tick_params(axis = 'y', labelcolor = 'r')
                line = m1_t["熱量"].plot(secondary_y=True, color='#ffeead',ax=f_plot)
                #日期設定
                f_plot.set_xticklabels( [str(d)+"月" for d in m1_t['month']], color='white' )
                
            else:
                f_plot.axis('off') #移除原本預設xy軸的刻度                
                data={"month":[i for i in range(1, 13)],"深蹲":[0]*12,"臀橋":[0]*12,"弓步蹲":[0]*12,"熱量":[0]*12}
                f_plot = f.add_subplot(111)
                m1_t = pd.DataFrame(data)
                bar = m1_t[['深蹲','臀橋','弓步蹲']].plot(kind='bar', width = .45, stacked=True,ax=f_plot,color=["#96ceb4","#ffad60","#d9534f"])
                line = m1_t["熱量"].plot(secondary_y=True, color='#ffeead',ax=f_plot)
                line.set_ylim(0,100)
                #日期設定
                f_plot.set_xticklabels( [str(d)+"月" for d in m1_t['month']], color='white' )
                f_plot.set_ylim(0,100)
            
            #長條圖設定
            bar.set_facecolor("#333333")
            leg = bar.legend()
            #轉成直向文字
            labelRightTxt="次數"
            labelRightTxt_vtc=""
            for i in range(len(labelRightTxt)):
                labelRightTxt_vtc+=labelRightTxt[i]+"\n"
            bar.set_ylabel(labelRightTxt_vtc, fontsize="14", rotation="horizontal", horizontalalignment="right", verticalalignment="bottom",color="white")#, loc="TOP"
            #plt.ylabel(“數量”, fontsize=”14", rotation=360, horizontalalignment=’right’, verticalalignment=’top’)
            bar.tick_params(axis = 'y', colors = 'white')
            bar.set_xlim(-0.55)
            bar.set_ylim(0)
            
            #折線圖設定
            line.spines[:].set_color("white") #外邊框顏色
            leg2 = line.legend()
            #轉成直向文字
            labelRightTxt="熱量"
            labelRightTxt_vtc=""
            for i in range(len(labelRightTxt)):
                labelRightTxt_vtc+=labelRightTxt[i]+"\n"
            line.set_ylabel(labelRightTxt_vtc, color='yellow', fontsize="14", rotation="horizontal", horizontalalignment="left", verticalalignment="bottom")#, loc="TOP"
            #plt.ylabel(“數量”, fontsize=”14", rotation=360, horizontalalignment=’right’, verticalalignment=’top’)
            line.tick_params(axis = 'y', colors = 'yellow')
            line.set_xlim(-0.55)
            line.set_ylim(0)
            #line.yaxis.set_major_locator(MultipleLocator(20))
            #顯示熱量數值
            for i in range(len(data["month"])): #bar上的值
                if data["熱量"][i]!=0.0:
                    line.text(i, data["熱量"][i], data["熱量"][i], size=9, ha = 'center',va='bottom',color="yellow")
                    #print(data["熱量"][i])
            
            #圖標設定
            f_plot.tick_params(axis = 'x', colors = 'white')
            
            #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.07),ncol=3, fancybox=True, shadow=True)
            f_plot.legend(leg.get_patches()+leg2.get_lines(), 
                       [text.get_text() for text in leg.get_texts()+leg2.get_texts()], 
                       loc='upper left', fancybox=True, framealpha=1, shadow=True, borderpad=1, fontsize=11, bbox_to_anchor=(1.1, 0.5),facecolor="#272727",labelcolor='linecolor')
            leg2.remove()
            
            f_plot.grid(linestyle='dotted',linewidth =1, color= 'gray',alpha = 0.4) #網格
            #畫出圖表空間
            canvs = FigureCanvasTkAgg(f, analyses_top2)
            #canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #create the toolbar
            toolFrame=ttk.Frame(analyses_top2)
            toolFrame.grid(row=2,column=0,sticky="w",padx=150)
            toolbar=NavigationToolbar2Tk(canvs, toolFrame)
            for button in toolbar.winfo_children():
                button.config(background="#737373")

            f_plot.set_title(f"{year}年  —  年紀錄",color="white")
            f.subplots_adjust(right=0.7)
            
            #canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            canvs.get_tk_widget().grid(row=1,column=0,columnspan=4)
                
        #條件按鈕建立
        selectFrame=ttk.Frame(analyses_top2)
        labelY = ttk.Label(selectFrame, text="年份",anchor=tk.CENTER)
        entryY = ttk.Entry(selectFrame,width=10)
        searchBt = ttk.Button(selectFrame, text="查詢",command=search)
        msg=ttk.Label(selectFrame, text='')
        selectFrame.grid(row=0,column=0,sticky="w",padx=150,pady=7)
        labelY.grid(row=0,column=1,sticky="e")
        entryY.grid(row=0,column=2,padx=30,pady=7,sticky="w")
        searchBt.grid(row=0,column=3,padx=40,pady=7)
        msg.grid(row=0,column=4,padx=15,pady=7)
        entryY.insert(0, int(self.todayYear))
        search()

    def monthSearch(self):
        self.analyses_top2 = tk.Toplevel(self.analyses_top)
        self.analyses_top2.title(f'健體端勢【月分析結果】- {self.user}')
        def search():
            data={"date":[],"深蹲":[],"臀橋":[],"弓步蹲":[],"熱量":[]}
            year=entryY.get()
            month=entryM.get()
            
            self.userinfo_database = Main_data()
            self.onlyuser_database = GoogleSheets()
            self.user_email = self.userinfo_database.get_user_info()
            
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )
            
            try:
                y=int(year)
                m=int(month)
                if int(m) in range(1,13): msg["text"]=""
                else:
                    msg["text"]="*請輸入有效數值!"
                    return
            except:
                msg["text"]="*請輸入有效數值!"
                return
            
            self.month_search = self.userinfo_database.get_month_times(
                spreadsheetId=self.user_sheetId,
                sheet_range='工作表1',
                year = str(year),
                month = str(month)
                )
            
            # prepare data
            f = Figure(figsize=(11, 4), dpi=100)
            f.patch.set_facecolor('#333333') #圖紙的背景顏色
            f_plot = f.add_subplot(111)
            f_plot.clear()
            if self.month_search != False:
                res = self.month_search
                for i in range(len(res)):
                    date=res[i][0]
                    squat=res[i][1]
                    bridge=res[i][2]
                    lunge=res[i][3]
                    cal=Decimal(0.32 * squat).quantize(Decimal('.00'), ROUND_HALF_UP)+Decimal(0.3 * bridge).quantize(Decimal('.00'), ROUND_HALF_UP)+Decimal(0.5 * lunge).quantize(Decimal('.00'), ROUND_HALF_UP)
                    #print(f"{cal}")
                    #cal=squat*0.32+bridge*0.3+lunge*0.5
                    data["date"].append(date)
                    data["深蹲"].append(int(squat))
                    data["臀橋"].append(int(bridge))
                    data["弓步蹲"].append(int(lunge))
                    data["熱量"].append(float(cal))
                        
                #圖表                
                m1_t = pd.DataFrame(data)
                #長條圖製作
                bar = m1_t[['深蹲','臀橋','弓步蹲']].plot(kind='bar', width = .45, stacked=True,ax=f_plot,color=["#96ceb4","#ffad60","#d9534f"])
                #折線圖製作
                #bar.tick_params(axis = 'y', labelcolor = 'r')
                line = m1_t["熱量"].plot(secondary_y=True, color='#ffeead',ax=f_plot)
                #日期設定
                #ax = plt.gca()
                #plt.xlim([-width, len(m1_t['normal'])-width])
                f_plot.set_xticklabels( [int(d) for d in m1_t['date']], color='white' )
                
            else:
                f_plot.axis('off') #移除原本預設xy軸的刻度                
                data={"date":[i for i in range(1, self.monthTotalDay[str(int(month))]+1)],"深蹲":[0]*self.monthTotalDay[str(int(month))],"臀橋":[0]*self.monthTotalDay[str(int(month))],"弓步蹲":[0]*self.monthTotalDay[str(int(month))],"熱量":[0]*self.monthTotalDay[str(int(month))]}
                #print(data["date"])
                f_plot = f.add_subplot(111)
                m1_t = pd.DataFrame(data)
                bar = m1_t[['深蹲','臀橋','弓步蹲']].plot(kind='bar', width = .45, stacked=True,ax=f_plot,color=["#96ceb4","#ffad60","#d9534f"])
                line = m1_t["熱量"].plot(secondary_y=True, color='#ffeead',ax=f_plot)
                line.set_ylim(0,100)
                #日期設定
                f_plot.set_xticklabels( [int(d) for d in m1_t['date']], color='white' )
                f_plot.set_ylim(0,100)
            
            #長條圖設定
            bar.set_facecolor("#333333")
            leg = bar.legend()
            #轉成直向文字
            labelRightTxt="次數"
            labelRightTxt_vtc=""
            for i in range(len(labelRightTxt)):
                labelRightTxt_vtc+=labelRightTxt[i]+"\n"
            bar.set_ylabel(labelRightTxt_vtc, fontsize="14", rotation="horizontal", horizontalalignment="right", verticalalignment="bottom",color="white")#, loc="TOP"
            #plt.ylabel(“數量”, fontsize=”14", rotation=360, horizontalalignment=’right’, verticalalignment=’top’)
            bar.tick_params(axis = 'y', colors = 'white')
            bar.set_xlim(-0.55)
            bar.set_ylim(0)
            
            #折線圖設定
            line.spines[:].set_color("white") #外邊框顏色
            leg2 = line.legend()
            #轉成直向文字
            labelRightTxt="熱量"
            labelRightTxt_vtc=""
            for i in range(len(labelRightTxt)):
                labelRightTxt_vtc+=labelRightTxt[i]+"\n"
            line.set_ylabel(labelRightTxt_vtc, color='yellow', fontsize="14", rotation="horizontal", horizontalalignment="left", verticalalignment="bottom")#, loc="TOP"
            #plt.ylabel(“數量”, fontsize=”14", rotation=360, horizontalalignment=’right’, verticalalignment=’top’)
            line.tick_params(axis = 'y', colors = 'yellow')
            line.set_xlim(-0.55)
            line.set_ylim(0)
            #line.yaxis.set_major_locator(MultipleLocator(20))
            #顯示熱量數值
            for i in range(len(data["date"])): #bar上的值
                if data["熱量"][i]!=0.0:
                    line.text(i, data["熱量"][i], data["熱量"][i], size=9, ha = 'center',va='bottom',color="yellow")
                    #print(data["熱量"][i])
            
            #圖標設定
            f_plot.tick_params(axis = 'x', colors = 'white')
            
            #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.07),ncol=3, fancybox=True, shadow=True)
            f_plot.legend(leg.get_patches()+leg2.get_lines(), 
                       [text.get_text() for text in leg.get_texts()+leg2.get_texts()], 
                       loc='upper left', fancybox=True, framealpha=1, shadow=True, borderpad=1, fontsize=11, bbox_to_anchor=(1.1, 0.5),facecolor="#272727",labelcolor='linecolor')
            leg2.remove()
            
            f_plot.grid(linestyle='dotted',linewidth =1, color= 'gray',alpha = 0.4) #網格
            #畫出圖表空間
            canvs = FigureCanvasTkAgg(f, self.analyses_top2)
            print(plt.get_backend())
            #canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #create the toolbar
            toolFrame=ttk.Frame(self.analyses_top2)
            toolFrame.grid(row=2,column=0,sticky="w",padx=150)
            toolbar=NavigationToolbar2Tk(canvs, toolFrame)
            for button in toolbar.winfo_children():
                button.config(background="#737373")

            f_plot.set_title(f"{year}年{month}月  —  月紀錄",color="white")
            f.subplots_adjust(right=0.7)
            
            #canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            canvs.get_tk_widget().grid(row=1,column=0,columnspan=5)
                
        #條件按鈕建立
        selectFrame=ttk.Frame(self.analyses_top2)
        labelY = ttk.Label(selectFrame, text="年份",anchor=tk.CENTER)
        labelM = ttk.Label(selectFrame, text="月份",anchor=tk.CENTER)
        entryY = ttk.Entry(selectFrame,width=10)
        entryM = ttk.Spinbox(selectFrame, from_=1, to=12, increment=1,width=5)
        searchBt = ttk.Button(selectFrame, text="查詢",command=search)
        msg=ttk.Label(selectFrame, text='')
        selectFrame.grid(row=0,column=0,sticky="w",padx=150,pady=7)
        labelY.grid(row=0,column=0,sticky="e")
        entryY.grid(row=0,column=1,padx=30,pady=7,sticky="w")
        labelM.grid(row=0,column=2,sticky="e")
        entryM.grid(row=0,column=3,padx=30,pady=7,sticky="w")
        searchBt.grid(row=0,column=4,padx=40,pady=7)
        msg.grid(row=0,column=5,padx=15,pady=7)
        entryY.insert(0, int(self.todayYear))
        entryM.insert(0, int(self.todayMonth))
        search()
        
    def weekSearch(self):
        analyses_top2 = tk.Toplevel(self.analyses_top)
        analyses_top2.title(f'健體端勢【周分析結果】- {self.user}')
        def search(s):
            data={"date":[],"深蹲":[],"臀橋":[],"弓步蹲":[],"熱量":[]}
            data2={"date":[],"深蹲":[],"臀橋":[],"弓步蹲":[],"熱量":[]}
            selectDate=startCal.get_date()
            selectWeek=startCal.get_date().weekday()
            weekDateList=[]
            try:
                sdate=startCal.get_date()-datetime.timedelta(days=selectWeek)
                edate=startCal.get_date()+datetime.timedelta(days=7-selectWeek-1)
                for i in range(7):
                    weekDateList.append(str(sdate + datetime.timedelta(days=i)))
                msg["text"]=""
            except:
                msg["text"]="*請輸入有效數值!"
                return
            
            self.userinfo_database = Main_data()
            self.onlyuser_database = GoogleSheets()
            self.user_email = self.userinfo_database.get_user_info()
            
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )
            
            self.weekTimes = self.userinfo_database.get_date_times(
                spreadsheetId=self.user_sheetId,
                range='工作表1',
                sdate=str(sdate),
                edate=str(edate),
                )
            
            # prepare data
            f = Figure(figsize=(11, 4), dpi=100)
            f.patch.set_facecolor('#333333') #圖紙的背景顏色
            f_plot = f.add_subplot(111)
            f_plot.clear()
            if self.weekTimes != False:
                res = self.weekTimes
                for i in range(len(res)):
                    date=res[i][0]
                    squat=res[i][1]
                    bridge=res[i][2]
                    lunge=res[i][3]
                    cal=Decimal(0.32 * squat).quantize(Decimal('.00'), ROUND_HALF_UP)+Decimal(0.3 * bridge).quantize(Decimal('.00'), ROUND_HALF_UP)+Decimal(0.5 * lunge).quantize(Decimal('.00'), ROUND_HALF_UP)
                    data2["date"].append(date)
                    data2["深蹲"].append(int(squat))
                    data2["臀橋"].append(int(bridge))
                    data2["弓步蹲"].append(int(lunge))
                    data2["熱量"].append(float(cal))
                #print("data2: ",data2)
                for t in range(len(weekDateList)):
                    data["date"].append(weekDateList[t])
                    data["深蹲"].append(0)
                    data["臀橋"].append(0)
                    data["弓步蹲"].append(0)
                    data["熱量"].append(0)
                    if weekDateList[t] in data2["date"]:    #將0取代呈實際數據
                        indexInData2Dict=data2["date"].index(weekDateList[t])
                        #print(indexInData2Dict)
                        data["深蹲"][t]=data2["深蹲"][indexInData2Dict]
                        data["臀橋"][t]=data2["臀橋"][indexInData2Dict]
                        data["弓步蹲"][t]=data2["弓步蹲"][indexInData2Dict]
                        data["熱量"][t]=data2["熱量"][indexInData2Dict]
                        #print(data)
                        
                #圖表                
                m1_t = pd.DataFrame(data)
                #print("a",m1_t)
                #長條圖製作
                bar = m1_t[['深蹲','臀橋','弓步蹲']].plot(kind='bar', width = .45, stacked=True,ax=f_plot,color=["#96ceb4","#ffad60","#d9534f"])
                #折線圖製作
                #bar.tick_params(axis = 'y', labelcolor = 'r')
                line = m1_t["熱量"].plot(secondary_y=True, color='#ffeead',ax=f_plot)
                #日期設定
                #ax = plt.gca()
                #plt.xlim([-width, len(m1_t['normal'])-width])
                f_plot.set_xticklabels( [str(int(m1_t['date'][d][-2:]))+"日 (周"+self.weekCh[d+1]+")" for d in range(len(m1_t['date']))], color='white' )
                
            else:
                f_plot.axis('off') #移除原本預設xy軸的刻度                
                data={"date":weekDateList,"深蹲":[0]*7,"臀橋":[0]*7,"弓步蹲":[0]*7,"熱量":[0]*7}
                f_plot = f.add_subplot(111)
                m1_t = pd.DataFrame(data)
                #print("b",m1_t)
                bar = m1_t[['深蹲','臀橋','弓步蹲']].plot(kind='bar', width = .45, stacked=True,ax=f_plot,color=["#96ceb4","#ffad60","#d9534f"])
                line = m1_t["熱量"].plot(secondary_y=True, color='#ffeead',ax=f_plot)
                line.set_ylim(0,100)
                #日期設定
                f_plot.set_xticklabels( [d for d in weekDateList], color='white' )
                f_plot.set_ylim(0,100)
            
            #長條圖設定
            bar.set_facecolor("#333333")
            leg = bar.legend()
            #轉成直向文字
            labelRightTxt="次數"
            labelRightTxt_vtc=""
            for i in range(len(labelRightTxt)):
                labelRightTxt_vtc+=labelRightTxt[i]+"\n"
            bar.set_ylabel(labelRightTxt_vtc, fontsize="14", rotation="horizontal", horizontalalignment="right", verticalalignment="bottom",color="white")#, loc="TOP"
            #plt.ylabel(“數量”, fontsize=”14", rotation=360, horizontalalignment=’right’, verticalalignment=’top’)
            bar.tick_params(axis = 'y', colors = 'white')
            bar.set_xlim(-0.55)
            bar.set_ylim(0)
            
            #折線圖設定
            line.spines[:].set_color("white") #外邊框顏色
            leg2 = line.legend()
            #轉成直向文字
            labelRightTxt="熱量"
            labelRightTxt_vtc=""
            for i in range(len(labelRightTxt)):
                labelRightTxt_vtc+=labelRightTxt[i]+"\n"
            line.set_ylabel(labelRightTxt_vtc, color='yellow', fontsize="14", rotation="horizontal", horizontalalignment="left", verticalalignment="bottom")#, loc="TOP"
            #plt.ylabel(“數量”, fontsize=”14", rotation=360, horizontalalignment=’right’, verticalalignment=’top’)
            line.tick_params(axis = 'y', colors = 'yellow')
            line.set_xlim(-0.55)
            line.set_ylim(0)
            #line.yaxis.set_major_locator(MultipleLocator(20))
            #顯示熱量數值
            for i in range(len(data["date"])): #bar上的值
                if data["熱量"][i]!=0.0:
                    line.text(i, data["熱量"][i], data["熱量"][i], size=9, ha = 'center',va='bottom',color="yellow")
                    #print(data["熱量"][i])
            
            #圖標設定
            f_plot.tick_params(axis = 'x', colors = 'white')
            
            #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.07),ncol=3, fancybox=True, shadow=True)
            f_plot.legend(leg.get_patches()+leg2.get_lines(), 
                       [text.get_text() for text in leg.get_texts()+leg2.get_texts()], 
                       loc='upper left', fancybox=True, framealpha=1, shadow=True, borderpad=1, fontsize=11, bbox_to_anchor=(1.1, 0.5),facecolor="#272727",labelcolor='linecolor')
            leg2.remove()
            
            f_plot.grid(linestyle='dotted',linewidth =1, color= 'gray',alpha = 0.4) #網格
            #畫出圖表空間
            canvs = FigureCanvasTkAgg(f, analyses_top2)
            #canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #create the toolbar
            toolFrame=ttk.Frame(analyses_top2)
            toolFrame.grid(row=2,column=0,sticky="w",padx=150)
            toolbar=NavigationToolbar2Tk(canvs, toolFrame)
            for button in toolbar.winfo_children():
                button.config(background="#737373")

            f_plot.set_title(f"{sdate} ~ {edate}  —  周紀錄",color="white")
            f.subplots_adjust(right=0.7)
            
            #canvs.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            canvs.get_tk_widget().grid(row=1,column=0,columnspan=4)
        
        #文字區塊
        sel=tk.StringVar() # declaring string 
        sel.set(str(datetime.date.today()))
        #sel.set(datetime.date.today())
        #條件按鈕建立
        selectFrame=ttk.Frame(analyses_top2)
        labelY = ttk.Label(selectFrame, text="日期",anchor=tk.CENTER)
        startCal=DateEntry(selectFrame,selectmode='day',date_pattern='Y-mm-dd', maxdate=datetime.date.today(),textvariable=sel.get())
        searchBt = ttk.Button(selectFrame, text="查詢",command=lambda: search(None))
        msg=ttk.Label(selectFrame, text='')
        
        startCal.bind("<<DateEntrySelected>>", search)
        
        selectFrame.grid(row=0,column=0,sticky="w",padx=150)
        labelY.grid(row=0,column=1,sticky="e")
        startCal.grid(row=0,column=2, pady=20,padx=30,sticky=('W'))
        searchBt.grid(row=0,column=3,padx=40)
        msg.grid(row=0,column=4,padx=15)
        search(None)

'''root = tk.Tk()
user = "user1"
style = ttk.Style(root)
root.tk.call('source', './azure dark/azure dark.tcl')   #使用azure dark風格
style.theme_use('azure')
Aanalyses(root,user)
root.mainloop()'''