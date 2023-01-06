from all_main import Main_data
from googleSheet import GoogleSheets
import pandas as pd
import datetime

'''更新金鑰或新增權限、取得使用者email'''
userinfo_database = Main_data()
print(userinfo_database.googleAPIService)
onlyuser_database = GoogleSheets()
print(onlyuser_database.googleAPIService)
user_email = userinfo_database.get_user_info()
print(user_email)


#%%
'''#判斷使用者資料是否在主資料庫'''

user_sheetId = onlyuser_database.getWorksheet(
    spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A', 
    range='工作表1', 
    email=user_email,
    )

print(user_sheetId)
#%%
'''如果該使用者沒有建立資料過則新增資料至主資料庫，取得使用者的試算表ID，使用者試算表建立
第一筆資料'''
if user_sheetId == False:
    print(onlyuser_database.appendWorksheet(
            spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
            range='工作表1',
            df=pd.DataFrame(
                {'email': [user_email],
                'sheet_id': [userinfo_database.createsheet('exercise')],
                }
            )
        ))
    user_sheetId = onlyuser_database.getWorksheet(
        spreadsheetId='11sbALGUGTJ9fxRWC83G8nUOwUBlULV5qEIlMcpJMt4A',
        range='工作表1',
        email=user_email,)
    print(user_sheetId)
    
    print(userinfo_database.setWorksheet(
        spreadsheetId=user_sheetId,
        range='工作表1',
        df=pd.DataFrame(
            {'data': [str(datetime.date.today())],
            'squat': [0],
            'glute_bridge': [0],
            'lunge': [0]},
        )
            )
                )
    
#%%
'''更新指定日期次數'''
update_cell_num = userinfo_database.get_day_pos(
    spreadsheetId=user_sheetId,
    range='工作表1',
    date='2022-11-25', #str(datetime.date.today())
    )
update_cell = "B" + str(update_cell_num) + ":D" +str(update_cell_num)

userinfo_database.updateSheet(
    spreadsheetId=user_sheetId, 
    range_name=update_cell, 
    df=[[5,2,3]]
    )
#%%
'''新增當日日期(defalt:0)'''
print(userinfo_database.appendWorksheet(
        spreadsheetId=user_sheetId,
        range='工作表1',
        df=pd.DataFrame(
            {'data': [str(datetime.date.today())],
            'squat': [0],
            'glute_bridge': [0],
            'lunge': [0],
            }
        )
    ))
#%%
squat_counter, glutebridge_counter, lunge_counter =userinfo_database.get_today_times(
    spreadsheetId=user_sheetId, 
    range="工作表1", 
    date=str(datetime.date.today()))
print(squat_counter, glutebridge_counter, lunge_counter)
type(squat_counter)
#%%

update_cell_num = userinfo_database.get_day_pos(
    spreadsheetId=user_sheetId,
    range='工作表1',
    date=str(datetime.date.today()),
    )
print("42424242424")
print(update_cell_num)
update_cell = "B" + str(update_cell_num) + ":D" +str(update_cell_num)
print(update_cell)

print(userinfo_database.updateSheet(
    spreadsheetId=user_sheetId, 
    range_name=update_cell, 
    df=[[5,1000,7]]
    ))
#%%
userinfo_database.get_date_times(
    spreadsheetId=user_sheetId,
    range='工作表1',
    sdate="2022-10-1",
    edate="2022-11-27",
    )
#%%
total=[t for t in range(1,13)]
print(total)
#%%
total=[t for t in range(1,13)]
userinfo_database.get_year_times(
    spreadsheetId=user_sheetId,
    sheet_range='工作表1',
    year = '2022',
    )
#%%
userinfo_database.get_month_times(
    spreadsheetId=user_sheetId,
    sheet_range='工作表1',
    year = '2022',
    month = '9'
    )
#%%
           
userinfo_database = Main_data()
memberName = userinfo_database.get_user_info().split('@')[0]

print(memberName)