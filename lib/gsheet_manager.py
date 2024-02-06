import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetManager:
    def __init__(self, service_account_file, spreadsheet_id):
        self.service_account_file = service_account_file
        self.spreadsheet_id = spreadsheet_id
        self.sheet = self.init_google_sheet()

    def init_google_sheet(self):
        # Define the required scopes
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        # Authenticate using the service account file
        creds = Credentials.from_service_account_file(self.service_account_file, scopes=scopes)
        client = gspread.authorize(creds)
        # Open the spreadsheet by its ID
        spreadsheet = client.open_by_key(self.spreadsheet_id)
        # Select the first sheet
        return spreadsheet.sheet1


    def read_records(self):
        return self.sheet.get_all_records()

    def delete_all_records(self):
        # Get the total number of rows with data (assuming the first row is headers)
        total_rows = len(self.sheet.get_all_values())
        if total_rows > 1:
            # Clear all rows starting from the second
            self.sheet.delete_rows(2, total_rows)
        return None

    def read_id_records(self):
        # Fetch all records
        records = self.sheet.get_all_records()        
        # Associate each record with its row number (starting from 2 to account for header row)
        records_with_row_ids = [{"Row ID": i+2, **record} for i, record in enumerate(records)]
        return records_with_row_ids
    
    def add_record(self,record):
        self.sheet.append_row(record)
        return

    def delete_record(self, row_number):
        # Delete the specified row
        self.sheet.delete_row(row_number)
        return


class SheetRequestManager(GoogleSheetManager):

    def __init__(self, service_account_file):
        # Initialize with a specific spreadsheet ID
        self.spreadsheet_id = "1eUOJQpUwGgf4YGkN749oMKsAh2pHDDXB8s7N6acFurA"
        super().__init__(service_account_file, self.spreadsheet_id)
  
    def get_requests(self):
        # Use the parent class's sheet attribute to get all records
        records = self.sheet.get_all_records()
        return [ [record["Usuario"], record["Autor/Anime"], record["Titulo"], record["Link de Youtube"]] for record in records ]    
    
    
class SheetDebugManager(GoogleSheetManager):

    def __init__(self, service_account_file):
        # Initialize with a specific spreadsheet ID
        self.spreadsheet_id = "1HvyZsr2fy1wo0EZUtIF5VECzj2aWo8IPpb9DgFQ6dSA"
        super().__init__(service_account_file, self.spreadsheet_id)
  
    def get_requests(self):
        # Use the parent class's sheet attribute to get all records
        records = self.sheet.get_all_records()
        return [ [record["Usuario"], record["Autor/Anime"], record["Titulo"], record["Link de Youtube"]] for record in records ]    


class SheetQueueManager(GoogleSheetManager):

    def __init__(self, service_account_file):
        # Initialize with a specific spreadsheet ID
        self.spreadsheet_id = "1pqZKkKmAq8OODb6-WPw14DCrmi9bwaseLhZXQayAdEo"
        super().__init__(service_account_file, self.spreadsheet_id)
  
    def get_queuedsongs(self):
        # Use the parent class's sheet attribute to get all records
        records = self.sheet.get_all_records()
        return [ [record["Cantante"], record["Autor/Anime"], record["Titulo"], record["Link de Youtube"]] for record in records ]    


class SheetAuthorizedUsersManager(GoogleSheetManager):

    def __init__(self, service_account_file):
        # Initialize with a specific spreadsheet ID
        self.spreadsheet_id = "13Vh3yUOMo5T7TyGrF2u1fXjiUL-dX1P1BmGrJ66vl2I"
        super().__init__(service_account_file, self.spreadsheet_id)

    def get_usernames(self):
        # Use the parent class's sheet attribute to get all records
        records = self.sheet.get_all_records()
        # Loop through each record and print only the first three columns
        return [ record["Usuario"].lower() for i,record in enumerate(records) ] 

    def get_singers(self):
        # Use the parent class's sheet attribute to get all records
        records = self.sheet.get_all_records()
        # Loop through each record and print only the first three columns
        return [ record["Cantante"] for i,record in enumerate(records) ] 
            
            


