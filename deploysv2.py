#! /usr/bin/python

"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""

# run: export CREDS_FILE='/Users/chris/.ssh/<service_account>.json';python deploysv2.py

from __future__ import print_function
from argparse import ArgumentParser
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import http
from apiclient.http import MediaFileUpload
from google.oauth2 import service_account

import os

creds_key = 'CREDS_FILE'
if creds_key in os.environ:
    SERVICE_ACCOUNT_FILE = os.environ[creds_key]
# Update with the correct service_account.json file location
else:
    SERVICE_ACCOUNT_FILE = '/Users/chris/.ssh/<service_account>.json'


SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

DRIVE = build('drive', 'v3', credentials=credentials)

# creds_file = "/tmp/testrun/client_secret.json"

# Setup the Drive API
# store = file.Storage('credentials.json')
# creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets(creds_file, SCOPES)
#     creds = tools.run_flow(flow, store)
#
#
# DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

# Call the Drive API for inventory file
FILENAME = 'Network'
SRC_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
DST_MIMETYPE = 'text/csv'

#previous files: 'deploys'

# files = DRIVE.files().list(
#
#     orderBy='modifiedTime desc,name').execute().get('files', [])
#
# print(files)
# raise EnvironmentError('Failure')

files = DRIVE.files().list(
    q='name="%s" and mimeType="%s"' % (FILENAME, SRC_MIMETYPE),
    orderBy='modifiedTime desc,name').execute().get('files', [])

if files:
    fn = '%s.csv' % os.path.splitext(files[0]['name'].replace(' ', '_'))[0]
    print('Exporting "%s" as "%s"... ' % (files[0]['name'], fn), end='')
    data = DRIVE.files().export(fileId=files[0]['id'], mimeType=DST_MIMETYPE).execute()
    if data:
        with open(fn, 'wb') as f:
            f.write(data)
        print('DONE')
    else:
        print('ERROR (could not download file)')
else:
    print('!!! ERROR: File not found')


# Upload the file to quickbase sync folder
folder_id = '0B2QChk3pua2VcHhNX3dBRm93Mzg'


file_metadata = {
    'name': 'Network.csv',
    'parents': [folder_id]
}
media = MediaFileUpload('Network.csv',
                        mimetype='text/csv',
                        resumable=False)
file = DRIVE.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
print('File ID:"%s"' % file.get('id'))




# Call the Sheets API
#SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#RANGE_NAME = 'Class Data!A2:E'
#result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
#                                             range=RANGE_NAME).execute()
#values = result.get('values', [])
#if not values:
#    print('No data found.')
#else:
#    print('Name, Major:')
#    for row in values:
#        # Print columns A and E, which correspond to indices 0 and 4.
#        print('%s, %s' % (row[0], row[4]))

