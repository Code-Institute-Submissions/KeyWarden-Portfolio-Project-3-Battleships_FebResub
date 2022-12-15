# code needed to connect game to leaderboard in Google Sheets
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('project3_leaderboard')

leaderboard = SHEET.worksheet('board')

data = leaderboard.get_all_values()

# declare contants to be used for input verification
MENU_INPUT = ["1", "s", "start", "2", "o", "options", "3", "l", "leaderboard"]
OPTIONS_INPUT = ["1", "d", "difficulty", "2", "m", "map", "3", "b", "back"]
AI_INPUT = ["1", "e", "easy", "2", "n", "normal", "3", "h", "hard", "4", "b", "back"]
MAP_SIZE_INPUT = ["1", "s", "small", "2", "m", "medium", "3", "l", "large", "4", "b", "back"]
LEADERBOARD_INPUT = ["1", "b", "back"]
SHIP_INPUT = ["1", "p", "place", "2", "r", "rotate"]

def valid_menu_input(choice):
    # function to check validity of input on menu screen
    n = 0
    is_valid = False
    while n < 9:
        if choice == MENU_INPUT[n]:
            is_valid = True
            n = 9
        else:
            n += 1
    return is_valid

def ai_difficulty(difficulty):
    if difficulty == 0:
        return "Easy"
    elif difficulty == 1:
        return "Normal"
    elif difficulty == 2:
        return "Hard"

def menu_screen(difficulty, size):
    # function that controls menu screen
    ai = "Easy"
    map = "Small"

    print("BATTLESHIPS")
    print(f"Current Difficulty: {difficulty} - Current Map Size: ")
    choice = input("Please enter your choice here: ")
