pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

https://developers.google.com/sheets/api/quickstart/python

cred刪除即可
sheet id 要改
all_main:所有用戶
main+googleSheet:個人用戶
cred要更新

from main import GoogleAPIClient
from all_main import Main_data
from googleSheet import GoogleSheets
import pandas as pd
switchuser內google_login()新增
ttk.Button新增
loginpage()新增
loginpage()內的google_login()新增
ttk.Button新增
switchUser()新增
resetCounter()新增
 __init__()新增
三個動作()新增