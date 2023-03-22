from __future__ import print_function

import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '18nAYUNPVaTGEpQJSa1wjJNaUhQBFGe_ZwS2OnIrZvHA'


def main():
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

        snippet_mark_count = 0
        snippets = []
        images = []
        elements = document.get('body').get('content')
        snippet_text = ""
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for element in elements:
                    text_run = element.get('textRun')
                    if text_run:
                        content = text_run.get('content')
                        if content.startswith("```"):
                            snippet_mark_count = snippet_mark_count + 1
                            continue
                        elif snippet_mark_count % 2 == 1:
                            snippet_text = snippet_text + content.strip()
                        elif snippet_mark_count % 2 == 0 and snippet_text != "":
                            snippets.append(snippet_text)
                            snippet_text = ""

                        image = re.search("!\[(.*?)]\((https?:\/\/\S+\.\w+)\)", content)
                        if image:
                            images.append(image)


        print(f"Found {len(snippets)} code snippets")
        print(f"Found {len(images)} images")
        #print(images[0].groups()[1])
        #print(snippets[18])

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
