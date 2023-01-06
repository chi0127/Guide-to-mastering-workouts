from __future__ import print_function
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import requests
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from main import GoogleAPIClient
import datetime

class Main_data(GoogleAPIClient):
    
    SECRET_PATH = '.credentials/client_secret.json'
    CREDS_PATH = '.credentials/cred1.json'
    
    def __init__(self) -> None:
        # 呼叫 GoogleAPIClient.__init__()，並提供 serviceName, version, scope
        super().__init__(
            'sheets',
            'v4',
            ['openid','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/userinfo.email'
             ],
            '.credentials/cred.json'
        )
        
    def clearWorksheet(self, spreadsheetId: str, range: str):
        self.googleAPIService.spreadsheets().values().clear(
            spreadsheetId=spreadsheetId,
            range=range,
        ).execute()
        return 0

    def setWorksheet(self, spreadsheetId: str, range: str, df: pd.DataFrame):
        #self.clearWorksheet(spreadsheetId, range)
        self.googleAPIService.spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range=range,
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': df.T.reset_index().T.values.tolist()
            },
        ).execute()
        return 0
    
    def createsheet(self, title):
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".credentials/final-works-account.json"  
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            spreadsheet = self.googleAPIService.spreadsheets().create(body=spreadsheet,
                                       fields='spreadsheetId') \
                .execute()
            print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
            return spreadsheet.get('spreadsheetId')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
    def get_user_info(self):
            with open('.credentials/cred.json', 'r') as token:
                token = token.read().split(",")[0]
                token = token.split('"')[3]
                self.token = token
            address = "https://www.googleapis.com/oauth2/v2/userinfo?access_token="+self.token
            self.user_gmail = requests.get(address).text.split(",")[1].split('"')[3]
            return self.user_gmail

    def get_day_pos(self, spreadsheetId: str, range: str, date: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=range,
        )
        response = request.execute()        
        result = response['values']       
        count = 0
        for item in result:
            count += 1
            if date in item[0]: return count
        return False
        
    def updateSheet(self, spreadsheetId: str, range_name: str, df: list):
        self.googleAPIService.spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': df
            },
        ).execute()
        return print(df)
    
    def appendWorksheet(self, spreadsheetId: str, range: str, df: pd.DataFrame):
        self.googleAPIService.spreadsheets().values().append(
            spreadsheetId=spreadsheetId,
            range=range,
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': df.values.tolist()
            },
        ).execute()
        return 0
    
    def get_today_times(self, spreadsheetId: str, range: str, date: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=range,
        )
        response = request.execute()        
        result = response['values']       
        for item in result:
            if date in item[0]: return item[1],item[2],item[3]
        return False
    def get_date_times(self, spreadsheetId: str, range: str,sdate: str, edate: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=range,
        )
        response = request.execute()        
        result = response['values']  
        all_date = []
        real_date = []
        three_pose = []
        start = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(edate, '%Y-%m-%d').date()
        if result != None:
            for item in result[1::]:
                all_date.append(datetime.datetime.strptime(item[0], '%Y-%m-%d').date())
            alldate_df = pd.DataFrame(all_date)
            df1 = pd.DataFrame(alldate_df[(alldate_df >= start) & (alldate_df <= end)]).values.tolist()
            for i in df1:
                for j in i:
                    if str(j) != 'nan':
                        print(j)
                        real_date.append(str(j))
            for item in result[1::]:
                date_item = datetime.datetime.strptime(item[0], '%Y-%m-%d').date()
                date_item = str(date_item)
                if date_item in real_date:
                    three_pose.append([date_item,int(item[1]),int(item[2]),int(item[3])])               
            return three_pose
        else:return False

    def get_year_times(self, spreadsheetId: str, sheet_range: str,year: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=sheet_range,
        )
        response = request.execute()        
        result = response['values']  
        all_date=[]
        squat = [0 for t in range(1,13)]
        glute_bridge = [0 for t in range(1,13)]
        lunge = [0 for t in range(1,13)]
        if result != None:
            for item in result[1::]:
                if str(item[0].split('-')[0]) == year:
                    sq = int(item[1])
                    glu = int(item[2])
                    lun = int(item[3])
                    squat[int(item[0].split('-')[1])-1]+=sq
                    glute_bridge[int(item[0].split('-')[1])-1]+=glu
                    lunge[int(item[0].split('-')[1])-1]+=lun
            for i in range(1,13):
                all_date.append([i,squat[i-1],glute_bridge[i-1],lunge[i-1]])
            return all_date    
        else:return False
        
    def get_month_times(self, spreadsheetId: str, sheet_range: str,year: str,month: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=sheet_range,
        )
        response = request.execute()        
        result = response['values']  
        month_day=[]
        month_small = [4,6,9,11]
        month_times = []
        
        if int(month) in month_small:
            month_day.append(t for t in range(1,31))
        if int(month) == 2:
            if (int(year) % 100) == 0 and (int(year) % 400) == 0:
                month_day=([t for t in range(1,30)])
            elif (int(year) % 4) == 0 and (int(year) % 100) != 0:
                month_day=([t for t in range(1,30)])
            else:month_day=([t for t in range(1,29)])
        else:month_day=([t for t in range(1,32)])   
        
        for i in range(len(month_day)):
            month_day[i] = [ month_day[i],0,0,0]
        
        for item in result[1::]:
            if str(item[0].split('-')[0]) == year and str(item[0].split('-')[1]) == month:
                month_day[int(item[0].split('-')[2])-1] = [int(item[0].split('-')[2]),int(item[1]),int(item[2]),int(item[3])]
                              
        return month_day    

                    
      
'''if __name__ == '__main__':
    
    googleSheetAPI = Main_data()
    print(googleSheetAPI.googleAPIService)

    
    print(googleSheetAPI.setWorksheet(
        spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
        range='工作表1',
        df=pd.DataFrame(
            {'姓名': ['Janice','Wade','Henry','Wendy'],
            '性別': ['F','M','M','F'],
            '體重': [54,67,82,68]}
        )
    ))'''