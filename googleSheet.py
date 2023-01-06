from __future__ import print_function
from main import GoogleAPIClient
import pandas as pd
import os
from googleapiclient.errors import HttpError
import requests


class GoogleSheets(GoogleAPIClient):
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".credentials/final-works-account.json"
    def __init__(self) -> None:
        # 呼叫 GoogleAPIClient.__init__()，並提供 serviceName, version, scope
        super().__init__(
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets'],
            '.credentials/cred1.json'
        )
    def clearWorksheet(self, spreadsheetId: str, range: str):
        self.googleAPIService.spreadsheets().values().clear(
            spreadsheetId=spreadsheetId,
            range=range,
        ).execute()
        return 0
    def setWorksheet(self, spreadsheetId: str, range: str, df: pd.DataFrame):
        self.clearWorksheet(spreadsheetId, range)
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
            
    def getWorksheet(self, spreadsheetId: str, range: str, email: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=range,
        )
        response = request.execute()
        
        result = response['values']
        
        for item in result:
            if email in item[0]: return(item[1])
        return False

        '''for i in result:
            if(result[1][0] != None and result[1][0] == email):
                return result[1][1]
        header = result[0]
        del result[0]
        return pd.DataFrame(result, columns=header)'''
        
    
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
    
if __name__ == '__main__':
    myWorksheet = GoogleSheets()
    myWorksheet.get_user_info()
    
    '''print(myWorksheet.createsheet(
        title='excrcise_sheet',
    ))'''
    
    '''print(myWorksheet.setWorksheet(
         spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
         range='工作表1',
         df=pd.DataFrame(
             {'姓名': ['Janice','Wade','Henry','Wendy'],
             '性別': ['F','M','M','F'],
             '體重': [54,67,82,68]}
         )
     ))'''
    
    
    
#fileTest = r".credentials/cred.json"

#try:
#    os.remove(fileTest)
#except OSError as e:
#    print(e)
#else:
#    print("File is deleted successfully")