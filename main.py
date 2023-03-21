from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1x_gDq3lHa2dT2bNRossoT8gf16HjiLKaY6GaGHqZtQc'


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        snippet_counter = 0
        elements = document.get('body').get('content')
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for element in elements:
                    text_run = element.get('textRun')
                    if text_run:
                        content = text_run.get('content')
                        if content.startswith("```"):
                            snippet_counter = snippet_counter + 1
                            print("----------")
                            continue
                        elif snippet_counter % 2 == 1:
                            print(content.strip())

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
