import os
from plugins.googlesheet.google import Create_Service

class GS():
    def __init__(self) -> None:
        FOLDER_PATH = r'plugins/googlesheet/'
        CLIENT_SECRET_FILE = os.path.join(FOLDER_PATH, 'client_secret.json')
        API_SERVICE_NAME = 'sheets'
        API_VERSION = 'v4'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        try:
            self.service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
            print(API_SERVICE_NAME, 'service created successfully')
        except Exception as e:
            print(e)
            self.service = None
    
    def create_sheet(self, title):
        body = {
            'properties': {
                'title': title
            }
        }
        return self.service.spreadsheets().create(body=body).execute()
    
    def get_sheet(self, sheet_id):
        return self.service.spreadsheets().get(spreadsheetId=sheet_id).execute()

    def update_spreadsheet(self, sheet_id, values, range_):
            body = {
                'values': values,
                'majorDimension': 'ROWS'
            }
            self.service.spreadsheets().values().update(
                        spreadsheetId=sheet_id,
                        range=range_,
                        valueInputOption='USER_ENTERED',
                        body=body).execute()
                
