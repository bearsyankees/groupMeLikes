from groupy.client import Client
import os
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('sngm help')


groupme_client = Client.from_token(os.environ.get("TOKEN"))

nu = groupme_client.groups.get("91997574")

message_page = nu.messages.list()
#print(sorted(nu.messages.list_all(),key = lambda x: len(x.favorited_by), reverse = True))
def main():
    #TODO skip this step just use gpsread
    with open("out.csv", "w") as f:
        writer = csv.writer(f)
        for message in nu.messages.list_all():
           #print(dir(message))
           writer.writerow([message.created_at, message.name,message.text,len(message.favorited_by), len(message.attachments)])

    with open('out.csv', 'r') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)

