import os.path

import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from RunEventDTO import RunEventDTO

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
RUNS = []


def __init__(self, name):
    set_gs_reader_logging()
    self.name = name


def start_gs_reader():
    creds = None
    creds = check_token(creds)
    check_credentials(creds)

    service = create_sheet_service(creds)

    result = get_results(service)
    # print_result_values(result)
    # run_event_dto_test_creation()

    create_run_dto(result)

    for index, item in enumerate(RUNS):
        print(f"Index: {index}, Item: {item}")

    print("Done!")


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
                "./resources/credentials.json", SCOPES
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
        range_name = "Sheet1!A2:C"
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
        # check_result_length(values)
        print("Day, Date, Run Plan")
        for row in values:
            print(f"{row}")
    except HttpError as err:
        print(f'Error when printing: {err}')
def check_result_length(values):
    for row in values:
        if len(row) != 3:
            print("Length of less than three found.")



def create_run_dto(results):
    run_event_1 = RunEventDTO("Monday", "6/7/23", "test run")
    # print(f'run_event_1 day {run_event_1.getDay()}')
    # print(f'run_event_1 date {run_event_1.getDate()}')
    # print(f'run_event_1 run {run_event_1.getRun()}')

    values = results.get("values", [])

    for row in values:
        # TODO: I need to figure out a way to ensure the creation of the DTO, regardless of the 3rd columns value/null.
        if len(values) != 3:
            print(f'day:{row[0]} date:{row[1]} run:{row[2]}')
            run = RunEventDTO(row[0],row[1],row[2])
            RUNS.append(run)
    return
