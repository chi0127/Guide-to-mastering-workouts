import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk
#show_webcam的import
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import threading
import time
import os
from tqdm import tqdm
from IPython.core.display import Image#反轉套件
from PIL import ImageFont, ImageDraw, Image #載入中文字型
import pygame #載入音樂撥放器
import ttkwidgets as ttkw #TickScale使用
import pyttsx3 #錯誤姿勢語音
from PIL import Image, ImageDraw, ImageFont#繪制中文文字in cv2 
from decimal import Decimal, ROUND_HALF_UP

#db1111010
#!pip install databases
import dataBase as db
import datetime
#from functools import partial #tkinter的command增加參數用
#from view import *
from graphChart import Graph as graph
from analysesResult import Aanalyses as analyses

from main import GoogleAPIClient
from all_main import Main_data
from googleSheet import GoogleSheets
import pandas as pd
from graphChart_copy import Graph as googlegtaph
from analysesResult_copy import Aanalyses as googleAanalyses

class Application(tk.Frame):
    #counter=0
    lunge_counter=0
    glutebridge_counter=0
    squat_counter=0
    #cal_counter=0.0
    stage=None
    worst_txt=None  
    s= pyttsx3.init()#語音
    poseAngle=True
    frameWidth=640
    frameHeight=480
    img_w=frameWidth
    img_h=frameHeight
    cap=None
    bgm="4 Minute Tabata  Intense HIIT Workout   No Repeat  No Equipment.mp3"#"good.mp3"
    countUp_sound="counter_sound.mp3" #計數增加時放的音樂
    g=0
    voice_ON="./voice.png"
    voice_OFF='./mute.png'
    first_voice_on=True
    first_voice_on_value=0.0
    circle_angle=360 #圓圈的一圈角度
    #背景音樂初始化
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.6) #音量0-1
    sound_channel_0=pygame.mixer.Channel(0) #計數增加的音樂頻道
    countUp_volumn=0
    allPoseName={'glutebridge':'橋臀','lunge':'弓步蹲','squat':'深蹲'}
    #cap=cv2.VideoCapture(0)
    
    #db1010
    today=datetime.datetime.now().strftime('%Y-%m-%d')       
    user='visitor'
    VISITOR_ACCOUNT='visitor'
    VISITOR_PASSWORD='visitor'
    
    def showTable(self):
        if self.user != 'googleuser':
            table=graph(root,self.user)
        else:
            self.userinfo_database = Main_data()
            self.user_email = self.userinfo_database.get_user_info()
            self.onlyuser_database = GoogleSheets()
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )           
            update_cell_num = self.userinfo_database.get_day_pos(
                spreadsheetId=self.user_sheetId,
                range='工作表1',
                date=str(datetime.date.today()),
                )
            update_cell = "B" + str(update_cell_num) + ":D" +str(update_cell_num)
            self.userinfo_database.updateSheet(
                spreadsheetId=self.user_sheetId, 
                range_name=update_cell, 
                df=[[self.squat_counter,self.glutebridge_counter,self.lunge_counter]]
                )
            
            squat_counter, glutebridge_counter, lunge_counter =self.userinfo_database.get_today_times(
                spreadsheetId=self.user_sheetId, 
                range="工作表1", 
                date=str(datetime.date.today()))
            table1=googlegtaph(root,self.user)
        
    def showAnalyses(self):
        if self.user != 'googleuser':
            analysesResult=analyses(root,self.user)
        else:
            self.userinfo_database = Main_data()
            self.user_email = self.userinfo_database.get_user_info()
            self.onlyuser_database = GoogleSheets()
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )           
            update_cell_num = self.userinfo_database.get_day_pos(
                spreadsheetId=self.user_sheetId,
                range='工作表1',
                date=str(datetime.date.today()),
                )
            update_cell = "B" + str(update_cell_num) + ":D" +str(update_cell_num)
            self.userinfo_database.updateSheet(
                spreadsheetId=self.user_sheetId, 
                range_name=update_cell, 
                df=[[self.squat_counter,self.glutebridge_counter,self.lunge_counter]]
                )
            
            squat_counter, glutebridge_counter, lunge_counter =self.userinfo_database.get_today_times(
                spreadsheetId=self.user_sheetId, 
                range="工作表1", 
                date=str(datetime.date.today()))
            analysesResult=googleAanalyses(root,self.user)
        
    def switchUser(self):
        global user
        #root.destroy()
        switch_top = tk.Toplevel(root)
        #ttk.Label(switch_top,text="top").grid(row=1,column=1)
        switch_top.title("健體端勢【使用者切換】")
        
        default_font = tkFont.nametofont("TkDefaultFont")  #改原本預設的字型
        default_font.configure(family='Helvetica', size=15)
        
        bLogin = ttk.Style()
        bLogin.configure("bLogin.TButton", font=('Helvetica', 20), width=5)
        
        login_frame = ttk.Frame(switch_top)
        login_frame.grid(padx=15, pady=15)
        
        filepath = r".credentials/cred.json"        
        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
            except OSError as e:
                print(e)
            else:
                print("File is deleted successfully")
        else:
          print("google_creds檔案不存在。")
                
        ttk.Label(login_frame, text='帳號:', anchor=tk.CENTER).grid(column=1, row=1, columnspan=2)
        self.account = ttk.Entry(login_frame)
        self.account.grid(column=3, row=1, columnspan=3, padx=10, pady=8, sticky='W')
        #account.insert(0, 'Entry')
        
        ttk.Label(login_frame, text='密碼:', anchor=tk.CENTER).grid(column=1, row=2, columnspan=2)
        self.password = ttk.Entry(login_frame, show='*')
        self.password.grid(column=3, row=2, columnspan=3, padx=10, pady=8, sticky='W')
        
        def reg():
            '''註冊'''
            account=self.account.get()
            password=self.password.get()
            if account=='' or password=='':
                msg['text']="*請輸入欲註冊帳號及密碼!"
                msg['foreground']='#ff4a4a'
            else:
                try:
                    if db.createAccount(account,password):
                        msg['text']="註冊成功! 請登入並開始使用:)"
                        msg['foreground']='white'
                    else:
                        msg['text']="*此帳號已存在!"
                        msg['foreground']='#ff4a4a'
                except Exception as e:
                    if int(str(e)[1:-1].split(',',1)[0]) == 1406:
                        msg['text']="*帳號及密碼長度需小於50!"
                        msg['foreground']='#ff4a4a'
                    else:
                        msg['text']="*資料格式錯誤"
                        msg['foreground']='#ff4a4a'
        
        def cert():    
            '''這裡需要驗證用戶名和密碼對不對,不對就跳出對話框告訴他,對就destroyee'''
            account=self.account.get()
            password=self.password.get()
            if account=='' or password=='':
                msg['text']="*請輸入正確的帳號及密碼!"
                msg['foreground']='#ff4a4a'
            else:
                if db.confirmAccount(account,password):
                    login_frame.destroy() #TREET
                    ttk.Label(switch_top, text='切換中...', anchor=tk.CENTER, font=('Helvetica', 25)).grid(column=1, row=1, padx=70, pady=45)
                    self.user = account
                    self.__init__(switch_top)
                    switch_top.destroy()
                else:
                    msg['text']="*請輸入正確的帳號及密碼:("
                    msg['foreground']='#ff4a4a'
                     
        def visit():
            db.confirmAccount(self.VISITOR_ACCOUNT,self.VISITOR_PASSWORD)
            login_frame.destroy() #TREET
            ttk.Label(switch_top, text='切換中...', anchor=tk.CENTER, font=('Helvetica', 25)).grid(column=1, row=1, padx=70, pady=45)
            #self.end_exercise()
            pygame.mixer.music.stop()
            self.poseAngle=False
            self.user = self.VISITOR_ACCOUNT
            self.__init__(switch_top)
            switch_top.destroy()
            
        def google_login():
            self.userinfo_database = Main_data()
            print(self.userinfo_database.googleAPIService)
            self.onlyuser_database = GoogleSheets()
            print(self.onlyuser_database.googleAPIService)
            self.user_email = self.userinfo_database.get_user_info()
            print(self.user_email)
            if os.path.isfile(filepath):        
                self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )
            if self.user_sheetId == False:
                self.onlyuser_database.appendWorksheet(
                        spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
                        range='工作表1',
                        df=pd.DataFrame(
                            {'email': [self.user_email],
                            'sheet_id': [self.userinfo_database.createsheet('exercise')],
                            }
                        )
                    )
                self.user_sheetId = self.onlyuser_database.getWorksheet(
                    spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
                    range='工作表1',
                    email=self.user_email,)
                
                print(self.userinfo_database.setWorksheet(
                    spreadsheetId=self.user_sheetId,
                    range='工作表1',
                    df=pd.DataFrame(
                        {'data': [str(datetime.date.today())],
                        'squat': [0],
                        'glute_bridge': [0],
                        'lunge': [0]},
                    )
                        )
                            )
            else:
                self.update_cell_num = self.userinfo_database.get_day_pos(
                    spreadsheetId=self.user_sheetId,
                    range='工作表1',
                    date=str(datetime.date.today()), #str(datetime.date.today())
                    )
                if self.update_cell_num == False:
                    self.userinfo_database.appendWorksheet(
                            spreadsheetId=self.user_sheetId,
                            range='工作表1',
                            df=pd.DataFrame(
                                {'data': [str(datetime.date.today())],
                                'squat': [0],
                                'glute_bridge': [0],
                                'lunge': [0],
                                }
                            )
                        )

            login_frame.destroy() #TREET
            ttk.Label(switch_top, text='切換中...', anchor=tk.CENTER, font=('Helvetica', 25)).grid(column=1, row=1, padx=70, pady=45)
            self.user = 'googleuser'
            self.__init__(switch_top)
            switch_top.destroy()
            
        #account=self.account.get()
        #password=account.get()
        msg=ttk.Label(login_frame, text='')
        msg.grid(column=1, row=4, columnspan=5)
        ttk.Button(login_frame,text='訪客',style='bLogin.TButton', command=visit).grid(column=1, row=3, columnspan=2, padx=10, pady=15)
        ttk.Button(login_frame,text='註冊',style='bLogin.TButton', command=reg).grid(column=3, row=3, columnspan=2, padx=10, pady=15)
        ttk.Button(login_frame,text='登入',style='bLogin.TButton', command=cert).grid(column=5, row=3, columnspan=2, padx=10, pady=15)
        ttk.Button(login_frame,text='Google',style='bLogin.TButton', command=google_login).grid(column=7, row=3, columnspan=2, padx=10, pady=15, ipadx=20)
        
        return login_frame #這裡一定要return

    def resetCounter(self):
        global squat_counter, glutebridge_counter, lunge_counter
        if self.user != 'googleuser':
            self.squat_counter, self.glutebridge_counter, self.lunge_counter = db.setCounter(self.today, self.user, 0, 0, 0)
            self.count_display(3)
        else:
            update_cell_num = self.userinfo_database.get_day_pos(
                spreadsheetId=self.user_sheetId,
                range='工作表1',
                date=str(datetime.date.today()), #str(datetime.date.today())
                )
            update_cell = "B" + str(update_cell_num) + ":D" +str(update_cell_num)

            self.userinfo_database.updateSheet(
                spreadsheetId=self.user_sheetId, 
                range_name=update_cell, 
                df=[[0,0,0]]
                )
            squat_counter, glutebridge_counter, lunge_counter =self.userinfo_database.get_today_times(
                spreadsheetId=self.user_sheetId, 
                range="工作表1", 
                date=str(datetime.date.today()))
            self.squat_counter = int(squat_counter)
            self.glutebridge_counter = int(glutebridge_counter)
            self.lunge_counter = int(lunge_counter)
            self.count_display(5)
    
    def cv2AddChineseText(self, img, text, position, textColor=(0, 255, 0), textSize=30,stroke_fill=None,stroke_width=0):
        if (isinstance(img, np.ndarray)):  # 判斷是否是OpenCV圖片類型(np.ndarray))
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if img!=None:
            draw = ImageDraw.Draw(img) #建立一個可以在給定圖像上繪製的對象
            fontStyle = ImageFont.truetype("NotoSansHK-Bold.otf", textSize, encoding="utf-8") #字體的格式
            draw.text(position, text, textColor, font=fontStyle, stroke_fill=stroke_fill, stroke_width=stroke_width) #繪製文本
            
            return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR) #轉換回OpenCV格式
        return None

    def scraper(self,data):
        self.s.say(data)
        #time.sleep(3)
        try:
            self.s.runAndWait()
        #self.s.stop()
        except:
            self.s.endLoop()

    #定義函數計算關節角度(用三角函數計算)
    def calculate_angle(self,a,b,c):
        a=np.array(a)#first
        b=np.array(b)#mid
        c=np.array(c)#end
        
        radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
        angle=np.abs(radians*180.0/np.pi)
        
        if angle>180.0:
            angle=360-angle     
        return angle
    
    def point_touch(self,state,startTime,point,target,wristR,wristL):
        if time.time()-startTime>3:
            temTime=[]
            timeGap=0.1
            editTimeGap=True
            fontSize=70
            #開始前的啟動機制
            while state=='start':
                c=self.circle_angle
                s=0
                with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
                    while self.cap.isOpened():
                        ret, frame = self.cap.read()
                        #畫面大小控制
                        frame = cv2.resize(frame, (self.img_w,self.img_h))
                        frame = cv2.flip(frame,1) #影像反轉                            
                        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False
                        #Make detection
                        results = pose.process(image)
                    
                        #Recolor back to BGR (RGB TO BGR)
                        image.flags.writeable = True
                        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
                        landmarks=results.pose_landmarks.landmark
                        if point=='knee':
                            points=[landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        elif point=='head':
                            points=[landmarks[self.mp_pose.PoseLandmark.NOSE.value].x,landmarks[self.mp_pose.PoseLandmark.NOSE.value].y]
                        WRx=landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x
                        WLx=landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x
                        sx=points[0]
                        WRy=landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y
                        WLy=landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y
                        sy=points[1]
                        #print('手腕x: ',WRx,' ','手腕y: ',WRy,' ','肩膀x: ',sx,'肩膀y: ',sy)
                        #print(abs(WRx-sx),abs(WRx-sx)<=0.1,abs(WRy-sy),abs(WRy-sy)<=0.1)
                        if (abs(WRx-sx)<=0.1 and abs(WRy-sy)<=0.1) or (abs(WLx-sx)<=0.1 and abs(WLy-sy)<=0.1):
                            #print(landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,'  ',landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x)
                            if editTimeGap and len(temTime)<11: temTime.append(round(time.time(),4)-round(s,4))
                            if editTimeGap and len(temTime)>=11:
                               temTime[0]=0
                               timeGap=round(sum(temTime)/len(temTime),4)
                               editTimeGap=False
                               for n in range(0,5):
                                   if timeGap>10**-n:
                                       timeGap+=5/10**n
                                       break
                            if s!=0 and time.time()-s>timeGap: c=self.circle_angle
                            c-=10
                            cv2.ellipse(image, tuple(np.multiply(points,[self.img_w,self.img_h]).astype(int)), (50,50), 45, 0, c, (0, 0, 255), 20)
                            s=time.time()
                            if c==0:
                                state='continue'
                                break
                        
                        cv2.ellipse(image, tuple(np.multiply(points,[self.img_w,self.img_h]).astype(int)), (50,50), 45, 0, 360, (0, 255, 255), 2)
                        #Render detections
                        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
                        #開始前提示文字
                        if self.img_w>900: fontSize=100
                        elif self.img_w>540: fontSize=70
                        else: fontSize=30
                        image=self.cv2AddChineseText(image,'觸碰黃圈處開始', (self.img_w//2-self.img_w//3,self.img_h//2-self.img_w//8),(230,194,3),fontSize,(30,30,30),1)
                        
                        #cv2.imshow('frame', image)
                        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(image)
                        imgtk = ImageTk.PhotoImage(image=img)
                        self.stream.imgtk = imgtk
                        self.stream.configure(image=imgtk)
                        #self.stream.after(15, self.show_frame)
                        self.stream.update()
                        self.cam_size(image)
                startTime=time.time()
            if state=='continue': #要stop了
                if (abs(target.x-wristR.x)<=0.1 and abs(target.y-wristR.y)<=0.1) or (abs(target.x-wristL.x)<=0.1 and abs(target.y-wristL.y)<=0.1):
                    state='stop'
                    startTime=time.time()
            elif state=='stop': #要continue了
                if (abs(target.x-wristR.x)<=0.1 and abs(target.y-wristR.y)<=0.1) or (abs(target.x-wristL.x)<=0.1 and abs(target.y-wristL.y)<=0.1):
                    state='continue'
                    startTime=time.time()
                
        return state, startTime
    
    def switchPose(self,cur_pose):
        c=self.circle_angle
        s=0
        startTime=0
        temTime=[]
        timeGap=0.2
        editTimeGap=True
        cur_pose=list(self.allPoseName.values())[list(self.allPoseName.keys()).index(cur_pose)]
        #導入畫圖工具
        self.mp_drawing = mp.solutions.drawing_utils
        #導入姿勢估計模型
        self.mp_pose = mp.solutions.pose
        if(self.cap==None): self.cap = cv2.VideoCapture(0)#cap=第一鏡頭,VC物件會連接到第一攝影機
        with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as self.pose:
            while self.cap.isOpened():
                fontSize=70
                ret, frame = self.cap.read()
                #畫面大小控制
                frame = cv2.resize(frame, (self.img_w,self.img_h))
                frame = cv2.flip(frame,1) #影像反轉                            
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                #Make detection
                results = self.pose.process(image)
            
                #Recolor back to BGR (RGB TO BGR)
                image.flags.writeable = True
                image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            
                #Extract landmarks
                try:
                    landmarks=results.pose_landmarks.landmark
              #-----此處能將特定角度渲染到影像內，如想更改計算的角度只需注意中點，更改三個關節的參數
                    #Get coordinates
                    #手腕位置
                    l_pinky=[landmarks[self.mp_pose.PoseLandmark.LEFT_PINKY.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_PINKY.value].y]
                    r_pinky=[landmarks[self.mp_pose.PoseLandmark.RIGHT_PINKY.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_PINKY.value].y]
                    
                    #Visualize
                    imageCopy=image.copy()
                    cv2.rectangle(imageCopy,(self.img_w//2-self.img_w//3,self.img_h//2-self.img_w//4),(self.img_w//2+self.img_w//10*3,self.img_h//2+self.img_w//10*3),(245,117,16),-1)
                    image = cv2.addWeighted(imageCopy,1,image,0.3,1)
                    cv2.putText(image,'>',
                                (self.img_w-80,self.img_h//2+self.img_h//10),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SCRIPT_COMPLEX,2.5,(0,0,255),5,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    cv2.putText(image,'<',
                                (0,self.img_h//2+self.img_h//10),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SCRIPT_COMPLEX,2.5,(0,0,255),5,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    cv2.putText(image,'X',
                                (self.img_w-self.img_w//10,0+self.img_h//10),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    
                    #動作的文字輸出
                    if self.img_w>900: fontSize=100
                    image=self.cv2AddChineseText(image,'GO', (self.img_w//2-self.img_w//15,self.img_h//2-self.img_w//4),(0,0,255),fontSize-40,(0,0,255),1)
                    if len(cur_pose)<5:
                        image=self.cv2AddChineseText(image,cur_pose, (self.img_w//2-self.img_w//6,self.img_h//2-self.img_h//20),(0,0,255),fontSize,(0,0,255),1)
                    else:
                        image=self.cv2AddChineseText(image,cur_pose, (self.img_w//2-self.img_w//4,self.img_h//2-self.img_h//20),(0,0,255),fontSize,(0,0,255),1)
                    
                    #cv2.ellipse(image, (self.img_w//2-self.img_w//27,self.img_h//2-self.img_w//5), (40,40), 45, 0, 360, (0, 255, 255), 2)
                    #cv2.ellipse(image, (self.img_w//2-self.img_w//15,self.img_h//2-self.img_w//4), (40,40), 45, 0, 360, (0, 255, 255), 2)
            #------        
                    l_pinky_point = np.multiply(l_pinky,[self.img_w,self.img_h]).astype(int)
                    r_pinky_point = np.multiply(r_pinky,[self.img_w,self.img_h]).astype(int)
                    #碰到X關掉
                    if ( abs(l_pinky_point[0]-(self.img_w-self.img_w//10))<40 and abs(l_pinky_point[1]-(0+self.img_h//10))<40 ) or ( abs(r_pinky_point[0]-(self.img_w-self.img_w//10))<130 and abs(r_pinky_point[1]-0+self.img_h//10)<120 ):
                        #break
                        if cur_pose==list(self.allPoseName.values())[0]: self.glutebridge('continue')
                        elif cur_pose==list(self.allPoseName.values())[1]: self.lunge('continue')
                        elif cur_pose==list(self.allPoseName.values())[2]: self.squat('continue')
                        break
                    #碰到go進入該動作
                    if ( abs(l_pinky_point[0]-(self.img_w//2-45))<50 and abs(l_pinky_point[1]-(self.img_h//2-self.img_w//4))<45 ) or ( abs(r_pinky_point[0]-(self.img_w//2-45))<50 and abs(r_pinky_point[1]-(self.img_h//2-self.img_w//4))<45 ):
                        if editTimeGap and len(temTime)<11: temTime.append(round(time.time(),4)-round(s,4))
                        if editTimeGap and len(temTime)>=11:
                            temTime[0]=0
                            timeGap=round(sum(temTime)/len(temTime),4)
                            editTimeGap=False
                            for n in range(0,5):
                                if timeGap>10**-n:
                                    timeGap+=5/10**n
                                    break
                        if s!=0 and time.time()-s>timeGap: c=self.circle_angle
                        c-=25
                        cv2.ellipse(image, (self.img_w//2-self.img_w//27,self.img_h//2-self.img_w//5), (50,50), 45, 0, c, (0, 0, 255), 10)
                        s=time.time()
                        if c<=0:
                            if cur_pose==list(self.allPoseName.values())[0]: self.go_glutebridge()
                            elif cur_pose==list(self.allPoseName.values())[1]: self.go_lunge()
                            elif cur_pose==list(self.allPoseName.values())[2]: self.go_squat()
                            break
                    
                    endTime=time.time()
                    if endTime-startTime>1:
                        #碰到>下一個動作
                        if ( abs(l_pinky_point[0]-self.img_w-80)<160 and abs(l_pinky_point[1]-(self.img_h//2+self.img_h//10))<50 ) or ( abs(r_pinky_point[0]-self.img_w-80)<160 and abs(r_pinky_point[1]-(self.img_h//2+self.img_h//10))<50 ):
                            #print(r_pinky_point[0],'\/',self.img_w-self.img_w//2)
                            cur_pose = list(self.allPoseName.values())[0] if list(self.allPoseName.values()).index(cur_pose)>=(len(self.allPoseName)-1) else list(self.allPoseName.values())[list(self.allPoseName.values()).index(cur_pose)+1]
                            #print(cur_pose)
                        #碰到<上一個動作
                        if ( abs(l_pinky_point[0]-(0+10))<40 and abs(l_pinky_point[1]-(self.img_h//2+self.img_h//10))<50 ) or ( abs(r_pinky_point[0]-(0+25))<40 and abs(r_pinky_point[1]-(self.img_h//2+self.img_h//10))<50 ):
                            #print(cur_pose)
                            cur_pose = list(self.allPoseName.values())[len(self.allPoseName)-1] if list(self.allPoseName.values()).index(cur_pose)<=0 else list(self.allPoseName.values())[list(self.allPoseName.values()).index(cur_pose)-1]
                            #print(cur_pose)
                        startTime=time.time()
                    #print('手的x: ',r_pinky_point[0],'箭頭的x座標: ',self.img_w-80)
                except:
                    pass
                
                #Render detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            
                #cv2.imshow('frame', image)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.stream.imgtk = imgtk
                self.stream.configure(image=imgtk)
                #self.stream.after(15, self.show_frame)
                self.stream.update()
                self.cam_size(image)
            
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
    
    def openArms(self):
        with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as self.pose:
            while self.cap.isOpened():
                fontSize=70
                ret, frame = self.cap.read()
                #畫面大小控制
                frame = cv2.resize(frame, (self.img_w,self.img_h))
                frame = cv2.flip(frame,1) #影像反轉                            
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                #Make detection
                results = self.pose.process(image)
            
                #Recolor back to BGR (RGB TO BGR)
                image.flags.writeable = True
                image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            
                #Extract landmarks
                try:
                    landmarks=results.pose_landmarks.landmark
              #-----此處能將特定角度渲染到影像內，如想更改計算的角度只需注意中點，更改三個關節的參數
                    #Get coordinates
                    #左肩角度
                    l_hip=[landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    l_shoulder=[landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    l_elbow=[landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    
                    #右肩角度
                    r_hip=[landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    r_shoulder=[landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    r_elbow=[landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                    #左臀角度
                    l_hip=[landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    l_shoulder=[landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    l_knee=[landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                    #右臀角度
                    r_hip=[landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    r_shoulder=[landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    r_knee=[landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
              
                    #Calculate angle
                    angle_l_shoulder=self.calculate_angle(l_hip,l_shoulder,l_elbow)
                    angle_r_shoulder=self.calculate_angle(r_hip,r_shoulder,r_elbow)
                    angle_l_hip=self.calculate_angle(l_shoulder,l_hip,l_knee)
                    angle_r_hip=self.calculate_angle(r_shoulder,r_hip,r_knee)
                    
                    #Visualize
                    cv2.putText(image,str(int(angle_l_shoulder)),
                                tuple(np.multiply(l_shoulder,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    cv2.putText(image,str(int(angle_r_shoulder)),
                                tuple(np.multiply(r_shoulder,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    cv2.putText(image,str(int(angle_l_hip)),
                                tuple(np.multiply(l_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    cv2.putText(image,str(int(angle_r_hip)),
                                tuple(np.multiply(r_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA#次數輸出跟字體顏色
                               )
            #------        
                    #Curl Counter logic
                    if angle_l_shoulder>85 and angle_r_shoulder>85 and angle_l_hip>150 and angle_r_hip>150:
                        break
                except:
                    pass
                #if self.img_w>700: fontSize=100
                if self.img_w>900: fontSize=100
                elif self.img_w>540: fontSize=70
                else: fontSize=30
                image=self.cv2AddChineseText(image,'擺大字型', (self.img_w//2-self.img_w//4,self.img_h//2-self.img_w//7),(230,194,3),fontSize,(30,30,30),1)
                image=self.cv2AddChineseText(image,'即可開始預測', (self.img_w//2-self.img_w//3,self.img_h//2),(230,194,3),fontSize,(30,30,30),1)
                
                #Render detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            
                #cv2.imshow('frame', image)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.stream.imgtk = imgtk
                self.stream.configure(image=imgtk)
                #self.stream.after(15, self.show_frame)
                self.stream.update()
                self.cam_size(image)
            
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
    
    def glutebridge(self,state):
        global glutebridge_counter
        #self.counter=0
        self.stage=None
        self.poseAngle=True
        self.mp_drawing = mp.solutions.drawing_utils #導入畫圖工具
        self.mp_pose = mp.solutions.pose #導入姿勢估計模型
        if state!='continue': state='start'
        startTime=0
        if self.cap==None: self.cap = cv2.VideoCapture(0)#cap=第一鏡頭,VC物件會連接到第一攝影機
        with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as self.pose:
            while self.poseAngle:
                ret, frame = self.cap.read()
                #畫面大小控制
                frame = cv2.resize(frame, (self.img_w,self.img_h))
                frame = cv2.flip(frame,1) #影像反轉                            
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                #Make detection
                results = self.pose.process(image)
                #Recolor back to BGR (RGB TO BGR)
                image.flags.writeable = True
                image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            
                #Extract landmarks
                try:
                    landmarks=results.pose_landmarks.landmark
              #-----此處能將特定角度渲染到影像內，如想更改計算的角度只需注意中點，更改三個關節的參數
                    #Get coordinates
                    #右腹部(m的左腹部)
                    r_shoulder=[landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    r_hip=[landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    r_knee=[landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    #左腹部(m的右腹部)
                    l_shoulder=[landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    l_hip=[landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    l_knee=[landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    #Calculate angle
                    r_angle=self.calculate_angle(r_shoulder,r_hip,r_knee)
                    l_angle=self.calculate_angle(l_shoulder,l_hip,l_knee)
                    
                    #Calculate angle
                    r_angle=self.calculate_angle(r_shoulder,r_hip,r_knee)
                    l_angle=self.calculate_angle(l_shoulder,l_hip,l_knee)
                    
                    #Visualize
                    cv2.putText(image,str(int(r_angle)),
                                tuple(np.multiply(r_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    cv2.putText(image,str(int(l_angle)),
                                tuple(np.multiply(l_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
            #------     
                    cv2.ellipse(image, tuple(np.multiply( r_knee,[self.img_w,self.img_h]).astype(int)), (50,50), 45, 0, 360, (0, 255, 255), 5)
                                        
                    state, startTime=self.point_touch(state,startTime,'knee',landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value],landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])
                    
                    if state=='continue':
                        #print(round(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,2),' ',round(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y,2),'  ',round(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,2),' ',round(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,2))
                        if abs(round(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y,2)\
                            -round(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,2))<0.05\
                                and (r_angle>90 and r_angle<130 and self.stage=="up")or(l_angle>90 and l_angle<130 and self.stage=="up"):
                            self.stage="down"
                            self.glutebridge_counter+=1
                            if self.user != 'visitor' and self.user != 'googleuser':
                                db.updateData(self.today,self.user,self.squat_counter,self.glutebridge_counter,self.lunge_counter)
                            self.sound_channel_0.play(pygame.mixer.Sound(self.countUp_sound))#計數增加音樂
                            self.sound_channel_0.set_volume(self.countUp_volumn)#計數增加音樂之音量
                            self.count_display(0)
                        if r_angle>160 or l_angle>160:
                            self.stage="up"
                    
                    if state=='stop':
                        cv2.putText(image, 'PAUSE',
                                    (int(frame.shape[1]*0.3),int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                                    cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA)  # 加入文字
                        
                    r_shoulder=[landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    l_shoulder=[landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    r_elbow=[landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    l_elbow=[landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    l_shoulder=self.calculate_angle(l_hip,l_shoulder,l_elbow)
                    r_shoulder=self.calculate_angle(r_hip,r_shoulder,r_elbow)
                    if l_shoulder>85 and r_shoulder>85 and l_angle>150 and r_angle>150: #判斷是否進入動作選擇
                        self.switchPose('glutebridge')
                        break
                    
                except:
                    pass
                
                #Render Curl Counter
                #Setup status box
                #透過cv2讓計數顯示於影像上
                #讓計數處於左上角(圖像,矩形.的起點,矩形的端點,顏色,線寬)這裡是做框架
                cv2.rectangle(image,(0,0),(300,73),(245,117,16),-1)
                
                #Rep data
                cv2.putText(image,'REPS',(15,12),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA) #
                cv2.putText(image,str(self.glutebridge_counter),
                            (10,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                #stage data
                cv2.putText(image,'stage',(140,12),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
                cv2.putText(image,self.stage,(140,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                
                #Render detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            
                #cv2.imshow('frame', image)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.stream.imgtk = imgtk
                self.stream.configure(image=imgtk)
                #self.stream.after(15, self.show_frame)
                self.stream.update()
                self.cam_size(image)
            
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            #self.switchPose('glutebridge')
        #self.cap.release() #釋放webcam
        #cv2.destroyAllWindows() #關閉視窗
    
    def lunge(self,state):
        global lunge_counter
        speakconut=1
        #self.counter=0
        self.stage=None
        self.poseAngle=True
        #導入畫圖工具
        self.mp_drawing = mp.solutions.drawing_utils
        #導入姿勢估計模型
        self.mp_pose = mp.solutions.pose
        if state!='continue': state='start'
        startTime=0
        isWrongPose=False
        
        if(self.cap==None): self.cap = cv2.VideoCapture(0)#cap=第一鏡頭,VC物件會連接到第一攝影機
        with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as self.pose:
            while(self.poseAngle):
                ret, frame = self.cap.read()
                #畫面大小控制
                frame = cv2.resize(frame, (self.img_w,self.img_h))
                frame = cv2.flip(frame,1) #影像反轉                            
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                #Make detection
                results = self.pose.process(image)
            
                #Recolor back to BGR (RGB TO BGR)
                image.flags.writeable = True
                image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            
                #Extract landmarks
                try:
                    landmarks=results.pose_landmarks.landmark
                    #Get coordinates
                    #前腳 右膝(m左膝)
                    r_hip=[landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    r_knee=[landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    r_ankle=[landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    #弓步 上半身過度前傾 左側(m的右側) 前腳是右、m的左腳
                    l_shoulder=[landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    l_hip=[landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    l_knee=[landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    #前腳是左(m右)
                    l_ankle=[landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    r_shoulder=[landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                     
                    #觸碰頭的部位
                    nose=[landmarks[self.mp_pose.PoseLandmark.NOSE.value].x,landmarks[self.mp_pose.PoseLandmark.NOSE.value].y]
                    
                    #Calculate angle
                    f_r_angle=self.calculate_angle(r_hip,r_knee,r_ankle)#前腳 右膝(m左膝)
                    l_angle_worst=self.calculate_angle(l_shoulder,l_hip,l_knee)#弓步 上半身過度前傾 左側(m的右側) 前腳是右、m的左腳
                    f_l_angle=self.calculate_angle(l_hip,l_knee,l_ankle)#前腳 左膝(m右膝)
                    r_angle_worst=self.calculate_angle(r_shoulder,r_hip,r_knee)#弓步 上半身過度前傾 右側(m的左側) 前腳是左、m的右腳
                    
                    
                    #Visualize
                    #畫面and實際左膝，程式碼要寫右
                    
                    cv2.putText(image,str(int(f_r_angle)),
                                tuple(np.multiply(r_knee,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                              )
                    
                    #弓步 上半身過度前傾 畫面右側右膝、程式碼要寫左
                    cv2.putText(image,str(int(l_angle_worst)),
                                tuple(np.multiply(l_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    #畫面and實際右膝，程式碼要寫左
                    cv2.putText(image,str(int(f_l_angle)),
                                tuple(np.multiply(l_knee,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                              )
                    #弓步 上半身過度前傾  畫面左側左膝、程式碼要寫右
                    
                    cv2.putText(image,str(int(r_angle_worst)),
                                tuple(np.multiply(r_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    
            #------
            
                    cv2.ellipse(image, tuple(np.multiply( nose,[self.img_w,self.img_h]).astype(int)), (50,50), 45, 0, 360, (0, 255, 255), 5)
                    
                    state, startTime=self.point_touch(state,startTime,'head',landmarks[self.mp_pose.PoseLandmark.NOSE.value],landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value],landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])
                    
                    if state=='continue':
                        
                        if f_r_angle<80 and r_angle_worst<120 and l_angle_worst<180 and self.stage=="down":#弓步_前膝太靠前
                            isWrongPose=True
                            self.worst_txt="左膝太靠前"
                            if self.s.isBusy()==False:
                                #print('ok')
                                t = threading.Thread(target=self.scraper,args=('左膝太靠前',))  #建立執行緒
                                t.start()  #執行
                            if speakconut!=0:
                                speakconut=0
                                t = threading.Thread(target=self.scraper,args=('左膝太靠前',))  #建立執行緒
                                t.start()  #執行
                        elif f_l_angle<80 and l_angle_worst<120 and r_angle_worst<180 and self.stage=="down":#弓步_前膝太靠前
                            isWrongPose=True
                            self.worst_txt="右膝太靠前"
                            if self.s.isBusy()==False:
                                #print('ok')
                                t = threading.Thread(target=self.scraper,args=('右膝太靠前',))  #建立執行緒
                                t.start()  #執行
                            if speakconut!=0:
                                speakconut=0
                                t = threading.Thread(target=self.scraper,args=('右膝太靠前',))  #建立執行緒
                                t.start()  #執行
                        elif ((l_angle_worst<170 and r_angle_worst<85)or(l_angle_worst<85 and r_angle_worst<170)) and self.stage=="down":
                            isWrongPose=True
                            self.worst_txt="上半身前傾"
                            print (self.s.isBusy())
                            if self.s.isBusy()==False:
                                #print('ok')
                                t = threading.Thread(target=self.scraper,args=('上半身前傾',))  #建立執行緒
                                t.start()  #執行
                            if speakconut!=0:
                                speakconut=0
                                t = threading.Thread(target=self.scraper,args=('上半身前傾',))  #建立執行緒
                                t.start()  #執行
                        else:
                            self.worst_txt=""
                            #Curl Counter logic
                            #---前腳-畫面and實際左膝，程式碼要寫右
                            if (f_r_angle<100 and f_r_angle>=90)or (f_l_angle<100 and f_l_angle>=90):
                                self.stage="down"
                            if (f_r_angle>160 and f_l_angle>160 and self.stage=="down")or(f_l_angle>160 and f_r_angle>160 and self.stage=="down"):
                                self.stage="up"
                                if isWrongPose != True:
                                    self.lunge_counter+=1
                                    if self.user != 'visitor' and self.user != 'googleuser':
                                        db.updateData(self.today,self.user,self.squat_counter,self.glutebridge_counter,self.lunge_counter)
                                    self.sound_channel_0.play(pygame.mixer.Sound(self.countUp_sound))#計數增加音樂
                                    self.sound_channel_0.set_volume(self.countUp_volumn)#計數增加音樂之音量
                                    self.count_display(1)
                                    #print(counter)
                                isWrongPose=False
                            
                    if state=='stop':
                        cv2.putText(image, 'PAUSE',
                                    (int(frame.shape[1]*0.3),int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                                    cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA)  # 加入文字
                        
                    r_elbow=[landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    l_elbow=[landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    angle_l_shoulder=self.calculate_angle(l_hip,l_shoulder,l_elbow)
                    angle_r_shoulder=self.calculate_angle(r_hip,r_shoulder,r_elbow)
                    l_angle=self.calculate_angle(l_shoulder,l_hip,l_knee) #腰角度
                    r_angle=self.calculate_angle(r_shoulder,r_hip,r_knee)
                    #print(l_shoulder,' ',r_shoulder)
                    if angle_l_shoulder>85 and angle_r_shoulder>85 and l_angle>150 and r_angle>150: #判斷是否進入動作選擇
                        self.switchPose('lunge')
                except:
                    pass
                #Render Curl Counter
                #Setup status box
                #透過cv2讓計數顯示於影像上
                #讓計數處於左上角(圖像,矩形的起點,矩形的端點,顏色,線寬)這裡是做框架
                cv2.rectangle(image,(0,0),(300,73),(245,117,16),-1)
                
                #Rep data
                cv2.putText(image,'REPS',(15,12),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA) #
                cv2.putText(image,str(self.lunge_counter),
                            (10,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                #stage data
                cv2.putText(image,'stage',(140,12),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
                cv2.putText(image,self.stage,(140,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                
                #錯誤輸出
                try:
                    output=self.cv2AddChineseText(image,self.worst_txt, (int(frame.shape[1]*0.25),int(frame.shape[0]*0.4)+10),(0,0,0),70)
                    #cv2.putText(image,self.worst_txt,
                    #            (int(frame.shape[1]*0.15),int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                    #            cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),5,cv2.LINE_AA)
                except:
                    output=image
                
                #Render detections
                self.mp_drawing.draw_landmarks(output, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
            
                #cv2.imshow('frame', image)
                image = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.stream.imgtk = imgtk
                self.stream.configure(image=imgtk)
                #self.stream.after(15, self.show_frame)
                self.stream.update()
                self.cam_size(image)
            
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
        #self.cap.release() #釋放webcam
        #cv2.destroyAllWindows() #關閉視窗
    
    def squat(self,state):
        global squat_counter
        speakconut=1
        #self.counter=0
        self.stage=None
        self.poseAngle=True
        #導入畫圖工具
        self.mp_drawing = mp.solutions.drawing_utils
        #導入姿勢估計模型
        self.mp_pose = mp.solutions.pose
        if(self.cap==None): self.cap = cv2.VideoCapture(0)#cap=第一鏡頭,VC物件會連接到第一攝影機
        #取得label寬高
        #self.label_w=self.stream.winfo_width() #label_width
        #self.label_h=self.stream.winfo_height() #label_height
        if state!='continue': state='start'
        startTime=0
        isWrongPose=False
        
        with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as self.pose:
            while(self.poseAngle):
                ret, frame = self.cap.read()
                #畫面大小控制
                frame = cv2.resize(frame, (self.img_w,self.img_h))
                frame = cv2.flip(frame,1) #影像反轉
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                #Make detection
                results = self.pose.process(image)
            
                #Recolor back to BGR (RGB TO BGR)
                image.flags.writeable = True
                image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            
                #Extract landmarks
                try:
                    landmarks=results.pose_landmarks.landmark
              #-----此處能將特定角度渲染到影像內，如想更改計算的角度只需注意中點，更改三個關節的參數
                    #Get coordinates
                    #畫面實際左腳，程式要寫右腳
                    r_hip=[landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    r_knee=[landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    r_ankle=[landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    #畫面實際右腳，程式要寫左腳
                    l_hip=[landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    l_knee=[landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    l_ankle=[landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    #前傾
                    l_shoulder=[landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    r_shoulder=[landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                     
                    #觸碰頭的部位
                    nose=[landmarks[self.mp_pose.PoseLandmark.NOSE.value].x,landmarks[self.mp_pose.PoseLandmark.NOSE.value].y]
                    
                    #Calculate angle
                    
                    
                    #Calculate angle
                    r_angle=self.calculate_angle(r_hip,r_knee,r_ankle)
                    l_angle=self.calculate_angle(l_hip,l_knee,l_ankle)
                    #前傾用
                    l_angle_worst=self.calculate_angle(l_shoulder,l_hip,l_knee)
                    r_angle_worst=self.calculate_angle(r_shoulder,r_hip,r_knee)
                    
                    #Visualize
                    cv2.putText(image,str(int(r_angle)),
                                tuple(np.multiply(r_knee,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                              )
                    cv2.putText(image,str(int(l_angle)),
                                tuple(np.multiply(l_knee,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                              )                    
                    #前傾
                    cv2.putText(image,str(int(l_angle_worst)),
                                tuple(np.multiply(l_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                    cv2.putText(image,str(int(r_angle_worst)),
                                tuple(np.multiply(r_hip,[self.img_w,self.img_h]).astype(int)),#使用數組乘法抓肘座標以網路攝像頭尺寸640*480速度通過
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA#次數輸出跟字體顏色
                               )
                              
                    cv2.ellipse(image, tuple(np.multiply( nose,[self.img_w,self.img_h]).astype(int)), (50,50), 45, 0, 360, (0, 255, 255), 5)
                    state, startTime=self.point_touch(state,startTime,'head',landmarks[self.mp_pose.PoseLandmark.NOSE.value],landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value],landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])
                              
            #------     
                    if state=='continue':
                        if l_angle_worst<70 or r_angle_worst<70 and self.stage=="down":
                            isWrongPose=True
                            self.worst_txt="上半身前傾"
                            if self.s.isBusy()==False:
                                print('ok')
                                t = threading.Thread(target=self.scraper,args=('上半身前傾',))  #建立執行緒
                                t.start()  #執行
                            if speakconut!=0:
                                speakconut=0
                                t = threading.Thread(target=self.scraper,args=('上半身前傾',))  #建立執行緒
                                t.start()  #執行
                            #t = threading.Thread(target=self.scraper,args=('上半身前傾',))  #建立執行緒
                            #t.start()  #執行
                        else:
                            self.worst_txt=""
                            #Curl Counter logic
                            if r_angle<100 and l_angle<100:
                                self.stage="down"
                            if (r_angle>160 and l_angle>160) and self.stage=="down":
                                self.stage="up"
                                if isWrongPose != True:
                                    self.squat_counter+=1
                                    if self.user != 'visitor':
                                        db.updateData(self.today,self.user,self.squat_counter,self.glutebridge_counter,self.lunge_counter)
                                    self.sound_channel_0.play(pygame.mixer.Sound(self.countUp_sound))#計數增加音樂
                                    self.sound_channel_0.set_volume(self.countUp_volumn)#計數增加音樂之音量
                                    self.count_display(2)
                                isWrongPose=False
                        
                    if state=='stop':
                        cv2.putText(image, 'PAUSE',
                                    (int(frame.shape[1]*0.3),int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                                    cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA)  # 加入文字
                    
                    r_elbow=[landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    l_elbow=[landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    angle_l_shoulder=self.calculate_angle(l_hip,l_shoulder,l_elbow)
                    angle_r_shoulder=self.calculate_angle(r_hip,r_shoulder,r_elbow)
                    l_angle=self.calculate_angle(l_shoulder,l_hip,l_knee) #腰角度
                    r_angle=self.calculate_angle(r_shoulder,r_hip,r_knee)
                    if angle_l_shoulder>85 and angle_r_shoulder>85 and l_angle>150 and r_angle>150: #判斷是否進入動作選擇
                        self.switchPose('squat')
                except:
                    pass
                #Render Curl Counter
                #Setup status box
                #透過cv2讓計數顯示於影像上
                #讓計數處於左上角(圖像,矩形的起點,矩形的端點,顏色,線寬)這裡是做框架
                cv2.rectangle(image,(0,0),(300,73),(245,117,16),-1)
                
                #Rep data
                cv2.putText(image,'REPS',(15,12),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA) #
                cv2.putText(image,str(self.squat_counter),
                            (10,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                #stage data
                cv2.putText(image,'stage',(140,12),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
                cv2.putText(image,self.stage,(140,60),
                            cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                
                try:
                    output=self.cv2AddChineseText(image,self.worst_txt, (int(frame.shape[1]*0.25),int(frame.shape[0]*0.4)+10),(0,0,0),70)
                #cv2.putText(image,self.worst_txt,
                #            (int(frame.shape[1]*0.15),int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                #            cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),5,cv2.LINE_AA)
                except:
                    output=image
                
                #Render detections
                self.mp_drawing.draw_landmarks(output, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
                
                #cv2.imshow('frame', image)
                #image=self.cv2AddChineseText(image,"膝蓋前傾", (123, 123))
                image = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.stream.imgtk = imgtk
                self.stream.configure(image=imgtk)
                #self.stream.after(15, self.show_frame)
                self.stream.update()
                self.cam_size(image)
                
                #print('Label長: ',self.stream.winfo_width())
                #print('Label高: ',self.stream.winfo_height())
                #print('img長: ',image.shape[1])
                #print('img高: ',image.shape[0])
            
                #if cv2.waitKey(10) & 0xFF == ord('q'):
                #    break
        #self.cap.release() #釋放webcam
        #cv2.destroyAllWindows() #關閉視窗
    
    def cam_size(self,img): #640/480:480=>1.3:1
        global img_w
        global img_h
        r=4
        self.img_w=img.shape[1] #self.img_width
        self.img_h=img.shape[0] #img_height
        self.label_w=self.stream.winfo_width() #label_width
        self.label_h=self.stream.winfo_height() #label_height
        if self.label_w < self.img_w or self.label_h < self.img_h:
            if self.label_w < self.img_w:
                self.img_w=self.label_w-r #新的img寬
                self.img_h=int(self.img_w*(self.frameHeight/self.frameWidth)) #新的img高
                img = cv2.resize(img, (self.img_w,self.img_h))
            else:
                self.img_h=self.label_h-r #新的img寬
                self.img_w=int(self.img_h*(self.frameWidth/self.frameHeight)) #新的img高
                img = cv2.resize(img, (self.img_w,self.img_h))
        if self.label_w >= self.img_w and self.label_h >= self.img_h:
            if self.label_w>self.label_h:
                self.img_h=self.label_h-r #新的img寬
                self.img_w=int(self.img_h*(self.frameWidth/self.frameHeight)) #新的img高
            else:
                self.img_w=self.label_w-r #新的img寬
                self.img_h=int(self.img_w*(self.frameHeight/self.frameWidth)) #新的img高
            img = cv2.resize(img, (self.img_w,self.img_h))
        #print(self.img_w,' ',self.img_h)
        return img
    
    def play_or_stop_music(self):
        self.resumePause_music_btn.state(["!disabled"])   # visiable the button.
        self.scale.state(["!disabled"])   # visiable the button.
        #print(pygame.mixer.music.get_busy())
        if pygame.mixer.music.get_busy():
            self.stop_bgm("event")
        else: self.play_bgm("event")
        
    def resume_or_pause_music(self):
        #print(pygame.mixer.music.get_busy())
        if pygame.mixer.music.get_busy():
            self.pause_bgm("event")
        else: self.resume_bgm("event")
        #print(pygame.mixer.music.get_pos())
        
    def pause_bgm(self,event):    #暫停bgm
        pygame.mixer.music.pause()
        
    def resume_bgm(self,event):   #繼續播放bgm
        #print(pygame.mixer.music.get_busy())
        pygame.mixer.music.unpause() 
        #print(pygame.mixer.music.get_busy())
        
    def set_bgm_volume(self,v):   #bgm音量
        pygame.mixer.music.set_volume(v)    #0~1之間float
        #print(v)
    
    def play_bgm(self,event):#,event   #播放bgm
        #print(pygame.mixer.music.get_busy())
        global first_voice_on
        pygame.mixer.music.load(self.bgm)
        pygame.mixer.music.play(-1)  #play(n)=念n次，play(-1)=念無限次
        if self.first_voice_on: #第一次開啟介面，音量設為0
            self.set_bgm_volume(self.first_voice_on_value)
            self.first_voice_on=False
        
    def stop_bgm(self,event):   #停止bgm
        pygame.mixer.music.stop()      
    
    def close_window(self):
        self.stop_bgm('event')
        if self.cap != None: self.cap.release()
        cv2.destroyAllWindows()
    
    def click(self):
        self.btn['style']='C.TButton'
        
    def end_exercise(self):
        self.stop_bgm('event')
        self.poseAngle=False
        if(self.cap!=None): self.cap=None
        self.stream.configure(image="")#將圖像移除呈現說明文字
        self.stream.update()
        print(self.poseAngle)
        #for i in range(1): self.end_exercise()
        
    def xFunc1(self,event):
        print(f"事件觸發鍵盤輸入:{event.char},對應的ASCII碼:{event.keycode}")
        
    def count_display(self, i):
        if i==0:
            self.glutebridge_total['text']="橋臀: " + str(self.glutebridge_counter) + "下；消耗: " + str(Decimal(0.3 * self.glutebridge_counter).quantize(Decimal('.00'), ROUND_HALF_UP))  + "卡"
        elif i==1:
            self.lung_total['text']="弓步蹲: " + str(self.lunge_counter) + "下；消耗: " + str(Decimal(0.5 * self.lunge_counter).quantize(Decimal('.00'), ROUND_HALF_UP))  + "卡"
        else:       
            self.squat_total['text']="深蹲: " + str(self.squat_counter) + "下；消耗: " + str(Decimal(0.32 * self.squat_counter).quantize(Decimal('.00'), ROUND_HALF_UP))  + "卡"            
        if i==5:
            self.glutebridge_total['text']="橋臀: " + str(self.glutebridge_counter) + "下；消耗: " + str(Decimal(0.3 * self.glutebridge_counter).quantize(Decimal('.00'), ROUND_HALF_UP))  + "卡"
            self.lung_total['text']="弓步蹲: " + str(self.lunge_counter) + "下；消耗: " + str(Decimal(0.5 * self.lunge_counter).quantize(Decimal('.00'), ROUND_HALF_UP))  + "卡"
            self.squat_total['text']="深蹲: " + str(self.squat_counter) + "下；消耗: " + str(Decimal(0.32 * self.squat_counter).quantize(Decimal('.00'), ROUND_HALF_UP))  + "卡" 
            
        self.cal_total['text']="總共消耗: " + str(Decimal(0.3 * self.glutebridge_counter).quantize(Decimal('.00'), ROUND_HALF_UP) + Decimal(0.5 * self.lunge_counter).quantize(Decimal('.00'), ROUND_HALF_UP) + Decimal(0.32 * self.squat_counter).quantize(Decimal('.00'), ROUND_HALF_UP)) + "卡"
    
    def go_glutebridge(self):
        Custom_font = tkFont.Font(family='Helvetica', size=20)#, weight='bold', underline=1, overstrike=1
        Accentbutton = ttk.Style()
        Accentbutton.configure("Accentbutton", font=Custom_font, width=10)
        
        self.btn['style']='TButton'
        self.btn2['style']='Accentbutton'
        self.btn2.focus()
        self.btn3['style']='TButton'
        self.glutebridge('start')
    
    def go_squat(self):
        Custom_font = tkFont.Font(family='Helvetica', size=20)#, weight='bold', underline=1, overstrike=1
        Accentbutton = ttk.Style()
        Accentbutton.configure("Accentbutton", font=Custom_font, width=10)
        b1 = ttk.Style()
        b1.configure("TButton", font=('Helvetica', 20), width=10)
        self.btn['style']='Accentbutton'
        self.btn.focus()
        self.btn2['style']='TButton'
        self.btn3['style']='TButton'
        self.squat('start')
    
    def go_lunge(self):
        Custom_font = tkFont.Font(family='Helvetica', size=20)#, weight='bold', underline=1, overstrike=1
        Accentbutton = ttk.Style()
        Accentbutton.configure("Accentbutton", font=Custom_font, width=10)
        
        self.btn['style']='TButton'
        self.btn2['style']='TButton'
        self.btn3['style']='Accentbutton'
        self.btn3.focus()
        '''print(self.btn1['style'])
        print(self.btn2['style'])
        print(self.btn3['style'])'''
        self.lunge('start')
    
    def __init__(self, master):
        global g, squat_counter, glutebridge_counter, lunge_counter, user
        tk.Frame.__init__(self, master)
        
        filepath = r".credentials/cred.json"
        if os.path.isfile(filepath):
            self.user = 'googleuser'
            self.userinfo_database = Main_data()
            self.onlyuser_database = GoogleSheets()
            self.user_email = self.userinfo_database.get_user_info()
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )
            squat_counter, glutebridge_counter, lunge_counter =self.userinfo_database.get_today_times(
                spreadsheetId=self.user_sheetId, 
                range="工作表1", 
                date=str(datetime.date.today()))
            self.squat_counter = int(squat_counter)
            self.glutebridge_counter = int(glutebridge_counter)
            self.lunge_counter = int(lunge_counter)
        
        #確認使用者
        if self.user != 'googleuser':
            self.user=db.user
            #載入次數
            if db.dataExist(self.today,self.user) == 0:
                db.insertData(self.today, self.user, 0, 0, 0)    
            date, username, self.squat_counter, self.glutebridge_counter, self.lunge_counter = db.showDataByDate(self.today,self.user)
        
        # Window setup
        root.title('健體端勢')
        #WIDTH, HEIGHT = 820, 500
        #INITIAL_X_POSITION, INITIAL_Y_POSITION = 450, 200
        #root.geometry(f'{frameWidth}x{frameHeight}+{INITIAL_X_POSITION}+{INITIAL_Y_POSITION}')
        
        memberName=self.user
        if self.user == 'googleuser':
            try:            
                self.userinfo_database = Main_data()
                memberName = self.userinfo_database.get_user_info().split('@')[0]
            except Exception as err:
                print("error:")
                print(err)
                
        if len(self.user)>10:
            memberName=self.user[:10]+'...'
        # Creating Menubar
        menubar = tk.Menu(root)
        # Adding setting Menu and commands
        userOpt = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = memberName, menu = userOpt)
        userOpt.add_command(label ='切換使用者', command = self.switchUser)#self.inputData
        userOpt.add_separator()
        userOpt.add_command(label = self.user, command = None)#self.inputData
        operate = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='功能', menu = operate)
        if self.user!="visitor":
            operate.add_command(label ='歷史紀錄', command=self.showTable)#self.inputData
            operate.add_command(label ='分析報告', command=self.showAnalyses)#self.inputData
        operate.add_command(label ='今日計數歸零', command = self.resetCounter)
        setting = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='鏡頭', menu = setting)
        setting.add_command(label ='鏡頭0', command=self.changeWeb0)#self.inputData
        setting.add_command(label ='鏡頭1', command=self.changeWeb1)#self.inputData
        setting.add_command(label ='鏡頭2', command=self.changeWeb2)#self.inputData
        #setting.add_separator()
        #setting.add_command(label ='離開', command = root.destroy)
        # display Menu
        root.config(menu = menubar)
        def Exit(self):
            root.destroy
        
        style = ttk.Style(root)
        style.theme_use('azure')
        #root.tk.call('source', './azure dark/azure dark.tcl')   #使用azure dark風格
        default_font = tkFont.nametofont("TkDefaultFont")  #改原本預設的字型
        default_font.configure(family='Helvetica', size=15)
        b1 = ttk.Style()
        b1 = ttk.Style()
        b2 = ttk.Style()
        f1 = ttk.Style()
        f2 = ttk.Style()
        f3 = ttk.Style()
        voice_labelframe = ttk.Style()
        
        #'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
        b1.theme_use('azure')
        
        b1.configure("TButton", font=('Helvetica', 20), width=10)#, background='#d4b05a'
        b2.configure("C.TButton", width=8,font=('Helvetica', 15))#, background="blue"
        f1.configure("f1.TFrame", relief='groove')#, background='#d4b05a'
        f2.configure("f2.TFrame", relief='groove')#, background='pink'
        f3.configure("stream.TFrame", background='yellow', relief='groove')
        voice_labelframe.configure('voice.TLabelframe.Label', font=('Helvetica', 15, 'bold'), foreground='white')#, background='white'
        #Scale.configure("TScale", background="pink")
        
        b1.map('TButton', background=[('active', '#ff0000'), ('disabled', '#4c4c4c')])
        
        frame1 = ttk.Frame(style="f1.TFrame", padding=10)
        self.frame2 = ttk.Frame(style="f2.TFrame", padding=10)
        #音樂相關之框線LabelFrame
        self.music_label_Frame = ttk.LabelFrame(self.frame2, text='音量調整', labelanchor='n', style='voice.TLabelframe')
        #self.stream = ttk.Frame(root,style="stream.TFrame", padding=10, width=640, height=480)
        self.stream=ttk.Label(root,text="鏡頭尚未開啟，請點選【開始】或直接選擇動作!", font=('Helvetica', 25), foreground="white", anchor=tk.CENTER)#,background="blue", padding=10)
        
        self.btn = ttk.Button(frame1, text='深蹲', command=self.go_squat)
        self.btn2 = ttk.Button(frame1,text='臀橋', command=self.go_glutebridge)
        self.btn3 = ttk.Button(frame1,text='弓步蹲', command=self.go_lunge)
        self.btn4 = ttk.Button(self.frame2, text='開始', command=self.show_webcam)
        self.btn5 = ttk.Button(self.frame2,text='結束', command=self.end_exercise)
        self.sep1 = ttk.Separator(self.frame2, orient='horizontal')
        self.bgm_text=ttk.Label(self.music_label_Frame, text="背景音樂", font=('Helvetica', 15), foreground="white", anchor=tk.W)#,background="blue", padding=10)
        #self.sep2 = ttk.Separator(self.music_label_Frame, orient='horizontal')
        self.playStop_music_btn = ttk.Button(self.music_label_Frame,text='播放/停止', style='C.TButton', command=self.play_or_stop_music) #command如有打括號eg.self.play_bgm()，表示一開始會直接執行動作一遍，之後不會再執行
        self.resumePause_music_btn = ttk.Button(self.music_label_Frame,text='繼續/暫停', style='C.TButton', command=self.resume_or_pause_music, )
        self.countUp_text=ttk.Label(self.music_label_Frame, text="計數音效", font=('Helvetica', 15), foreground="white", anchor=tk.W)#,background="blue", padding=10)
        self.sep3 = ttk.Separator(self.music_label_Frame, orient='horizontal')
        self.lung_total=ttk.Label(self.frame2, text="弓步蹲: " + str(self.lunge_counter) + "下；消耗: " + str(0.32 * self.lunge_counter)  + "卡", font=('Helvetica', 17), foreground="white", anchor=tk.W)#,background="blue", padding=10)
        self.squat_total=ttk.Label(self.frame2, text="   深蹲: " + str(self.squat_counter) + "下；消耗: " + str(0.32 * self.squat_counter)  + "卡", font=('Helvetica', 17), foreground="white", anchor=tk.W)#,background="blue", padding=10)
        self.glutebridge_total=ttk.Label(self.frame2, text="   橋臀: " + str(self.glutebridge_counter) + "下；消耗: " + str(0.32 * self.glutebridge_counter)  + "卡", font=('Helvetica', 17), foreground="white", anchor=tk.W)#,background="blue", padding=10)
        self.cal_total=ttk.Label(self.frame2, text="總共消耗: " + str(0.3 * self.glutebridge_counter + 0.5 * self.lunge_counter + 0.32 * self.squat_counter) + "卡" , font=('Helvetica', 17), foreground="white", anchor=tk.W )
        #音量圖片
        # Create a photoimage object of the image in the path
        volumnOFF_img = Image.open(self.voice_OFF)
        self.volumnOFF = ImageTk.PhotoImage(volumnOFF_img.resize((50, 50), Image.ANTIALIAS))
        volumnON_img = Image.open(self.voice_ON)
        self.volumnON = ImageTk.PhotoImage(volumnON_img.resize((50, 50), Image.ANTIALIAS))
        self.bgm_img = ttk.Label(self.music_label_Frame, image=self.volumnOFF)
        self.countUp_img = ttk.Label(self.music_label_Frame, image=self.volumnOFF)
        #self.bgm_img.image = self.volumnOFF
        
        self.resumePause_music_btn.state(["disabled"])   # Disable the button.
        
        self.stream.grid(row=1,column=0,pady=1,padx=1,sticky=('N','E','W','S'))
        frame1.grid(row=0,column=0,sticky=('N','E','W'))
        self.frame2.grid(row=0,column=1,rowspan=2,sticky=('N','E','W','S'))        
        #frame1裡
        self.btn.grid(row=0, column=0, ipadx=10, ipady=10, padx=10)
        self.btn2.grid(row=0, column=1, ipadx=10, ipady=10, padx=10)
        self.btn3.grid(row=0, column=2, ipadx=10, ipady=10, padx=10)
        #frame2裡
        self.btn4.grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=20)
        self.btn5.grid(row=0, column=1, ipadx=10, ipady=15, padx=10, pady=20)
        self.sep1.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        self.music_label_Frame.grid(row=2, column=0, columnspan=3, rowspan=3, padx=10, pady=20)#, ipadx=10
        self.bgm_text.grid(row=0, column=0, ipadx=10, ipady=1, padx=2)
        #self.sep2.grid(row=1, column=0, columnspan=3, sticky="ew", pady=10, padx=15)
        self.playStop_music_btn.grid(row=0, column=1, ipadx=10, ipady=10, padx=10, pady=10)
        self.resumePause_music_btn.grid(row=0, column=2, ipadx=10, ipady=10, padx=10, pady=10)
        self.bgm_img.grid(row=3, column=0)#, columnspan=2, ipadx=10
        self.sep3.grid(row=4, column=0, columnspan=3, sticky="ew", pady=20, padx=15)
        self.countUp_text.grid(row=5, column=0, ipadx=10, ipady=1, padx=10)
        self.countUp_img.grid(row=6, column=0)#, columnspan=2, ipadx=10
        self.lung_total.grid(row=7, column=0, columnspan=2, padx=10, pady=10,sticky=('W'))
        self.squat_total.grid(row=8, column=0, columnspan=2, padx=10, pady=10,sticky=('W'))
        self.glutebridge_total.grid(row=9, column=0, columnspan=2, padx=10, pady=10,sticky=('W'))
        self.cal_total.grid(row=10, column=0, columnspan=2, padx=10, pady=10,sticky=('W'))
        
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        self.music_label_Frame.grid_columnconfigure(0, minsize=10)
        self.music_label_Frame.grid_columnconfigure(1, minsize=100)
        self.music_label_Frame.grid_rowconfigure(0, minsize=10) #music_label_Frame高度
        
        def scale(i):
            global countUp_volumn
            self.set_bgm_volume(int(self.scale.get())/100)
            self.countUp_volumn=int(self.scale2.get())/100
            if int(self.scale.get())>5:
                self.bgm_img['image']=self.volumnON
            else:
                self.bgm_img['image']=self.volumnOFF
            if int(self.scale2.get())>5:
                self.countUp_img['image']=self.volumnON
            else:
                self.countUp_img['image']=self.volumnOFF
            #self.bgm_img.grid(row=4, column=1, columnspan=2)
            #print(int(self.scale.get()))
            
        Scale = ttk.Style()
        Scale.configure('my.Horizontal.TScale', foreground='white',troughcolor='#73B5FA')#, sliderlength=10, background='black'
        #scale = ttk.Scale(self.frame2, from_=100, to=0, length=120, style='TScale', variable=self.g, command=scale)
        self.scale = ttkw.TickScale(self.music_label_Frame, orient='horizontal', style='my.Horizontal.TScale', from_=0, to=100, tickinterval=20, resolution=10, showvalue=True, length=200, labelpos='n', command=scale)
        self.scale2 = ttkw.TickScale(self.music_label_Frame, orient='horizontal', style='my.Horizontal.TScale', from_=0, to=100, tickinterval=20, resolution=10, showvalue=True, length=200, labelpos='n', command=scale)
        self.scale.grid(row=3, column=1, columnspan=2, ipadx=10, ipady=10, padx=10)
        self.scale2.grid(row=6, column=1, columnspan=2, ipadx=10, ipady=10, padx=10)
        self.scale.state(["disabled"])   # Disable the button.
    
    def changeWeb0(self):
        self.cap = cv2.VideoCapture(0)
        
    def changeWeb1(self):
        self.cap = cv2.VideoCapture(1)
        
    def changeWeb2(self):
        self.cap = cv2.VideoCapture(2)
        
    def quit_savegoogledata(self):
        if self.user =='googleuser':
            self.userinfo_database = Main_data()
            self.user_email = self.userinfo_database.get_user_info()
            self.onlyuser_database = GoogleSheets()
            self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )           
            update_cell_num = self.userinfo_database.get_day_pos(
                spreadsheetId=self.user_sheetId,
                range='工作表1',
                date=str(datetime.date.today()),
                )
            update_cell = "B" + str(update_cell_num) + ":D" +str(update_cell_num)
            self.userinfo_database.updateSheet(
                spreadsheetId=self.user_sheetId, 
                range_name=update_cell, 
                df=[[self.squat_counter,self.glutebridge_counter,self.lunge_counter]]
                )
            
            squat_counter, glutebridge_counter, lunge_counter =self.userinfo_database.get_today_times(
                spreadsheetId=self.user_sheetId, 
                range="工作表1", 
                date=str(datetime.date.today()))
            root.destroy()
        else:root.destroy()
        
    def show_webcam(self):
        #導入畫圖工具
        self.mp_drawing = mp.solutions.drawing_utils
        #導入姿勢估計模型
        self.mp_pose = mp.solutions.pose
        
        self.model = load_model('90%_model.h5')
        self.model.summary()
        self.model.load_weights('90%_weights.h5')
        
        if(self.cap==None): self.cap = cv2.VideoCapture(0)#cap=第一鏡頭,VC物件會連接到第一攝影機
        
        #Curl Counter
        #self.counter=0#計數器
        self.stage=None#運動關節狀態(此例為人的手臂是處於彎舉上/下部)
        IMAGE_SIZE = (128, 128)
        all_predict_label=[] #所有預測張數(最多basePicAmount張)
        picNum = 0 #目前擷取張數
        repeatTime=1 #計算無法辨識所重複次數
        showCountDown=True #倒數計時器
        sec=4 #倒數起始秒數
        subtractSeconds=0.05 #每次減去的秒數
        basePicAmount=30 #取眾數時需大於的基本張數
        startEndGap=0.01
        self.poseAngle=True
        self.btn['style']='TButton'
        self.btn2['style']='TButton'
        self.btn3['style']='TButton'
        temTime=[]
        editTimeGap=True
        
        with self.mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as self.pose:
            #大字形偵測(以確認開始倒數)
            self.openArms()
            s=0
                
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                frame = cv2.flip(frame,1) #影像反轉
                
                #設定倒數3秒開始偵測
                while showCountDown==True:
                    ret, frame = self.cap.read()
                    frame = cv2.resize(frame, (self.img_w,self.img_h))
                    frame = cv2.flip(frame,1) #影像反轉
                    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    
                    sec-=subtractSeconds #每次減0.05秒
                    output = frame.copy()
                    cv2.putText(output, str(int(sec)),
                                (int(frame.shape[1]*0.5)-50,int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                                cv2.FONT_HERSHEY_SIMPLEX,5,(255,255,255),10,cv2.LINE_AA)  # 加入文字
                    if sec<1:
                        showCountDown=False
                        sec=3
                        break
                    if cv2.waitKey(1) == ord('q'):
                        showCountDown=False
                        break
                    #cv2.imshow('frame', output)
                    
                    #畫面大小控制
                    #output = cv2.resize(output, (self.img_w,self.img_h))
                    img = Image.fromarray(output)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.stream.imgtk = imgtk
                    self.stream.configure(image=imgtk)
                    #self.stream.after(15, self.show_frame)
                    self.stream.update()
                    self.cam_size(output)
                ###############
                
                #計時開始
                tStart = time.time()
                # 若按下 q 鍵則離開迴圈
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return
                
                self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #畫面大小控制
                self.image = cv2.resize(self.image, (self.img_w,self.img_h))
                #顯示圖片
                #cv2.imshow('frame', frame)                
                img = Image.fromarray(self.image)
                self.imgtk = ImageTk.PhotoImage(image=img)
                self.stream.imgtk = self.imgtk
                self.stream.configure(image=self.imgtk)
                #self.stream.after(15, self.show_frame)
                self.stream.update()
                self.cam_size(self.image)
                #計時結束
                tEnd = time.time()
                  
                gap = tEnd - tStart
                #print("gap: ",gap)
                #print("s: ",s)
                if editTimeGap and len(temTime)<11: temTime.append(round(gap,4))
                if editTimeGap and len(temTime)>=11:
                   temTime[0]=0
                   startEndGap=round(sum(temTime[1::])/(len(temTime)-1),4)
                   #print("startEndGap前: ",startEndGap)
                   editTimeGap=False
                   for n in range(0,5):
                       if startEndGap>10**-n:
                           #startEndGap+=5/10**n
                           break
                #print("startEndGap: ",startEndGap)
                #print("全部:",temTime)
                s=time.time()
                if gap > startEndGap: #0.01
                    frame=np.array(frame)
                    images = []
                    #cv讀照片，顏色莫認為BGR，需轉為RGB，錯誤表示黑白或已轉
                    self.image = cv2.resize(self.image, IMAGE_SIZE)
                    images.append(self.image)
                    images = np.array(images, dtype = 'float32')
                    images = images / 255.0
                    predictions = self.model.predict(images)
                    ############################################
                    #如果最高機率的動作仍小於0.7，則歸類此次為模糊動作label3(表三動作機率差不多)
                    for i in range(len(predictions)):
                        if max(predictions[i])<0.7:
                            pred_labels=3
                        else:
                            pred_labels = np.argmax(predictions, axis = 1)
                            pred_labels = pred_labels[0]
                    #################################################
                    print('目前重複次數: ',repeatTime)
                    print('目前擷取數: ',picNum)
                    print("當前動作: ",pred_labels)
                    all_predict_label.append(pred_labels)
                    print("目前累積: ",all_predict_label)
                    gap=0
                    picNum+=1
                  
                if picNum>=basePicAmount: #大於basePicAmount(30張)判斷什麼動作
                    from scipy import stats #取眾數套件
                    currentPose=3 #目前動作label
                    mode = stats.mode(all_predict_label) #所有動作之眾數
                    if(all_predict_label.count(mode[0])/basePicAmount < 0.6): currentPose=3
                    else: currentPose=mode[0]
                    print("眾數: ",mode[0])
                    
                    if(currentPose==0):
                        self.go_glutebridge()
                        break
                    elif(currentPose==1):
                        self.go_lunge()
                        break
                    elif(currentPose==2):
                        self.go_squat()
                        break
                    else:
                        #給予提示訊息告知動作無法被正確辨識，重新辨識執行三次都一樣則提供手動選擇
                        #設定倒數3秒開始偵測
                        if repeatTime>=3:
                            showCountDown=True
                            while True:
                                ret, frame = self.cap.read()
                                frame = cv2.flip(frame,1) #影像反轉
                                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                                sec-=0.02
                                output = frame.copy()
                                #(int(frame.shape[1]*0.5)-50,int(frame.shape[0]*0.5)+10)
                                cv2.rectangle(output,(int(frame.shape[1]*0.9),int(frame.shape[0]*0.4)),(int(frame.shape[1]*0.1),int(frame.shape[0]*0.6)),(52,50,51),-1) #img,右上,左下,實心
                                cv2.putText(output, 'please click START to repeat',
                                            (int(frame.shape[1]*0.15),int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                                            cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA)  # 加入文字
                                if sec<1:
                                    sec=4
                                    break
                                if cv2.waitKey(1) == ord('q'):
                                    break
                                #畫面大小控制
                                output = cv2.resize(output, (self.img_w,self.img_h))
                                #cv2.imshow('frame', output)
                                img = Image.fromarray(output)
                                imgtk = ImageTk.PhotoImage(image=img)
                                self.stream.imgtk = imgtk
                                self.stream.configure(image=imgtk)
                                #self.stream.after(15, self.show_frame)
                                self.stream.update()
                                self.cam_size(output)
                            break
                        else:
                            while True:
                                ret, frame = self.cap.read()
                                frame = cv2.flip(frame,1) #影像反轉
                                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                                sec-=0.01
                                output = frame.copy()
                                cv2.putText(output, 'Try Again',
                                            (int(frame.shape[1]*0.5)-150,int(frame.shape[0]*0.5)+10), #frame.shape[0]:垂直,frame.shape[1]:水平,frame.shape[2]:通道數
                                            cv2.FONT_HERSHEY_SIMPLEX,2.5,(255,255,255),10,cv2.LINE_AA)  # 加入文字
                                if sec<1:
                                    sec=4
                                    break
                                if cv2.waitKey(1) == ord('q'):
                                    break
                                #畫面大小控制
                                output = cv2.resize(output, (self.img_w,self.img_h))
                                #cv2.imshow('frame', output)
                                img = Image.fromarray(output)
                                imgtk = ImageTk.PhotoImage(image=img)
                                self.stream.imgtk = imgtk
                                self.stream.configure(image=imgtk)
                                #self.stream.after(15, self.show_frame)
                                self.stream.update()
                                self.cam_size(output)
                            ###############
                            repeatTime+=1
                            picNum = 0
                            showCountDown=True
                            all_predict_label=[]
        #self.cap.release() #釋放webcam
        #cv2.destroyAllWindows() #關閉視窗

class loginPage(tk.Frame):
    VISITOR_ACCOUNT='visitor'
    VISITOR_PASSWORD='visitor'
    
    filepath = r".credentials/cred.json"        
    if os.path.isfile(filepath):
        try:
            os.remove(filepath)
        except OSError as e:
            print(e)
        else:
            print("File is deleted successfully")
    else:
      print("google_creds檔案不存在。")
      
    def login(self):
        default_font = tkFont.nametofont("TkDefaultFont")  #改原本預設的字型
        default_font.configure(family='Helvetica', size=15)
        
        f1 = ttk.Style()
        bLogin = ttk.Style()
        f1.configure("f1.TFrame")#, background='#d4b05a'
        bLogin.configure("bLogin.TButton", font=('Helvetica', 15), width=4)
        #b1.map('TButton', background=[('active', '#ff0000'), ('disabled', '#4c4c4c')])
        
        root.title("健體端勢【登入/註冊】")
        login_frame = ttk.Frame(root,style="f1.TFrame")
        login_frame.grid(padx=15, pady=15)
        
        ttk.Label(login_frame, text='帳號:', anchor=tk.CENTER).grid(column=1, row=1, columnspan=2)
        self.account = ttk.Entry(login_frame)
        self.account.grid(column=3, row=1, columnspan=7, padx=10, pady=8, sticky='W')
        #account.insert(0, 'Entry')
        
        ttk.Label(login_frame, text='密碼:', anchor=tk.CENTER).grid(column=1, row=2, columnspan=2)
        self.password = ttk.Entry(login_frame, show='*')
        self.password.grid(column=3, row=2, columnspan=7, padx=10, pady=8, sticky='W')
        
        def reg():
            '''註冊'''
            account=self.account.get()
            password=self.password.get()
            if account=='' or password=='':
                msg['text']="*請輸入欲註冊帳號及密碼!"
                msg['foreground']='#ff4a4a'
            else:
                try:
                    if db.createAccount(account,password):
                        msg['text']="註冊成功! 請登入並開始使用:)"
                        msg['foreground']='white'
                    else:
                        msg['text']="*此帳號已存在!"
                        msg['foreground']='#ff4a4a'
                except Exception as e:
                    if int(str(e)[1:-1].split(',',1)[0]) == 1406:
                        msg['text']="*帳號及密碼長度需小於50!"
                        msg['foreground']='#ff4a4a'
                    else:
                        msg['text']="*資料格式錯誤"
                        msg['foreground']='#ff4a4a'
        
        def cert():    
            '''這裡需要驗證用戶名和密碼對不對,不對就跳出對話框告訴他,對就destroyee'''
            account=self.account.get()
            password=self.password.get()
            if account=='' or password=='':
                msg['text']="*請輸入正確的帳號及密碼!"
                msg['foreground']='#ff4a4a'
            else:
                if db.confirmAccount(account,password):
                    login_frame.destroy() #TREET
                else:
                    msg['text']="*請輸入正確的帳號及密碼:("
                    msg['foreground']='#ff4a4a'
                    
        def visit():
            db.confirmAccount(self.VISITOR_ACCOUNT,self.VISITOR_PASSWORD)
            login_frame.destroy() #TREET
            
        def google_login():
            self.userinfo_database = Main_data()
            self.userinfo_database.googleAPIService
            self.onlyuser_database = GoogleSheets()
            self.onlyuser_database.googleAPIService
            self.user_email = self.userinfo_database.get_user_info()
            filepath = r".credentials/cred.json"   
            if os.path.isfile(filepath):       
                login_frame.destroy()
                self.user_sheetId = self.onlyuser_database.getWorksheet(
                spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
                range='工作表1', 
                email=self.user_email,
                )
            if self.user_sheetId == False:
                self.onlyuser_database.appendWorksheet(
                        spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
                        range='工作表1',
                        df=pd.DataFrame(
                            {'email': [self.user_email],
                            'sheet_id': [self.userinfo_database.createsheet('exercise')],
                            }
                        )
                    )
                self.user_sheetId = self.onlyuser_database.getWorksheet(
                    spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
                    range='工作表1',
                    email=self.user_email,)
                
                print(self.userinfo_database.setWorksheet(
                    spreadsheetId=self.user_sheetId,
                    range='工作表1',
                    df=pd.DataFrame(
                        {'data': [str(datetime.date.today())],
                        'squat': [0],
                        'glute_bridge': [0],
                        'lunge': [0]},
                    )
                        )
                            )
            else:
                self.update_cell_num = self.userinfo_database.get_day_pos(
                    spreadsheetId=self.user_sheetId,
                    range='工作表1',
                    date=str(datetime.date.today()), #str(datetime.date.today())
                    )
                if self.update_cell_num == False:
                    self.userinfo_database.appendWorksheet(
                            spreadsheetId=self.user_sheetId,
                            range='工作表1',
                            df=pd.DataFrame(
                                {'data': [str(datetime.date.today())],
                                'squat': [0],
                                'glute_bridge': [0],
                                'lunge': [0],
                                }
                            )
                        )
            login_frame.destroy()
            
        #account=self.account.get()
        #password=account.get()
        msg=ttk.Label(login_frame, text='', anchor=tk.CENTER)
        msg.grid(column=1, row=4, columnspan=8)
        ttk.Button(login_frame,text='訪客',style='bLogin.TButton', command=visit).grid(column=1, row=3, columnspan=2, padx=10, pady=15)
        ttk.Button(login_frame,text='註冊',style='bLogin.TButton', command=reg).grid(column=3, row=3, columnspan=2, padx=10, pady=15)
        ttk.Button(login_frame,text='登入',style='bLogin.TButton', command=cert).grid(column=5, row=3, columnspan=2, padx=10, pady=15)
        ttk.Button(login_frame,text='Google',style='bLogin.TButton', command=google_login).grid(column=7, row=3, columnspan=2, padx=10, pady=15, ipadx=20)
        
        return login_frame #這裡一定要return
        

root = tk.Tk()
style = ttk.Style(root)
root.tk.call('source', './azure dark/azure dark.tcl')   #使用azure dark風格
style.theme_use('azure')

'''app = Application(root)
root.bind("<space>", app.play_bgm)
root.bind("<p>", app.pause_bgm)
root.bind("<r>", app.resume_bgm)
root.mainloop()
app.close_window()'''

if __name__ == "__main__":
    loginPage = loginPage(root)
    login = loginPage.login()
    try:#因為用戶可能直接關閉主窗口,所以我們要捕捉這個錯誤
        root.wait_window(window=login)#等待直到login銷毀,不銷毀後面的語句就不執行
        app = Application(root)
        root.bind("<space>", app.play_bgm)
        root.bind("<p>", app.pause_bgm)
        root.bind("<r>", app.resume_bgm )
        app()
    except Exception as err:
        print(err)
    root.protocol("WM_DELETE_WINDOW", app.quit_savegoogledata)
    root.mainloop()
    app.close_window()
