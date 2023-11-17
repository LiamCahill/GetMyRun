import os.path

import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from RunEventDTO import RunEventDTO

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def __init__(self, name):
    set_gs_reader_logging()
    self.name = name


def start_gs_reader():
    creds = None
    creds = check_token(creds)
    check_credentials(creds)

    service = create_sheet_service(creds)

    result = get_results(service)
    print_result_values(result)

    # run_event_dto_test_creation()


def set_gs_reader_logging():
    logging.basicConfig(
        filename="output.log",
        level=logging.DEBUG,
    )


def check_credentials(creds):
    logging.debug("Checking credentials...")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("resources/token.json", "w") as token:
            token.write(creds.to_json())


def check_token(creds):
    logging.debug("Checking token...")

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("resources/token.json"):
        creds = Credentials.from_authorized_user_file("resources/token.json", SCOPES)
    return creds


def create_sheet_service(creds):
    logging.debug("Creating sheet service...")

    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print(err)


def get_spreadsheet_id():
    logging.debug("Getting spreadsheet id...")

    spreadsheet_id = input("Please enter spreadsheet id, or press enter for Sample")
    if not spreadsheet_id:
        spreadsheet_id = "1ixaAZVjxvNWjtUm6Ey41aeKV46VW5lQXmiNDm7nRcjA"
    return spreadsheet_id


def get_range_name():
    logging.debug("Getting spreadsheet range...")

    range_name = input("Please enter spreadsheet range, or press enter for Sample")
    if not range_name:
        range_name = "Sheet1!A2:C11"
        # Might be a good idea to write functions for sheet name, row, col
    return range_name


def get_results(service):
    logging.debug("Creating result object...")
    spreadsheet_id = get_spreadsheet_id()
    range_name = get_range_name()

    try:
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        return result
    except HttpError as err:
        logging.debug(err)


def print_result_values(result):
    logging.debug("Printing result values...")

    try:
        values = result.get("values", [])
        print("Day, Date, Run Plan")
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(f"{row[0]},{row[1]},{row[2]}")
            RunEventDTO.weekday_helper(row[1])
    except HttpError as err:
        print(err)


def run_event_dto_test_creation():
    logging.debug("Creating test DTO with default properties...")
    run_event_default = RunEventDTO()
    print(f'run_event_default day {run_event_default.getDay()}')
    print(f'run_event_default date {run_event_default.getDate()}')
    print(f'run_event_default run {run_event_default.getRun()}')

    logging.debug("Creating test DTO with test properties...")
    run_event_1 = RunEventDTO("Monday", "6/7/23", "test run")
    print(f'run_event_1 day {run_event_1.getDay()}')
    print(f'run_event_1 date {run_event_1.getDate()}')
    print(f'run_event_1 run {run_event_1.getRun()}')

def create_run_dto():
    return