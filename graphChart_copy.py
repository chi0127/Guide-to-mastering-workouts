import tkinter as tk
from tkinter import ttk
#from tkcalendar import Calendar
from tkcalendar import DateEntry
import tkinter.font as tkFont
import dataBase as db
import datetime
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
#隨視窗的滾輪製作參考https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame

from main import GoogleAPIClient
from all_main import Main_data
from googleSheet import GoogleSheets
import pandas as pd

class Graph(tk.Frame):
    sdate=str(datetime.datetime.now().strftime('%Y-%m-%d'))
    edate=str(datetime.datetime.now().strftime('%Y-%m-%d'))
    dateRangeLabel=""
    selectDateLabe2=""
    selectTotalSqu = 0
    selectTotalBri = 0
    selectTotalLun = 0
    selectTotalCa = 0
    
    def __init__(self,root,user):
        tk.Frame.__init__(self, root)
        #root.destroy()
        show_top = tk.Toplevel(root)
        show_top.title(f'健體端勢【記錄查詢】- {user}')
        #ttk.Label(show_top,text="top").grid(row=1,column=1)
        
        default_font = tkFont.nametofont("TkDefaultFont")  #改原本預設的字型
        default_font.configure(family='Helvetica', size=15)
        
        bLogin = ttk.Style()
        treeStyle=ttk.Style()
        bLogin.configure("bLogin.TButton", font=('Helvetica', 20), width=5)
        treeStyle.configure("Table.Treeview", font=("System", 20), rowheight=40)#, background="#F6F4EC"
        #資料表
        treeFrame = ttk.Frame(show_top)
        treeScroll = ttk.Scrollbar(treeFrame)
        self.treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1,2,3,4), height=5, style="Table.Treeview")#height可放筆數
        
        treeScroll.config(command=self.treeview.yview)
        
        self.treeview.column("#0", width=220)
        self.treeview.column(1, anchor='center', width=120)
        self.treeview.column(2, anchor='center', width=120)
        self.treeview.column(3, anchor='center', width=120)
        self.treeview.column(4, anchor='center', width=120)

        self.treeview.heading("#0", text="日期", anchor='center')
        self.treeview.heading(1, text="深蹲", anchor='center')
        self.treeview.heading(2, text="橋臀", anchor='center')
        self.treeview.heading(3, text="弓步蹲", anchor='center')
        self.treeview.heading(4, text="總消耗熱量", anchor='center')
        #文字區塊
        sel=tk.StringVar() # declaring string variable
        sel2=tk.StringVar() # declaring string variable
        startTxt = ttk.Label(show_top, text="起始日: ")
        endTxt = ttk.Label(show_top, text="結束日: ")
        print(self.sdate,self.edate )
        self.dateRangeLabel = ttk.Label(show_top, text=f"{self.sdate} 至 {self.edate} 的紀錄:")
        totalSqu = ttk.Label(show_top, text="深蹲: 0次，消耗 0.00卡")
        totalBri = ttk.Label(show_top, text="臀橋: 0次，消耗 0.00卡")
        totalLun = ttk.Label(show_top, text="弓步蹲: 0次，消耗 0.00卡")
        totalCa = ttk.Label(show_top, text="總共消耗 0卡")
        
        self.selectDateLabe2 = ttk.Label(show_top, text="請點選紀錄查看詳細資料")
        self.selectTotalSqu = ttk.Label(show_top, text="")
        self.selectTotalBri = ttk.Label(show_top, text="")
        self.selectTotalLun = ttk.Label(show_top, text="")
        self.selectTotalCa = ttk.Label(show_top, text="")
        self.endCal=DateEntry(show_top,selectmode='day',date_pattern='Y-mm-dd', maxdate=datetime.date.today(),textvariable=sel2)
        self.maxEndDate = datetime.datetime.strptime(str(self.endCal.get_date()), "%Y-%m-%d").date()#today=datetime.datetime.now().strftime('%Y-%m-%d')
        self.startCal=DateEntry(show_top,selectmode='day',date_pattern='Y-mm-dd', maxdate=self.maxEndDate,textvariable=sel)
        
        startTxt.grid(row=1, column=1, pady=20)
        endTxt.grid(row=1, column=3, pady=20)
        self.endCal.grid(row=1,column=4, pady=20,sticky=('W'))
        self.startCal.grid(row=1,column=2, pady=20,sticky=('W'))
        treeFrame.grid(row=2, column=1, columnspan=5, padx=15, pady=15)
        self.treeview.grid(row=2, column=1, columnspan=5)
        treeScroll.grid(row=2, column=6, sticky='ns')
        
        self.dateRangeLabel.grid(row=3, column=1, columnspan=3, pady=10, padx=20, sticky='w')
        totalSqu.grid(row=4, column=1, columnspan=3, pady=10, padx=20, sticky='w')
        totalBri.grid(row=5, column=1, columnspan=3, pady=10, padx=20, sticky='w')
        totalLun.grid(row=6, column=1, columnspan=3, pady=10, padx=20, sticky='w')
        totalCa.grid(row=7, column=1, columnspan=3, pady=10, padx=20, sticky='w')
        
        self.selectDateLabe2.grid(row=3, column=4, columnspan=2, pady=10, padx=20, sticky='w')
        self.selectTotalSqu.grid(row=4, column=4, columnspan=2, pady=10, padx=20, sticky='w')
        self.selectTotalBri.grid(row=5, column=4, columnspan=2, pady=10, padx=20, sticky='w')
        self.selectTotalLun.grid(row=6, column=4, columnspan=2, pady=10, padx=20, sticky='w')
        self.selectTotalCa.grid(row=7, column=4, columnspan=2, pady=10, padx=20, sticky='w')
        
        #print(str(endCal.get_date()))
        
        def selectItem(a):
            curItem = self.treeview.focus()
            Scount = self.treeview.item(curItem)["values"][0]
            Bcount = self.treeview.item(curItem)["values"][1]
            Lcount = self.treeview.item(curItem)["values"][2]
            calSqu=Decimal(0.32 * Scount).quantize(Decimal('.00'), ROUND_HALF_UP)
            calBri=Decimal(0.3 * Bcount).quantize(Decimal('.00'), ROUND_HALF_UP)
            calLun=Decimal(0.5 * Lcount).quantize(Decimal('.00'), ROUND_HALF_UP)
            calToday = calSqu + calBri + calLun
            self.selectDateLabe2["text"] = f"{self.treeview.item(curItem)['text']} 的紀錄:"
            print(self.treeview.item(curItem)["text"])
            self.selectTotalSqu["text"] = f"深蹲: {str(Scount)}次，消耗 {str(calSqu)}卡"
            self.selectTotalBri['text']=f"臀橋: {str(Bcount)}次，消耗 {str(calBri)}卡"
            self.selectTotalLun['text']=f"弓步蹲: {str(Lcount)}次，消耗 {str(calLun)}卡"
            self.selectTotalCa['text']=f"總共消耗 {calToday}卡"
            print(self.treeview.item(curItem), self.treeview.item(curItem)["values"][0])
        
        def search():
            global sdate,edate
            #print(self.startCal.get_date(),self.endCal.get_date())
            #print(type(self.startCal.get_date()))
            self.sdate=str(self.startCal.get_date())
            self.edate=str(self.endCal.get_date())
            self.treeview.delete(*self.treeview.get_children())
            Scount=0
            Bcount=0
            Lcount=0
            
            self.userinfo_database = Main_data()
            self.onlyuser_database = GoogleSheets()
            self.user_email = self.userinfo_database.get_user_info()
            
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )
            
            self.dateTimes = self.userinfo_database.get_date_times(
                spreadsheetId=self.user_sheetId,
                range='工作表1',
                sdate=self.sdate,
                edate=self.edate,
                )
            
            if self.dateTimes != False:
                res=self.dateTimes
                #date2, username, squat_counter, glutebridge_counter, lunge_counter = db.showDataBySearchDate(self.sdate,self.edate, user)
                for i in range(len(res)):
                    calSqu=Decimal(0.32 * res[i][1]).quantize(Decimal('.00'), ROUND_HALF_UP)
                    calBri=Decimal(0.3 * res[i][2]).quantize(Decimal('.00'), ROUND_HALF_UP)
                    calLun=Decimal(0.5 * res[i][3]).quantize(Decimal('.00'), ROUND_HALF_UP)
                    calToday = calSqu + calBri + calLun
                    self.treeview.insert(parent='', index='end', iid=i, text=res[i][0], values=(res[i][1], res[i][2], res[i][3], calToday))
                    #self.treeview.insert(parent='', index='end', iid=2, text="Parent", values=("Item 1", "Value 2"))
                    self.dateRangeLabel["text"] = f"{self.sdate} 至 {self.edate} 的紀錄:"
                    self.treeview.bind('<ButtonRelease-1>', selectItem)
                    Scount+=res[i][1]
                    Bcount+=res[i][2]
                    Lcount+=res[i][3]
                calSqu=Decimal(0.32 * Scount).quantize(Decimal('.00'), ROUND_HALF_UP)
                calBri=Decimal(0.3 * Bcount).quantize(Decimal('.00'), ROUND_HALF_UP)
                calLun=Decimal(0.5 * Lcount).quantize(Decimal('.00'), ROUND_HALF_UP)
                totalSqu['text']=f"深蹲: {str(Scount)}次，消耗 {calSqu}卡"
                totalBri['text']=f"臀橋: {str(Bcount)}次，消耗 {calBri}卡"
                totalLun['text']=f"弓步蹲: {str(Lcount)}次，消耗 {calLun}卡"
                totalCa['text']=f"總共消耗 {calSqu + calBri + calLun}卡"
            else:
                self.treeview.insert(parent='', index='end', iid=1, text="沒有資料")
        
        searchB=ttk.Button(show_top, text="查詢",command=search)
        searchB.grid(row=1,column=5)
        
        #結束日小於起始日時就將起始日設定為結束日
        def endDateTrace(*args):
            try:
                self.maxEndDate=datetime.datetime.strptime(str(sel2.get()), "%Y-%m-%d").date()
            except:
                pass
            selectDate=datetime.datetime.strptime(str(sel.get()), "%Y-%m-%d").date()
            self.startCal["maxdate"]=self.maxEndDate
            if selectDate>self.maxEndDate:
                sel.set(self.maxEndDate)
        sel2.trace('w',endDateTrace)
        
        #進入就先顯示今天紀錄
        search()
        
        

'''root = tk.Tk()
user = "user1"
style = ttk.Style(root)
root.tk.call('source', './azure dark/azure dark.tcl')   #使用azure dark風格
style.theme_use('azure')
Graph(root,user)
root.mainloop()'''