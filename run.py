"""code needed to connect game to leaderboard in Google Sheets, as well as to
produce random numbers"""
import random
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

"""declare constants to be used for input verification"""
MENU_INPUT = ["1", "s", "start", "2", "o", "options", "3", "l", "leaderboard"]
OPTIONS_INPUT = ["1", "d", "difficulty", "2", "m", "map", "3", "b", "back"]
AI_INPUT = [
    "1", "e", "easy", "2", "n", "normal", "3", "h", "hard", "4", "b", "back"
    ]
MAP_SIZE_INPUT = [
    "1", "s", "small", "2", "m", "medium", "3", "l", "large", "4", "b", "back"
    ]
LEADERBOARD_INPUT = ["1", "b", "back"]
SHIP_INPUT = ["1", "p", "place", "2", "r", "rotate"]
SMALL_MAP_COL_INPUT = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
MED_MAP_COL_INPUT = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o"
    ]
LARGE_MAP_COL_INPUT = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"
    ]
SMALL_MAP_ROW_INPUT = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
MED_MAP_ROW_INPUT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15"
    ]
LARGE_MAP_ROW_INPUT = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
    ]
ENDING_SCREEN = [
    "1", "s", "start", "2", "r", "return", "3", "l", "leaderboard"
    ]
SAVING_SCREEN = ["1", "y", "yes", "2", "n", "no"]

"""declare variables for input verification"""
player_map_input = []
player_invalid_h = []
player_invalid_v = []
enemy_map_input = []
enemy_invalid_h = []
enemy_invalid_v = []
all_hit_grids_player = []
all_hit_grids_enemy = []
battleship_pgrid1 = ""
battleship_pgrid2 = ""
battleship_pgrid3 = ""
battleship_pgrid4 = ""
battleship_pgrid5 = ""
battleship_egrid1 = ""
battleship_egrid2 = ""
battleship_egrid3 = ""
battleship_egrid4 = ""
battleship_egrid5 = ""

"""global variables"""
game_finished = False
current_turn = ""
score = 0
player_ships_sunk = 0
enemy_ships_sunk = 0
last_hit = ""
focus_direction = "right"
core_hit = ""
victory = False


def convert_number(number):
    """converts collumn number into letter"""
    if number < 1:
        number = 1
    collumn = ""
    if number == 1:
        collumn = "A"
    elif number == 2:
        collumn = "B"
    elif number == 3:
        collumn = "C"
    elif number == 4:
        collumn = "D"
    elif number == 5:
        collumn = "E"
    elif number == 6:
        collumn = "F"
    elif number == 7:
        collumn = "G"
    elif number == 8:
        collumn = "H"
    elif number == 9:
        collumn = "I"
    elif number == 10:
        collumn = "J"
    elif number == 11:
        collumn = "K"
    elif number == 12:
        collumn = "L"
    elif number == 13:
        collumn = "M"
    elif number == 14:
        collumn = "N"
    elif number == 15:
        collumn = "O"
    elif number == 16:
        collumn = "P"
    elif number == 17:
        collumn = "Q"
    elif number == 18:
        collumn = "R"
    elif number == 19:
        collumn = "S"
    elif number == 20:
        collumn = "T"
    elif number == 21:
        collumn = "T"
    elif number == 22:
        collumn = "T"
    elif number == 23:
        collumn = "T"
    elif number == 24:
        collumn = "T"
    return collumn


def convert_letter(letter):
    """converts collumn letter into number"""
    check = letter.upper()
    collumn = 0
    if check == "A":
        collumn = 1
    elif check == "B":
        collumn = 2
    elif check == "C":
        collumn = 3
    elif check == "D":
        collumn = 4
    elif check == "E":
        collumn = 5
    elif check == "F":
        collumn = 6
    elif check == "G":
        collumn = 7
    elif check == "H":
        collumn = 8
    elif check == "I":
        collumn = 9
    elif check == "J":
        collumn = 10
    elif check == "K":
        collumn = 11
    elif check == "L":
        collumn = 12
    elif check == "M":
        collumn = 13
    elif check == "N":
        collumn = 14
    elif check == "O":
        collumn = 15
    elif check == "P":
        collumn = 16
    elif check == "Q":
        collumn = 17
    elif check == "R":
        collumn = 18
    elif check == "S":
        collumn = 19
    elif check == "T":
        collumn = 20
    return collumn


class MapGrid:
    """define a class to handle the map grids for the game"""
    def __init__(self, size):
        self.size = size
        if self.size == 0:
            self.row0 = [
                "  |", " A |", " B |", " C |", " D |", " E |", " F |", " G |",
                " H |", " I |", " J |"
                ]
            self.row1 = [
                "1 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row2 = [
                "2 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row3 = [
                "3 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row4 = [
                "4 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row5 = [
                "5 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row6 = [
                "6 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row7 = [
                "7 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row8 = [
                "8 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row9 = [
                "9 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row10 = [
                "10|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |"
                ]
            self.row_divide = [
                "--|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|"
            ]
        elif self.size == 1:
            self.row0 = [
                "  |", " A |", " B |", " C |", " D |", " E |", " F |", " G |",
                " H |", " I |", " J |", " K |", " L |", " M |", " N |", " O |"
                ]
            self.row1 = [
                "1 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row2 = [
                "2 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row3 = [
                "3 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row4 = [
                "4 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row5 = [
                "5 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row6 = [
                "6 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row7 = [
                "7 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row8 = [
                "8 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row9 = [
                "9 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row10 = [
                "10|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row11 = [
                "11|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row12 = [
                "12|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row13 = [
                "13|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row14 = [
                "14|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row15 = [
                "15|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |"
                ]
            self.row_divide = [
                "--|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|", "---|", "---|", "---|", "---|", "---|"
            ]
        elif self.size == 2:
            self.row0 = [
                "  |", " A |", " B |", " C |", " D |", " E |", " F |", " G |",
                " H |", " I |", " J |", " K |", " L |", " M |", " N |", " O |",
                " P |", " Q |", " R |", " S |", " T |"
                ]
            self.row1 = [
                "1 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row2 = [
                "2 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row3 = [
                "3 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row4 = [
                "4 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row5 = [
                "5 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row6 = [
                "6 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row7 = [
                "7 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row8 = [
                "8 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row9 = [
                "9 |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row10 = [
                "10|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row11 = [
                "11|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row12 = [
                "12|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row13 = [
                "13|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row14 = [
                "14|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row15 = [
                "15|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row16 = [
                "16|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row17 = [
                "17|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row18 = [
                "18|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row19 = [
                "19|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row20 = [
                "20|", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |", "   |", "   |", "   |",
                "   |", "   |", "   |", "   |", "   |"
                ]
            self.row_divide = [
                "--|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|", "---|", "---|", "---|", "---|", "---|",
                "---|", "---|", "---|", "---|", "---|"
            ]

    def print_grid(self):
        """function to print the grid to the console"""
        dividing_row = ""
        title_row = ""
        first_row = ""
        second_row = ""
        third_row = ""
        fourth_row = ""
        fifth_row = ""
        sixth_row = ""
        seventh_row = ""
        eighth_row = ""
        ninth_row = ""
        tenth_row = ""
        eleventh_row = ""
        twelth_row = ""
        thirteenth_row = ""
        fourteenth_row = ""
        fifteenth_row = ""
        sixteenth_row = ""
        seventeenth_row = ""
        eighteenth_row = ""
        ninteenth_row = ""
        twentieth_row = ""
        if self.size == 0:
            for i in range(0, 11):
                dividing_row += self.row_divide[i]
                title_row += self.row0[i]
                first_row += self.row1[i]
                second_row += self.row2[i]
                third_row += self.row3[i]
                fourth_row += self.row4[i]
                fifth_row += self.row5[i]
                sixth_row += self.row6[i]
                seventh_row += self.row7[i]
                eighth_row += self.row8[i]
                ninth_row += self.row9[i]
                tenth_row += self.row10[i]
            print(title_row)
            print(dividing_row)
            print(first_row)
            print(dividing_row)
            print(second_row)
            print(dividing_row)
            print(third_row)
            print(dividing_row)
            print(fourth_row)
            print(dividing_row)
            print(fifth_row)
            print(dividing_row)
            print(sixth_row)
            print(dividing_row)
            print(seventh_row)
            print(dividing_row)
            print(eighth_row)
            print(dividing_row)
            print(ninth_row)
            print(dividing_row)
            print(tenth_row)
            print(dividing_row)
        if self.size == 1:
            for i in range(0, 16):
                dividing_row += self.row_divide[i]
                title_row += self.row0[i]
                first_row += self.row1[i]
                second_row += self.row2[i]
                third_row += self.row3[i]
                fourth_row += self.row4[i]
                fifth_row += self.row5[i]
                sixth_row += self.row6[i]
                seventh_row += self.row7[i]
                eighth_row += self.row8[i]
                ninth_row += self.row9[i]
                tenth_row += self.row10[i]
                eleventh_row += self.row11[i]
                twelth_row += self.row12[i]
                thirteenth_row += self.row13[i]
                fourteenth_row += self.row14[i]
                fifteenth_row += self.row15[i]
            print(title_row)
            print(dividing_row)
            print(first_row)
            print(dividing_row)
            print(second_row)
            print(dividing_row)
            print(third_row)
            print(dividing_row)
            print(fourth_row)
            print(dividing_row)
            print(fifth_row)
            print(dividing_row)
            print(sixth_row)
            print(dividing_row)
            print(seventh_row)
            print(dividing_row)
            print(eighth_row)
            print(dividing_row)
            print(ninth_row)
            print(dividing_row)
            print(tenth_row)
            print(dividing_row)
            print(eleventh_row)
            print(dividing_row)
            print(twelth_row)
            print(dividing_row)
            print(thirteenth_row)
            print(dividing_row)
            print(fourteenth_row)
            print(dividing_row)
            print(fifteenth_row)
            print(dividing_row)
        if self.size == 2:
            for i in range(0, 21):
                dividing_row += self.row_divide[i]
                title_row += self.row0[i]
                first_row += self.row1[i]
                second_row += self.row2[i]
                third_row += self.row3[i]
                fourth_row += self.row4[i]
                fifth_row += self.row5[i]
                sixth_row += self.row6[i]
                seventh_row += self.row7[i]
                eighth_row += self.row8[i]
                ninth_row += self.row9[i]
                tenth_row += self.row10[i]
                eleventh_row += self.row11[i]
                twelth_row += self.row12[i]
                thirteenth_row += self.row13[i]
                fourteenth_row += self.row14[i]
                fifteenth_row += self.row15[i]
                sixteenth_row += self.row16[i]
                seventeenth_row += self.row17[i]
                eighteenth_row += self.row18[i]
                ninteenth_row += self.row19[i]
                twentieth_row += self.row20[i]
            print(title_row)
            print(dividing_row)
            print(first_row)
            print(dividing_row)
            print(second_row)
            print(dividing_row)
            print(third_row)
            print(dividing_row)
            print(fourth_row)
            print(dividing_row)
            print(fifth_row)
            print(dividing_row)
            print(sixth_row)
            print(dividing_row)
            print(seventh_row)
            print(dividing_row)
            print(eighth_row)
            print(dividing_row)
            print(ninth_row)
            print(dividing_row)
            print(tenth_row)
            print(dividing_row)
            print(eleventh_row)
            print(dividing_row)
            print(twelth_row)
            print(dividing_row)
            print(thirteenth_row)
            print(dividing_row)
            print(fourteenth_row)
            print(dividing_row)
            print(fifteenth_row)
            print(dividing_row)
            print(sixteenth_row)
            print(dividing_row)
            print(seventeenth_row)
            print(dividing_row)
            print(eighteenth_row)
            print(dividing_row)
            print(ninteenth_row)
            print(dividing_row)
            print(twentieth_row)
            print(dividing_row)

    def update_grid_shot(self, grid, has_hit):
        """function to update the map grid after a shot"""
        hit_result = ""
        if has_hit:
            hit_result = " # |"
        elif not has_hit:
            hit_result = " ~ |"
        collumn = grid[:1]
        col_num = convert_letter(collumn)
        row = int(grid[1:])
        if row == 1:
            self.row1[col_num] = hit_result
        elif row == 2:
            self.row2[col_num] = hit_result
        elif row == 3:
            self.row3[col_num] = hit_result
        elif row == 4:
            self.row4[col_num] = hit_result
        elif row == 5:
            self.row5[col_num] = hit_result
        elif row == 6:
            self.row6[col_num] = hit_result
        elif row == 7:
            self.row7[col_num] = hit_result
        elif row == 8:
            self.row8[col_num] = hit_result
        elif row == 9:
            self.row9[col_num] = hit_result
        elif row == 10:
            self.row10[col_num] = hit_result
        elif row == 11:
            self.row11[col_num] = hit_result
        elif row == 12:
            self.row12[col_num] = hit_result
        elif row == 13:
            self.row13[col_num] = hit_result
        elif row == 14:
            self.row14[col_num] = hit_result
        elif row == 15:
            self.row15[col_num] = hit_result
        elif row == 16:
            self.row16[col_num] = hit_result
        elif row == 17:
            self.row17[col_num] = hit_result
        elif row == 18:
            self.row18[col_num] = hit_result
        elif row == 19:
            self.row19[col_num] = hit_result
        elif row == 20:
            self.row20[col_num] = hit_result

    def update_grid_place(self, grid, active_ship):
        """function to update the map grid after ship placement"""
        collumn1 = grid[:1]
        first_col = convert_letter(collumn1)
        first_row = int(grid[1:])
        if active_ship.direction == 0:
            second_col = (first_col + 1)
            third_col = (first_col + 2)
            fourth_col = (first_col + 3)
            fifth_col = (first_col + 4)
            if active_ship.type == "carrier":
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row1[second_col] = " @ |"
                    self.row1[third_col] = " @ |"
                    self.row1[fourth_col] = " @ |"
                    self.row1[fifth_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row2[second_col] = " @ |"
                    self.row2[third_col] = " @ |"
                    self.row2[fourth_col] = " @ |"
                    self.row2[fifth_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row3[second_col] = " @ |"
                    self.row3[third_col] = " @ |"
                    self.row3[fourth_col] = " @ |"
                    self.row3[fifth_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row4[second_col] = " @ |"
                    self.row4[third_col] = " @ |"
                    self.row4[fourth_col] = " @ |"
                    self.row4[fifth_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row5[second_col] = " @ |"
                    self.row5[third_col] = " @ |"
                    self.row5[fourth_col] = " @ |"
                    self.row5[fifth_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row6[second_col] = " @ |"
                    self.row6[third_col] = " @ |"
                    self.row6[fourth_col] = " @ |"
                    self.row6[fifth_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row7[second_col] = " @ |"
                    self.row7[third_col] = " @ |"
                    self.row7[fourth_col] = " @ |"
                    self.row7[fifth_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row8[second_col] = " @ |"
                    self.row8[third_col] = " @ |"
                    self.row8[fourth_col] = " @ |"
                    self.row8[fifth_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row9[second_col] = " @ |"
                    self.row9[third_col] = " @ |"
                    self.row9[fourth_col] = " @ |"
                    self.row9[fifth_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row10[second_col] = " @ |"
                    self.row10[third_col] = " @ |"
                    self.row10[fourth_col] = " @ |"
                    self.row10[fifth_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row11[second_col] = " @ |"
                    self.row11[third_col] = " @ |"
                    self.row11[fourth_col] = " @ |"
                    self.row11[fifth_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row12[second_col] = " @ |"
                    self.row12[third_col] = " @ |"
                    self.row12[fourth_col] = " @ |"
                    self.row12[fifth_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row13[second_col] = " @ |"
                    self.row13[third_col] = " @ |"
                    self.row13[fourth_col] = " @ |"
                    self.row13[fifth_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row14[second_col] = " @ |"
                    self.row14[third_col] = " @ |"
                    self.row14[fourth_col] = " @ |"
                    self.row14[fifth_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row15[second_col] = " @ |"
                    self.row15[third_col] = " @ |"
                    self.row15[fourth_col] = " @ |"
                    self.row15[fifth_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row16[second_col] = " @ |"
                    self.row16[third_col] = " @ |"
                    self.row16[fourth_col] = " @ |"
                    self.row16[fifth_col] = " @ |"
                elif first_row == 17:
                    self.row17[first_col] = " @ |"
                    self.row17[second_col] = " @ |"
                    self.row17[third_col] = " @ |"
                    self.row17[fourth_col] = " @ |"
                    self.row17[fifth_col] = " @ |"
                elif first_row == 18:
                    self.row18[first_col] = " @ |"
                    self.row18[second_col] = " @ |"
                    self.row18[third_col] = " @ |"
                    self.row18[fourth_col] = " @ |"
                    self.row18[fifth_col] = " @ |"
                elif first_row == 19:
                    self.row19[first_col] = " @ |"
                    self.row19[second_col] = " @ |"
                    self.row19[third_col] = " @ |"
                    self.row19[fourth_col] = " @ |"
                    self.row19[fifth_col] = " @ |"
                elif first_row == 20:
                    self.row20[first_col] = " @ |"
                    self.row20[second_col] = " @ |"
                    self.row20[third_col] = " @ |"
                    self.row20[fourth_col] = " @ |"
                    self.row20[fifth_col] = " @ |"
            elif active_ship.type == "battleship":
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row1[second_col] = " @ |"
                    self.row1[third_col] = " @ |"
                    self.row1[fourth_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row2[second_col] = " @ |"
                    self.row2[third_col] = " @ |"
                    self.row2[fourth_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row3[second_col] = " @ |"
                    self.row3[third_col] = " @ |"
                    self.row3[fourth_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row4[second_col] = " @ |"
                    self.row4[third_col] = " @ |"
                    self.row4[fourth_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row5[second_col] = " @ |"
                    self.row5[third_col] = " @ |"
                    self.row5[fourth_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row6[second_col] = " @ |"
                    self.row6[third_col] = " @ |"
                    self.row6[fourth_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row7[second_col] = " @ |"
                    self.row7[third_col] = " @ |"
                    self.row7[fourth_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row8[second_col] = " @ |"
                    self.row8[third_col] = " @ |"
                    self.row8[fourth_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row9[second_col] = " @ |"
                    self.row9[third_col] = " @ |"
                    self.row9[fourth_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row10[second_col] = " @ |"
                    self.row10[third_col] = " @ |"
                    self.row10[fourth_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row11[second_col] = " @ |"
                    self.row11[third_col] = " @ |"
                    self.row11[fourth_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row12[second_col] = " @ |"
                    self.row12[third_col] = " @ |"
                    self.row12[fourth_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row13[second_col] = " @ |"
                    self.row13[third_col] = " @ |"
                    self.row13[fourth_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row14[second_col] = " @ |"
                    self.row14[third_col] = " @ |"
                    self.row14[fourth_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row15[second_col] = " @ |"
                    self.row15[third_col] = " @ |"
                    self.row15[fourth_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row16[second_col] = " @ |"
                    self.row16[third_col] = " @ |"
                    self.row16[fourth_col] = " @ |"
                elif first_row == 17:
                    self.row17[first_col] = " @ |"
                    self.row17[second_col] = " @ |"
                    self.row17[third_col] = " @ |"
                    self.row17[fourth_col] = " @ |"
                elif first_row == 18:
                    self.row18[first_col] = " @ |"
                    self.row18[second_col] = " @ |"
                    self.row18[third_col] = " @ |"
                    self.row18[fourth_col] = " @ |"
                elif first_row == 19:
                    self.row19[first_col] = " @ |"
                    self.row19[second_col] = " @ |"
                    self.row19[third_col] = " @ |"
                    self.row19[fourth_col] = " @ |"
                elif first_row == 20:
                    self.row20[first_col] = " @ |"
                    self.row20[second_col] = " @ |"
                    self.row20[third_col] = " @ |"
                    self.row20[fourth_col] = " @ |"
            elif active_ship.type in ("destroyer", "submarine"):
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row1[second_col] = " @ |"
                    self.row1[third_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row2[second_col] = " @ |"
                    self.row2[third_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row3[second_col] = " @ |"
                    self.row3[third_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row4[second_col] = " @ |"
                    self.row4[third_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row5[second_col] = " @ |"
                    self.row5[third_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row6[second_col] = " @ |"
                    self.row6[third_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row7[second_col] = " @ |"
                    self.row7[third_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row8[second_col] = " @ |"
                    self.row8[third_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row9[second_col] = " @ |"
                    self.row9[third_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row10[second_col] = " @ |"
                    self.row10[third_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row11[second_col] = " @ |"
                    self.row11[third_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row12[second_col] = " @ |"
                    self.row12[third_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row13[second_col] = " @ |"
                    self.row13[third_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row14[second_col] = " @ |"
                    self.row14[third_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row15[second_col] = " @ |"
                    self.row15[third_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row16[second_col] = " @ |"
                    self.row16[third_col] = " @ |"
                elif first_row == 17:
                    self.row17[first_col] = " @ |"
                    self.row17[second_col] = " @ |"
                    self.row17[third_col] = " @ |"
                elif first_row == 18:
                    self.row18[first_col] = " @ |"
                    self.row18[second_col] = " @ |"
                    self.row18[third_col] = " @ |"
                elif first_row == 19:
                    self.row19[first_col] = " @ |"
                    self.row19[second_col] = " @ |"
                    self.row19[third_col] = " @ |"
                elif first_row == 20:
                    self.row20[first_col] = " @ |"
                    self.row20[second_col] = " @ |"
                    self.row20[third_col] = " @ |"
            elif active_ship.type == "gunboat":
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row1[second_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row2[second_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row3[second_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row4[second_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row5[second_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row6[second_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row7[second_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row8[second_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row9[second_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row10[second_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row11[second_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row12[second_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row13[second_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row14[second_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row15[second_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row16[second_col] = " @ |"
                elif first_row == 17:
                    self.row17[first_col] = " @ |"
                    self.row17[second_col] = " @ |"
                elif first_row == 18:
                    self.row18[first_col] = " @ |"
                    self.row18[second_col] = " @ |"
                elif first_row == 19:
                    self.row19[first_col] = " @ |"
                    self.row19[second_col] = " @ |"
                elif first_row == 20:
                    self.row20[first_col] = " @ |"
                    self.row20[second_col] = " @ |"
        elif active_ship.direction == 1:
            if active_ship.type == "carrier":
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row2[first_col] = " @ |"
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                    self.row19[first_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                    self.row19[first_col] = " @ |"
                    self.row20[first_col] = " @ |"
            elif active_ship.type == "battleship":
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row2[first_col] = " @ |"
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                    self.row19[first_col] = " @ |"
                elif first_row == 17:
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                    self.row19[first_col] = " @ |"
                    self.row20[first_col] = " @ |"
            elif active_ship.type in ("destroyer", "submarine"):
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row2[first_col] = " @ |"
                    self.row3[first_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                elif first_row == 17:
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                    self.row19[first_col] = " @ |"
                elif first_row == 18:
                    self.row18[first_col] = " @ |"
                    self.row19[first_col] = " @ |"
                    self.row20[first_col] = " @ |"
            elif active_ship.type == "gunboat":
                if first_row == 1:
                    self.row1[first_col] = " @ |"
                    self.row2[first_col] = " @ |"
                elif first_row == 2:
                    self.row2[first_col] = " @ |"
                    self.row3[first_col] = " @ |"
                elif first_row == 3:
                    self.row3[first_col] = " @ |"
                    self.row4[first_col] = " @ |"
                elif first_row == 4:
                    self.row4[first_col] = " @ |"
                    self.row5[first_col] = " @ |"
                elif first_row == 5:
                    self.row5[first_col] = " @ |"
                    self.row6[first_col] = " @ |"
                elif first_row == 6:
                    self.row6[first_col] = " @ |"
                    self.row7[first_col] = " @ |"
                elif first_row == 7:
                    self.row7[first_col] = " @ |"
                    self.row8[first_col] = " @ |"
                elif first_row == 8:
                    self.row8[first_col] = " @ |"
                    self.row9[first_col] = " @ |"
                elif first_row == 9:
                    self.row9[first_col] = " @ |"
                    self.row10[first_col] = " @ |"
                elif first_row == 10:
                    self.row10[first_col] = " @ |"
                    self.row11[first_col] = " @ |"
                elif first_row == 11:
                    self.row11[first_col] = " @ |"
                    self.row12[first_col] = " @ |"
                elif first_row == 12:
                    self.row12[first_col] = " @ |"
                    self.row13[first_col] = " @ |"
                elif first_row == 13:
                    self.row13[first_col] = " @ |"
                    self.row14[first_col] = " @ |"
                elif first_row == 14:
                    self.row14[first_col] = " @ |"
                    self.row15[first_col] = " @ |"
                elif first_row == 15:
                    self.row15[first_col] = " @ |"
                    self.row16[first_col] = " @ |"
                elif first_row == 16:
                    self.row16[first_col] = " @ |"
                    self.row17[first_col] = " @ |"
                elif first_row == 17:
                    self.row17[first_col] = " @ |"
                    self.row18[first_col] = " @ |"
                elif first_row == 18:
                    self.row18[first_col] = " @ |"
                    self.row19[first_col] = " @ |"
                elif first_row == 19:
                    self.row19[first_col] = " @ |"
                    self.row20[first_col] = " @ |"


class Ship:
    """class for all ships used"""
    def __init__(self, type, direction=0):
        self.type = type
        self.direction = direction
        self.hits = 0
        self.sunk = False
        if self.type == "carrier":
            self.segments = ["", "", "", "", ""]
        elif self.type == "battleship":
            self.segments = ["", "", "", ""]
        elif self.type == "destroyer" or self.type == "submarine":
            self.segments = ["", "", ""]
        elif self.type == "gunboat":
            self.segments = ["", ""]

    def ship_placed(self, grid):
        """function for filling segments lists with co-ordinates"""
        self.segments[0] = grid
        if self.direction == 0:
            collumn1 = grid[:1]
            col_num = convert_letter(collumn1)
            collumn2 = convert_number((col_num + 1))
            second_segment = collumn2 + grid[1:]
            collumn3 = convert_number((col_num + 2))
            third_segment = collumn3 + grid[1:]
            collumn4 = convert_number((col_num + 3))
            fourth_segment = collumn4 + grid[1:]
            collumn5 = convert_number((col_num + 4))
            fifth_segment = collumn5 + grid[1:]
            if self.type == "carrier":
                self.segments[1] = second_segment
                self.segments[2] = third_segment
                self.segments[3] = fourth_segment
                self.segments[4] = fifth_segment
            elif self.type == "battleship":
                self.segments[1] = second_segment
                self.segments[2] = third_segment
                self.segments[3] = fourth_segment
            elif self.type == "destroyer" or self.type == "submarine":
                self.segments[1] = second_segment
                self.segments[2] = third_segment
            elif self.type == "gunboat":
                self.segments[1] = second_segment
        elif self.direction == 1:
            row1 = int(grid[1:])
            row2 = (row1 + 1)
            second_segment = grid[:1] + str(row2)
            row3 = (row1 + 2)
            third_segment = grid[:1] + str(row3)
            row4 = (row1 + 3)
            fourth_segment = grid[:1] + str(row4)
            row5 = (row1 + 4)
            fifth_segment = grid[:1] + str(row5)
            if self.type == "carrier":
                self.segments[1] = second_segment
                self.segments[2] = third_segment
                self.segments[3] = fourth_segment
                self.segments[4] = fifth_segment
            elif self.type == "battleship":
                self.segments[1] = second_segment
                self.segments[2] = third_segment
                self.segments[3] = fourth_segment
            elif self.type == "destroyer" or self.type == "submarine":
                self.segments[1] = second_segment
                self.segments[2] = third_segment
            elif self.type == "gunboat":
                self.segments[1] = second_segment

    def ship_sunk(self):
        if self.hits == len(self.segments):
            self.sunk = True


"""declaring all possible class instances to be used within later functions"""
player_map_small = MapGrid(0)
player_map_medium = MapGrid(1)
player_map_large = MapGrid(2)
hidden_map_small = MapGrid(0)
hidden_map_medium = MapGrid(1)
hidden_map_large = MapGrid(2)
enemy_map_small = MapGrid(0)
enemy_map_medium = MapGrid(1)
enemy_map_large = MapGrid(2)
player_carrier = Ship("carrier")
player_battleship = Ship("battleship")
player_submarine = Ship("submarine")
player_destroyer = Ship("destroyer")
player_gunboat = Ship("gunboat")
enemy_carrier = Ship("carrier")
enemy_battleship = Ship("battleship")
enemy_submarine = Ship("submarine")
enemy_destroyer = Ship("destroyer")
enemy_gunboat = Ship("gunboat")


def valid_specific_input(choice, mode, turn, ship, rotation, size):
    """function to check validity of input for placement or shots fired"""
    is_valid = True
    if mode == "place":
        if turn == "player":
            if ship == "carrier":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 7:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 12:
                            is_valid = False
                    elif size == "Large":
                        if row >= 17:
                            is_valid = False
                    for i in range(len(player_invalid_v)):
                        if choice == player_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 7:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 12:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 17:
                            is_valid = False
                    for i in range(len(player_invalid_h)):
                        if choice == player_invalid_h[i]:
                            is_valid = False
                for i in range(len(player_map_input)):
                    if choice == player_map_input[i]:
                        is_valid = False
            elif ship == "battleship":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 8:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 13:
                            is_valid = False
                    elif size == "Large":
                        if row >= 18:
                            is_valid = False
                    for i in range(len(player_invalid_v)):
                        if choice == player_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 8:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 13:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 18:
                            is_valid = False
                    for i in range(len(player_invalid_h)):
                        if choice == player_invalid_h[i]:
                            is_valid = False
                for i in range(len(player_map_input)):
                    if choice == player_map_input[i]:
                        is_valid = False
            elif ship == "destroyer" or ship == "submarine":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 9:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 14:
                            is_valid = False
                    elif size == "Large":
                        if row >= 19:
                            is_valid = False
                    for i in range(len(player_invalid_v)):
                        if choice == player_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 9:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 14:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 19:
                            is_valid = False
                    for i in range(len(player_invalid_h)):
                        if choice == player_invalid_h[i]:
                            is_valid = False
                for i in range(len(player_map_input)):
                    if choice == player_map_input[i]:
                        is_valid = False
            elif ship == "gunboat":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 10:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 15:
                            is_valid = False
                    elif size == "Large":
                        if row >= 20:
                            is_valid = False
                    for i in range(len(player_invalid_v)):
                        if choice == player_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 10:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 15:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 20:
                            is_valid = False
                    for i in range(len(player_invalid_h)):
                        if choice == player_invalid_h[i]:
                            is_valid = False
                for i in range(len(player_map_input)):
                    if choice == player_map_input[i]:
                        is_valid = False
        if turn == "enemy":
            if ship == "carrier":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 7:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 12:
                            is_valid = False
                    elif size == "Large":
                        if row >= 17:
                            is_valid = False
                    for i in range(len(enemy_invalid_v)):
                        if choice == enemy_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 7:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 12:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 17:
                            is_valid = False
                    for i in range(len(enemy_invalid_h)):
                        if choice == enemy_invalid_h[i]:
                            is_valid = False
                for i in range(len(enemy_map_input)):
                    if choice == enemy_map_input[i]:
                        is_valid = False
            elif ship == "battleship":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 8:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 13:
                            is_valid = False
                    elif size == "Large":
                        if row >= 18:
                            is_valid = False
                    for i in range(len(enemy_invalid_v)):
                        if choice == enemy_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 8:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 13:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 18:
                            is_valid = False
                    for i in range(len(enemy_invalid_h)):
                        if choice == enemy_invalid_h[i]:
                            is_valid = False
                for i in range(len(enemy_map_input)):
                    if choice == enemy_map_input[i]:
                        is_valid = False
            elif ship == "destroyer" or ship == "submarine":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 9:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 14:
                            is_valid = False
                    elif size == "Large":
                        if row >= 19:
                            is_valid = False
                    for i in range(len(enemy_invalid_v)):
                        if choice == enemy_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 9:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 14:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 19:
                            is_valid = False
                    for i in range(len(enemy_invalid_h)):
                        if choice == enemy_invalid_h[i]:
                            is_valid = False
                for i in range(len(enemy_map_input)):
                    if choice == enemy_map_input[i]:
                        is_valid = False
            elif ship == "gunboat":
                if rotation == "vertical":
                    row = int(choice[1:])
                    if size == "Small":
                        if row >= 10:
                            is_valid = False
                    elif size == "Medium":
                        if row >= 15:
                            is_valid = False
                    elif size == "Large":
                        if row >= 20:
                            is_valid = False
                    for i in range(len(enemy_invalid_v)):
                        if choice == enemy_invalid_v[i]:
                            is_valid = False
                elif rotation == "horizontal":
                    collumn = convert_letter(choice[:1])
                    if size == "Small":
                        if collumn >= 10:
                            is_valid = False
                    elif size == "Medium":
                        if collumn >= 15:
                            is_valid = False
                    elif size == "Large":
                        if collumn >= 20:
                            is_valid = False
                    for i in range(len(enemy_invalid_h)):
                        if choice == enemy_invalid_h[i]:
                            is_valid = False
                for i in range(len(enemy_map_input)):
                    if choice == enemy_map_input[i]:
                        is_valid = False
    elif mode == "shoot":
        if turn == "player":
            for i in range(len(all_hit_grids_player)):
                if choice == all_hit_grids_player[i]:
                    is_valid = False
        elif turn == "enemy":
            for i in range(len(all_hit_grids_enemy)):
                if choice == all_hit_grids_enemy[i]:
                    is_valid = False
    return is_valid


def valid_general_input(choice, screen):
    """function to check validity of general input on all screens"""
    is_valid = False
    if screen == "menu":
        for i in range(len(MENU_INPUT)):
            if choice.lower() == MENU_INPUT[i]:
                is_valid = True
    elif screen == "options":
        for i in range(len(OPTIONS_INPUT)):
            if choice.lower() == OPTIONS_INPUT[i]:
                is_valid = True
    elif screen == "difficulty":
        for i in range(len(AI_INPUT)):
            if choice.lower() == AI_INPUT[i]:
                is_valid = True
    elif screen == "size":
        for i in range(len(MAP_SIZE_INPUT)):
            if choice.lower() == MAP_SIZE_INPUT[i]:
                is_valid = True
    elif screen == "leaderboard":
        for i in range(len(LEADERBOARD_INPUT)):
            if choice.lower() == LEADERBOARD_INPUT[i]:
                is_valid = True
    elif screen == "rotate":
        for i in range(len(SHIP_INPUT)):
            if choice.lower() == SHIP_INPUT[i]:
                is_valid = True
    elif screen == "place-col-small":
        for i in range(len(SMALL_MAP_COL_INPUT)):
            if choice.lower() == SMALL_MAP_COL_INPUT[i]:
                is_valid = True
    elif screen == "place-col-medium":
        for i in range(len(MED_MAP_COL_INPUT)):
            if choice.lower() == MED_MAP_COL_INPUT[i]:
                is_valid = True
    elif screen == "place-col-large":
        for i in range(len(LARGE_MAP_COL_INPUT)):
            if choice.lower() == LARGE_MAP_COL_INPUT[i]:
                is_valid = True
    elif screen == "place-row-small":
        for i in range(len(SMALL_MAP_ROW_INPUT)):
            if choice.lower() == SMALL_MAP_ROW_INPUT[i]:
                is_valid = True
    elif screen == "place-row-medium":
        for i in range(len(MED_MAP_ROW_INPUT)):
            if choice.lower() == MED_MAP_ROW_INPUT[i]:
                is_valid = True
    elif screen == "place-row-large":
        for i in range(len(LARGE_MAP_ROW_INPUT)):
            if choice.lower() == LARGE_MAP_ROW_INPUT[i]:
                is_valid = True
    elif screen == "ending":
        for i in range(len(ENDING_SCREEN)):
            if choice.lower() == ENDING_SCREEN[i]:
                is_valid = True
    return is_valid


def ai_difficulty(difficulty):
    """function translates difficulty into text for user"""
    result = ""
    if difficulty == 0:
        result = "Easy"
    elif difficulty == 1:
        result = "Normal"
    elif difficulty == 2:
        result = "Hard"
    return result


def map_size(size):
    """function translates map size into text for user"""
    result = ""
    if size == 0:
        result = "Small"
    elif size == 1:
        result = "Medium"
    elif size == 2:
        result = "Large"
    return result


def enemy_spaces(active_ship):
    """ensures invalid AI grid spaces are tracked"""
    base_grid1 = ""
    base_grid2 = ""
    base_grid3 = ""
    base_grid4 = ""
    end_grids_v = []
    end_grids_h = []
    global battleship_egrid1, battleship_egrid2, battleship_egrid3
    global battleship_egrid4, battleship_egrid5
    if active_ship.type == "carrier":
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                base_grid2 = collumn + str((row - 2))
                end_grids_v.append((collumn + str((row - 3))))
                enemy_invalid_v.append(base_grid1)
                enemy_invalid_v.append(base_grid2)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            base_grid4 = convert_number((col_num - 2)) + str(row)
            end_grids_h.append((convert_number((col_num - 3)) + str(row)))
            enemy_invalid_h.append(base_grid3)
            enemy_invalid_h.append(base_grid4)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                base_grid2 = convert_number((col_num - 2)) + str(row)
                end_grids_h.append((convert_number((col_num - 3)) + str(row)))
                enemy_invalid_h.append(base_grid1)
                enemy_invalid_h.append(base_grid2)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            base_grid4 = collumn + str((row - 2))
            end_grids_v.append((collumn + str((row - 3))))
            enemy_invalid_v.append(base_grid3)
            enemy_invalid_v.append(base_grid4)
        enemy_invalid_h.extend(end_grids_h)
        enemy_invalid_v.extend(end_grids_v)
    elif active_ship.type == "battleship":
        if enemy_carrier.direction == 0:
            enemy_invalid_h.pop()
            enemy_invalid_v.pop()
            enemy_invalid_v.pop()
            enemy_invalid_v.pop()
            enemy_invalid_v.pop()
            enemy_invalid_v.pop()
        elif enemy_carrier.direction == 1:
            enemy_invalid_h.pop()
            enemy_invalid_h.pop()
            enemy_invalid_h.pop()
            enemy_invalid_h.pop()
            enemy_invalid_h.pop()
            enemy_invalid_v.pop()
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                end_grids_v.append((collumn + str((row - 2))))
                enemy_invalid_v.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            end_grids_h.append((convert_number((col_num - 2)) + str(row)))
            enemy_invalid_h.append(base_grid3)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                end_grids_h.append((convert_number((col_num - 2)) + str(row)))
                enemy_invalid_h.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            end_grids_v.append((collumn + str((row - 2))))
            enemy_invalid_v.append(base_grid3)
        enemy_invalid_h.extend(end_grids_h)
        enemy_invalid_v.extend(end_grids_v)
    elif active_ship.type == "destroyer":
        if enemy_battleship.direction == 0:
            battleship_egrid1 = enemy_invalid_h[-1]
            battleship_egrid2 = enemy_invalid_v[-1]
            battleship_egrid3 = enemy_invalid_v[-2]
            battleship_egrid4 = enemy_invalid_v[-3]
            battleship_egrid5 = enemy_invalid_v[-4]
        elif enemy_battleship.direction == 1:
            battleship_egrid1 = enemy_invalid_v[-1]
            battleship_egrid2 = enemy_invalid_h[-1]
            battleship_egrid3 = enemy_invalid_h[-2]
            battleship_egrid4 = enemy_invalid_h[-3]
            battleship_egrid5 = enemy_invalid_h[-4]
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                end_grids_v.append((collumn + str((row - 2))))
                enemy_invalid_v.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            end_grids_h.append((convert_number((col_num - 2)) + str(row)))
            enemy_invalid_h.append(base_grid3)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                end_grids_h.append((convert_number((col_num - 2)) + str(row)))
                enemy_invalid_h.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            end_grids_v.append((collumn + str((row - 2))))
            enemy_invalid_v.append(base_grid3)
        enemy_invalid_h.extend(end_grids_h)
        enemy_invalid_v.extend(end_grids_v)
    elif active_ship.type == "submarine":
        if enemy_destroyer.direction == 0:
            enemy_invalid_h.pop()
            enemy_invalid_v.pop()
            enemy_invalid_v.pop()
            enemy_invalid_v.pop()
        elif enemy_destroyer.direction == 1:
            enemy_invalid_h.pop()
            enemy_invalid_h.pop()
            enemy_invalid_h.pop()
            enemy_invalid_v.pop()
        if enemy_battleship.direction == 0:
            enemy_invalid_h.remove(battleship_egrid1)
            enemy_invalid_v.remove(battleship_egrid2)
            enemy_invalid_v.remove(battleship_egrid3)
            enemy_invalid_v.remove(battleship_egrid4)
            enemy_invalid_v.remove(battleship_egrid5)
        elif enemy_battleship.direction == 1:
            enemy_invalid_v.remove(battleship_egrid1)
            enemy_invalid_h.remove(battleship_egrid2)
            enemy_invalid_h.remove(battleship_egrid3)
            enemy_invalid_h.remove(battleship_egrid4)
            enemy_invalid_h.remove(battleship_egrid5)
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                enemy_invalid_v.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            enemy_invalid_h.append(base_grid3)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                enemy_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                enemy_invalid_h.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            enemy_invalid_v.append(base_grid3)
    elif active_ship.type == "gunboat":
        for i in range(len(active_ship.segments)):
            enemy_map_input.append(active_ship.segments[i])


def enemy_place_current_ship_output(
  choice, active_ship, game_map, size, validity, extra_validity):
    """controls output of enemy_place_current_ship function"""
    if not validity:
        enemy_place_current_ship(active_ship, size)
    if not extra_validity:
        enemy_place_current_ship(active_ship, size)
    if validity and extra_validity:
        active_ship.ship_placed(choice)
        if game_map == "Small":
            enemy_map_small.update_grid_place(choice, active_ship)
        elif game_map == "Medium":
            enemy_map_medium.update_grid_place(choice, active_ship)
        elif game_map == "Large":
            enemy_map_large.update_grid_place(choice, active_ship)
        enemy_spaces(active_ship)


def enemy_place_current_ship(active_ship, size):
    """controls actual placing of AI ship on all maps"""
    game_map = map_size(size)
    validity = False
    extra_validity = True
    rotation = ""
    if active_ship.direction == 0:
        rotation = "horizontal"
        if game_map == "Small":
            col_num = random.randrange(1, 11)
            collumn = convert_number(col_num)
            row = str(random.randrange(1, 11))
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-small")
            row_validity = valid_general_input(row, "place-row-small")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "enemy",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Medium":
            col_num = random.randrange(1, 16)
            collumn = convert_number(col_num)
            row = str(random.randrange(1, 16))
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-medium")
            row_validity = valid_general_input(row, "place-row-medium")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "enemy",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Large":
            col_num = random.randrange(1, 21)
            collumn = convert_number(col_num)
            row = str(random.randrange(1, 21))
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-large")
            row_validity = valid_general_input(row, "place-row-large")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "enemy",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
    elif active_ship.direction == 1:
        rotation = "vertical"
        if game_map == "Small":
            col_num = random.randrange(1, 11)
            collumn = convert_number(col_num)
            row = str(random.randrange(1, 11))
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-small")
            row_validity = valid_general_input(row, "place-row-small")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "enemy",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Medium":
            col_num = random.randrange(1, 16)
            collumn = convert_number(col_num)
            row = str(random.randrange(1, 16))
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-medium")
            row_validity = valid_general_input(row, "place-row-medium")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "enemy",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Large":
            col_num = random.randrange(1, 21)
            collumn = convert_number(col_num)
            row = str(random.randrange(1, 21))
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-large")
            row_validity = valid_general_input(row, "place-row-large")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "enemy",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
    enemy_place_current_ship_output(
        choice.upper(), active_ship, game_map, size, validity, extra_validity
        )


def enemy_placing_ship_output(
  validity, choice, current_ship, active_ship, size):
    """controls result of AI input on ship placement for all maps"""
    if not validity:
        enemy_placing_ship(current_ship, size)

    if choice == "1" or choice == "p" or choice == "place":
        enemy_place_current_ship(active_ship, size)
    elif choice == "2" or choice == "r" or choice == "rotate":
        if active_ship.direction == 0:
            active_ship.direction = 1
        else:
            active_ship.direction = 0
        enemy_placing_ship(current_ship, size)


def enemy_placing_ship(current_ship, size):
    """function controlling exact process for AI placing ships"""
    if current_ship == 1:
        active_ship = enemy_carrier
    elif current_ship == 2:
        active_ship = enemy_battleship
    elif current_ship == 3:
        active_ship = enemy_destroyer
    elif current_ship == 4:
        active_ship = enemy_submarine
    elif current_ship == 5:
        active_ship = enemy_gunboat
    if active_ship.direction == 0:
        choice = str(random.randrange(1, 3))
    elif active_ship.direction == 1:
        choice = str(random.randrange(1, 3))
    validity = valid_general_input(choice, "rotate")
    enemy_placing_ship_output(
        validity, choice, current_ship, active_ship, size)


def player_spaces(active_ship):
    """ensures invalid player grid spaces are tracked"""
    base_grid1 = ""
    base_grid2 = ""
    base_grid3 = ""
    base_grid4 = ""
    end_grids_v = []
    end_grids_h = []
    global battleship_pgrid1, battleship_pgrid2, battleship_pgrid3
    global battleship_pgrid4, battleship_pgrid5
    if active_ship.type == "carrier":
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                base_grid2 = collumn + str((row - 2))
                end_grids_v.append((collumn + str((row - 3))))
                player_invalid_v.append(base_grid1)
                player_invalid_v.append(base_grid2)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            base_grid4 = convert_number((col_num - 2)) + str(row)
            end_grids_h.append((convert_number((col_num - 3)) + str(row)))
            player_invalid_h.append(base_grid3)
            player_invalid_h.append(base_grid4)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                base_grid2 = convert_number((col_num - 2)) + str(row)
                end_grids_h.append((convert_number((col_num - 3)) + str(row)))
                player_invalid_h.append(base_grid1)
                player_invalid_h.append(base_grid2)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            base_grid4 = collumn + str((row - 2))
            end_grids_v.append((collumn + str((row - 3))))
            player_invalid_v.append(base_grid3)
            player_invalid_v.append(base_grid4)
        player_invalid_h.extend(end_grids_h)
        player_invalid_v.extend(end_grids_v)
    elif active_ship.type == "battleship":
        if player_carrier.direction == 0:
            player_invalid_h.pop()
            player_invalid_v.pop()
            player_invalid_v.pop()
            player_invalid_v.pop()
            player_invalid_v.pop()
            player_invalid_v.pop()
        elif player_carrier.direction == 1:
            player_invalid_h.pop()
            player_invalid_h.pop()
            player_invalid_h.pop()
            player_invalid_h.pop()
            player_invalid_h.pop()
            player_invalid_v.pop()
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                end_grids_v.append((collumn + str((row - 2))))
                player_invalid_v.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            end_grids_h.append((convert_number((col_num - 2)) + str(row)))
            player_invalid_h.append(base_grid3)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                end_grids_h.append((convert_number((col_num - 2)) + str(row)))
                player_invalid_h.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            end_grids_v.append((collumn + str((row - 2))))
            player_invalid_v.append(base_grid3)
        player_invalid_h.extend(end_grids_h)
        player_invalid_v.extend(end_grids_v)
    elif active_ship.type == "destroyer":
        if player_battleship.direction == 0:
            battleship_pgrid1 = player_invalid_h[-1]
            battleship_pgrid2 = player_invalid_v[-1]
            battleship_pgrid3 = player_invalid_v[-2]
            battleship_pgrid4 = player_invalid_v[-3]
            battleship_pgrid5 = player_invalid_v[-4]
        elif player_battleship.direction == 1:
            battleship_pgrid1 = player_invalid_v[-1]
            battleship_pgrid2 = player_invalid_h[-1]
            battleship_pgrid3 = player_invalid_h[-2]
            battleship_pgrid4 = player_invalid_h[-3]
            battleship_pgrid5 = player_invalid_h[-4]
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                end_grids_v.append((collumn + str((row - 2))))
                player_invalid_v.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            end_grids_h.append((convert_number((col_num - 2)) + str(row)))
            player_invalid_h.append(base_grid3)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                end_grids_h.append((convert_number((col_num - 2)) + str(row)))
                player_invalid_h.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            end_grids_v.append((collumn + str((row - 2))))
            player_invalid_v.append(base_grid3)
        player_invalid_h.extend(end_grids_h)
        player_invalid_v.extend(end_grids_v)
    elif active_ship.type == "submarine":
        if player_destroyer.direction == 0:
            player_invalid_h.pop()
            player_invalid_v.pop()
            player_invalid_v.pop()
            player_invalid_v.pop()
        elif player_destroyer.direction == 1:
            player_invalid_h.pop()
            player_invalid_h.pop()
            player_invalid_h.pop()
            player_invalid_v.pop()
        if player_battleship.direction == 0:
            player_invalid_h.remove(battleship_pgrid1)
            player_invalid_v.remove(battleship_pgrid2)
            player_invalid_v.remove(battleship_pgrid3)
            player_invalid_v.remove(battleship_pgrid4)
            player_invalid_v.remove(battleship_pgrid5)
        elif player_battleship.direction == 1:
            player_invalid_v.remove(battleship_pgrid1)
            player_invalid_h.remove(battleship_pgrid2)
            player_invalid_h.remove(battleship_pgrid3)
            player_invalid_h.remove(battleship_pgrid4)
            player_invalid_h.remove(battleship_pgrid5)
        if active_ship.direction == 0:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = collumn + str((row - 1))
                player_invalid_v.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = convert_number((col_num - 1)) + str(row)
            player_invalid_h.append(base_grid3)
        elif active_ship.direction == 1:
            for i in range(len(active_ship.segments)):
                player_map_input.append(active_ship.segments[i])
                grid = active_ship.segments[i]
                collumn = grid[:1]
                col_num = convert_letter(collumn)
                row = int(grid[1:])
                base_grid1 = convert_number((col_num - 1)) + str(row)
                player_invalid_h.append(base_grid1)
            grid = active_ship.segments[0]
            collumn = grid[:1]
            col_num = convert_letter(collumn)
            row = int(grid[1:])
            base_grid3 = collumn + str((row - 1))
            player_invalid_v.append(base_grid3)
    elif active_ship.type == "gunboat":
        for i in range(len(active_ship.segments)):
            player_map_input.append(active_ship.segments[i])


def place_current_ship_output(
  choice, active_ship, game_map, size, validity, extra_validity):
    """controls output of place_current_ship function"""
    if not validity:
        print("Invalid input.")
        if game_map == "Small":
            print(
                "Please input one of the following in" +
                f" the collumn slot: {SMALL_MAP_COL_INPUT}," +
                " and one of the following in the row" +
                f" slot: {SMALL_MAP_ROW_INPUT}. e.g. 'A5'"
                )
        elif game_map == "Medium":
            print(
                "Please input one of the following in" +
                f" the collumn slot: {MED_MAP_COL_INPUT}," +
                " and one of the following in the row" +
                f" slot: {MED_MAP_ROW_INPUT}. e.g. 'A5'"
                )
        elif game_map == "Large":
            print(
                "Please input one of the following in" +
                f" the collumn slot: {LARGE_MAP_COL_INPUT}," +
                " and one of the following in the row" +
                f" slot: {LARGE_MAP_ROW_INPUT}. e.g. 'A5'"
                )
        place_current_ship(active_ship, size)
    if not extra_validity:
        print("Invalid Grid Coordinates.")
        print("The given coordinates are either:")
        print("1. Too close to one of the map edges.")
        print("2. Already taken by another ship.")
        print("3. Too close to another ship.")
        print("Please look over the Grid's current state, and try again")
        place_current_ship(active_ship, size)
    if validity and extra_validity:
        active_ship.ship_placed(choice)
        if game_map == "Small":
            player_map_small.update_grid_place(choice, active_ship)
        elif game_map == "Medium":
            player_map_medium.update_grid_place(choice, active_ship)
        elif game_map == "Large":
            player_map_large.update_grid_place(choice, active_ship)
        player_spaces(active_ship)


def place_current_ship(active_ship, size):
    """controls actual placing of ship on all maps"""
    out_of_bounds = (len(active_ship.segments) - 1)
    game_map = map_size(size)
    validity = False
    extra_validity = True
    rotation = ""
    print(
        f"In order to place your {active_ship.type}," +
        " you will need to enter the grid coordinates" +
        " of its first segment in the style: ##, where" +
        " the first # is the collumn letter, and the" +
        " second # is the row number"
        )
    if active_ship.direction == 0:
        rotation = "horizontal"
        print("The first segment is the left-most segment.")
        print(
            "You cannot select the grid-space within" +
            f" {out_of_bounds} spaces of the right edge."
            )
        choice = input("Please enter your choice here: \n").lower()
        if game_map == "Small":
            col_validity = valid_general_input(choice[:1], "place-col-small")
            row_validity = valid_general_input(choice[1:], "place-row-small")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "player",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Medium":
            col_validity = valid_general_input(choice[:1], "place-col-medium")
            row_validity = valid_general_input(choice[1:], "place-row-medium")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "player",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Large":
            col_validity = valid_general_input(choice[:1], "place-col-large")
            row_validity = valid_general_input(choice[1:], "place-row-large")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "player",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
    elif active_ship.direction == 1:
        rotation = "vertical"
        print("The first segment is the top-most segment.")
        print(
            "You cannot select the grid-space within" +
            f" {out_of_bounds} spaces of the bottom edge."
            )
        choice = input("Please enter your choice here: \n").lower()
        if game_map == "Small":
            col_validity = valid_general_input(choice[:1], "place-col-small")
            row_validity = valid_general_input(choice[1:], "place-row-small")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "player",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Medium":
            col_validity = valid_general_input(choice[:1], "place-col-medium")
            row_validity = valid_general_input(choice[1:], "place-row-medium")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "player",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
        elif game_map == "Large":
            col_validity = valid_general_input(choice[:1], "place-col-large")
            row_validity = valid_general_input(choice[1:], "place-row-large")
            extra_validity = valid_specific_input(
                choice.upper(), "place", "player",
                active_ship.type, rotation, game_map
                )
            if col_validity and row_validity:
                validity = True
    place_current_ship_output(
        choice.upper(), active_ship, game_map, size, validity, extra_validity
        )


def placing_ship_output(validity, choice, current_ship, active_ship, size):
    """controls result of user input on ship placement for all maps"""
    if not validity:
        print(
            f"Invalid input, please input one of the following: {SHIP_INPUT}"
            )
        placing_ship(current_ship, size)

    if choice == "1" or choice == "p" or choice == "place":
        place_current_ship(active_ship, size)
    elif choice == "2" or choice == "r" or choice == "rotate":
        if active_ship.direction == 0:
            active_ship.direction = 1
        else:
            active_ship.direction = 0
        placing_ship(current_ship, size)


def placing_ship(current_ship, size):
    """function controlling exact process for player placing ships"""
    if current_ship == 1:
        active_ship = player_carrier
    elif current_ship == 2:
        active_ship = player_battleship
    elif current_ship == 3:
        active_ship = player_destroyer
    elif current_ship == 4:
        active_ship = player_submarine
    elif current_ship == 5:
        active_ship = player_gunboat
    if active_ship.direction == 0:
        print(
            f"Current ship: {active_ship.type}" +
            f" - {active_ship.segments}"
            )
        print("Current orientation: Horizontal (left to right)")
        print("1. [P]lace")
        print("2. [R]otate")
        choice = input("Please enter your choice here: \n")
    elif active_ship.direction == 1:
        print(
            f"Current ship: {active_ship.type}" +
            f"- {active_ship.segments}"
            )
        print("Current orientation: Vertical (top to bottom)")
        print("1. [P]lace")
        print("2. [R]otate")
        choice = input("Please enter your choice here: \n")
    validity = valid_general_input(choice, "rotate")
    placing_ship_output(validity, choice, current_ship, active_ship, size)


def place_ships(size):
    """function guiding ship placing process for all maps"""
    print("Please place your ships.")
    current_ship = 1
    while current_ship <= 5:
        if size == 0:
            print("YOUR GRID:")
            player_map_small.print_grid()
        elif size == 1:
            print("YOUR GRID:")
            player_map_medium.print_grid()
        elif size == 2:
            print("YOUR GRID:")
            player_map_large.print_grid()
        placing_ship(current_ship, size)
        enemy_placing_ship(current_ship, size)
        current_ship += 1


def ship_hit(choice, turn):
    """function for finding ship hit, and registering the hit"""
    if turn == "player":
        for i in range(len(enemy_carrier.segments)):
            if choice == enemy_carrier.segments[i]:
                enemy_carrier.hits += 1
                enemy_carrier.ship_sunk()
                result = enemy_carrier
        for i in range(len(enemy_battleship.segments)):
            if choice == enemy_battleship.segments[i]:
                enemy_battleship.hits += 1
                enemy_battleship.ship_sunk()
                result = enemy_battleship
        for i in range(len(enemy_destroyer.segments)):
            if choice == enemy_destroyer.segments[i]:
                enemy_destroyer.hits += 1
                enemy_destroyer.ship_sunk()
                result = enemy_destroyer
        for i in range(len(enemy_submarine.segments)):
            if choice == enemy_submarine.segments[i]:
                enemy_submarine.hits += 1
                enemy_submarine.ship_sunk()
                result = enemy_submarine
        for i in range(len(enemy_gunboat.segments)):
            if choice == enemy_gunboat.segments[i]:
                enemy_gunboat.hits += 1
                enemy_gunboat.ship_sunk()
                result = enemy_gunboat
    elif turn == "enemy":
        for i in range(len(player_carrier.segments)):
            if choice == player_carrier.segments[i]:
                player_carrier.hits += 1
                player_carrier.ship_sunk()
                result = player_carrier
        for i in range(len(player_battleship.segments)):
            if choice == player_battleship.segments[i]:
                player_battleship.hits += 1
                player_battleship.ship_sunk()
                result = player_battleship
        for i in range(len(player_destroyer.segments)):
            if choice == player_destroyer.segments[i]:
                player_destroyer.hits += 1
                player_destroyer.ship_sunk()
                result = player_destroyer
        for i in range(len(player_submarine.segments)):
            if choice == player_submarine.segments[i]:
                player_submarine.hits += 1
                player_submarine.ship_sunk()
                result = player_submarine
        for i in range(len(player_gunboat.segments)):
            if choice == player_gunboat.segments[i]:
                player_gunboat.hits += 1
                player_gunboat.ship_sunk()
                result = player_gunboat
    return result


def player_turn_output(choice, game_map, size, validity, extra_validity):
    """function that controls output of the player's turn"""
    global game_finished, current_turn, score, enemy_ships_sunk
    has_hit = False
    if not validity:
        print("Invalid Input.")
        if game_map == "Small":
            print(
                "Please input one of the following in" +
                f" the collumn slot: {SMALL_MAP_COL_INPUT}," +
                " and one of the following in the row" +
                f" slot: {SMALL_MAP_ROW_INPUT}. e.g. 'A5'"
                )
        elif game_map == "Medium":
            print(
                "Please input one of the following in" +
                f" the collumn slot: {MED_MAP_COL_INPUT}," +
                " and one of the following in the row" +
                f" slot: {MED_MAP_ROW_INPUT}. e.g. 'A5'"
                )
        elif game_map == "Large":
            print(
                "Please input one of the following in" +
                f" the collumn slot: {LARGE_MAP_COL_INPUT}," +
                " and one of the following in the row" +
                f" slot: {LARGE_MAP_ROW_INPUT}. e.g. 'A5'"
                )
        player_turn(size)
    if not extra_validity:
        print("Invalid Grid Coordinates.")
        print("You have already hit that grid space.")
        print("Please look over the Grid's current state, and try again")
        player_turn(size)
    if validity and extra_validity:
        all_hit_grids_player.append(choice)
        for i in range(len(enemy_map_input)):
            if choice == enemy_map_input[i]:
                has_hit = True
                score += 10
                print("HIT!")
        if has_hit:
            shot_result = ship_hit(choice, "player")
            if shot_result.sunk:
                print(f"You've sunk the enemy {shot_result.type}!")
                score += 100
                enemy_ships_sunk += 1
        elif not has_hit:
            print("MISS!")
            score -= 1
        if game_map == "Small":
            hidden_map_small.update_grid_shot(choice, has_hit)
            enemy_map_small.update_grid_shot(choice, has_hit)
        elif game_map == "Medium":
            hidden_map_medium.update_grid_shot(choice, has_hit)
            enemy_map_medium.update_grid_shot(choice, has_hit)
        elif game_map == "Large":
            hidden_map_large.update_grid_shot(choice, has_hit)
            enemy_map_large.update_grid_shot(choice, has_hit)
        if enemy_ships_sunk >= 5:
            game_finished = True
        if not game_finished:
            current_turn = "enemy"


def player_turn(size):
    """function that guides the player's turn"""
    game_map = map_size(size)
    print("Select a grid space to fire a shot.")
    print(
        "Please do so in the following style: ##," +
        " where the first # represents the collumn " +
        "letter, and the second the row number."
        )
    choice = input("Please enter your choice here: \n").lower()
    collumn = choice[:1]
    row = choice[1:]
    validity = False
    extra_validity = True
    if game_map == "Small":
        col_validity = valid_general_input(collumn, "place-col-small")
        row_validity = valid_general_input(row, "place-row-small")
        if col_validity and row_validity:
            validity = True
    elif game_map == "Medium":
        col_validity = valid_general_input(collumn, "place-col-medium")
        row_validity = valid_general_input(row, "place-row-medium")
        if col_validity and row_validity:
            validity = True
    elif game_map == "Large":
        col_validity = valid_general_input(collumn, "place-col-large")
        row_validity = valid_general_input(row, "place-row-large")
        if col_validity and row_validity:
            validity = True
    extra_validity = valid_specific_input(
        choice.upper(), "shoot", "player", "", "", game_map)
    player_turn_output(
        choice.upper(), game_map, size, validity, extra_validity)


def enemy_turn_output(choice, validity, extra_validity, difficulty, size):
    """function that controls output of enemy_turn"""
    global game_finished, current_turn, score, player_ships_sunk, hit_last
    global core_hit, focus_direction
    game_map = map_size(size)
    a_i = ai_difficulty(difficulty)
    has_hit = False
    if a_i == "Easy":
        if not validity or not extra_validity:
            enemy_turn(difficulty, size)
        if validity and extra_validity:
            all_hit_grids_enemy.append(choice)
            for i in range(len(player_map_input)):
                if choice == player_map_input[i]:
                    has_hit = True
                    score -= 5
                    print("HIT!")
            if has_hit:
                shot_result = ship_hit(choice, "enemy")
                if shot_result.sunk:
                    score -= 50
                    player_ships_sunk += 1
                    print(f"The enemy has sunk your {shot_result.type}!")
            elif not has_hit:
                print("MISS!")
            if game_map == "Small":
                player_map_small.update_grid_shot(choice, has_hit)
            elif game_map == "Medium":
                player_map_medium.update_grid_shot(choice, has_hit)
            elif game_map == "Large":
                player_map_large.update_grid_shot(choice, has_hit)
            if player_ships_sunk >= 5:
                game_finished = True
            if not game_finished:
                current_turn = "player"
    elif a_i == "Normal":
        if not validity or not extra_validity:
            hit_last = ""
            enemy_turn(difficulty, size)
        if validity and extra_validity:
            all_hit_grids_enemy.append(choice)
            for i in range(len(player_map_input)):
                if choice == player_map_input[i]:
                    has_hit = True
                    score -= 5
                    hit_last = choice
                    print("HIT!")
            if has_hit:
                shot_result = ship_hit(choice, "enemy")
                if shot_result.sunk:
                    score -= 50
                    player_ships_sunk += 1
                    hit_last = ""
                    print(f"The enemy has sunk your {shot_result.type}!")
            elif not has_hit:
                print("MISS!")
                hit_last = ""
            if game_map == "Small":
                player_map_small.update_grid_shot(choice, has_hit)
            elif game_map == "Medium":
                player_map_medium.update_grid_shot(choice, has_hit)
            elif game_map == "Large":
                player_map_large.update_grid_shot(choice, has_hit)
            if player_ships_sunk >= 5:
                game_finished = True
            if not game_finished:
                current_turn = "player"
    elif a_i == "Hard":
        if core_hit == "":
            if not validity or not extra_validity:
                enemy_turn(difficulty, size)
            if validity and extra_validity:
                all_hit_grids_enemy.append(choice)
                for i in range(len(player_map_input)):
                    if choice == player_map_input[i]:
                        has_hit = True
                        score -= 5
                        hit_last = choice
                        core_hit = choice
                        print("HIT!")
                if has_hit:
                    shot_result = ship_hit(choice, "enemy")
                    if shot_result.sunk:
                        score -= 50
                        player_ships_sunk += 1
                        core_hit = ""
                        hit_last = ""
                        print(f"The enemy has sunk your {shot_result.type}!")
                elif not has_hit:
                    print("MISS!")
                    hit_last = ""
                    core_hit = ""
                if game_map == "Small":
                    player_map_small.update_grid_shot(choice, has_hit)
                elif game_map == "Medium":
                    player_map_medium.update_grid_shot(choice, has_hit)
                elif game_map == "Large":
                    player_map_large.update_grid_shot(choice, has_hit)
                if player_ships_sunk >= 5:
                    game_finished = True
                if not game_finished:
                    current_turn = "player"
        else:
            if not validity or not extra_validity:
                if focus_direction == "right":
                    focus_direction = "down"
                    enemy_turn(difficulty, size)
                elif focus_direction == "down":
                    focus_direction = "left"
                    enemy_turn(difficulty, size)
                elif focus_direction == "left":
                    focus_direction = "up"
                    enemy_turn(difficulty, size)
                elif focus_direction == "up":
                    hit_last = core_hit
                    focus_direction = "right"
                    enemy_turn(difficulty, size)
            if validity and extra_validity:
                all_hit_grids_enemy.append(choice)
                for i in range(len(player_map_input)):
                    if choice == player_map_input[i]:
                        has_hit = True
                        score -= 5
                        hit_last = choice
                        print("HIT!")
                if has_hit:
                    shot_result = ship_hit(choice, "enemy")
                    if shot_result.sunk:
                        score -= 50
                        player_ships_sunk += 1
                        core_hit = ""
                        hit_last = ""
                        print(f"The enemy has sunk your {shot_result.type}!")
                elif not has_hit:
                    print("MISS!")
                    if focus_direction == "right":
                        focus_direction = "down"
                    elif focus_direction == "down":
                        focus_direction = "left"
                    elif focus_direction == "left":
                        focus_direction = "up"
                    elif focus_direction == "up":
                        hit_last = core_hit
                        focus_direction = "right"
                if game_map == "Small":
                    player_map_small.update_grid_shot(choice, has_hit)
                elif game_map == "Medium":
                    player_map_medium.update_grid_shot(choice, has_hit)
                elif game_map == "Large":
                    player_map_large.update_grid_shot(choice, has_hit)
                if player_ships_sunk >= 5:
                    game_finished = True
                if not game_finished:
                    current_turn = "player"


def enemy_turn(difficulty, size):
    """function that guides the AI's turn"""
    game_map = map_size(size)
    a_i = ai_difficulty(difficulty)
    validity = False
    extra_validity = True
    choice = ""
    global hit_last, core_hit, focus_direction
    if a_i == "Easy":
        if game_map == "Small":
            col_num = random.randrange(1, 11)
            collumn = convert_number(col_num)
            row_num = random.randrange(1, 11)
            row = str(row_num)
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-small")
            row_validity = valid_general_input(row, "place-row-small")
            if col_validity and row_validity:
                validity = True
            extra_validity = valid_specific_input(
                choice, "shoot", "enemy", "", "", "")
        elif game_map == "Medium":
            col_num = random.randrange(1, 16)
            collumn = convert_number(col_num)
            row_num = random.randrange(1, 16)
            row = str(row_num)
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-medium")
            row_validity = valid_general_input(row, "place-row-medium")
            if col_validity and row_validity:
                validity = True
            extra_validity = valid_specific_input(
                choice, "shoot", "enemy", "", "", "")
        elif game_map == "Large":
            col_num = random.randrange(1, 16)
            collumn = convert_number(col_num)
            row_num = random.randrange(1, 16)
            row = str(row_num)
            choice = collumn + row
            col_validity = valid_general_input(collumn, "place-col-large")
            row_validity = valid_general_input(row, "place-row-large")
            if col_validity and row_validity:
                validity = True
            extra_validity = valid_specific_input(
                choice, "shoot", "enemy", "", "", "")
    elif a_i == "Normal":
        if hit_last == "":
            if game_map == "Small":
                col_num = random.randrange(1, 11)
                collumn = convert_number(col_num)
                row_num = random.randrange(1, 11)
                row = str(row_num)
                choice = collumn + row
                col_validity = valid_general_input(collumn, "place-col-small")
                row_validity = valid_general_input(row, "place-row-small")
                if col_validity and row_validity:
                    validity = True
                extra_validity = valid_specific_input(
                    choice, "shoot", "enemy", "", "", "")
            elif game_map == "Medium":
                col_num = random.randrange(1, 16)
                collumn = convert_number(col_num)
                row_num = random.randrange(1, 16)
                row = str(row_num)
                choice = collumn + row
                col_validity = valid_general_input(collumn, "place-col-medium")
                row_validity = valid_general_input(row, "place-row-medium")
                if col_validity and row_validity:
                    validity = True
                extra_validity = valid_specific_input(
                    choice, "shoot", "enemy", "", "", "")
            elif game_map == "Large":
                col_num = random.randrange(1, 16)
                collumn = convert_number(col_num)
                row_num = random.randrange(1, 16)
                row = str(row_num)
                choice = collumn + row
                col_validity = valid_general_input(collumn, "place-col-large")
                row_validity = valid_general_input(row, "place-row-large")
                if col_validity and row_validity:
                    validity = True
                extra_validity = valid_specific_input(
                    choice, "shoot", "enemy", "", "", "")
        else:
            direction = random.randrange(1, 5)
            collumn = hit_last[:1]
            col_num = convert_letter(collumn)
            row = hit_last[1:]
            row_num = int(row)
            if direction == 1:
                new_col_num = col_num + 1
                new_collumn = convert_number(new_col_num)
                choice = new_collumn + row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-small")
                    row_validity = valid_general_input(row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-medium")
                    row_validity = valid_general_input(row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-large")
                    row_validity = valid_general_input(row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
            elif direction == 2:
                new_row_num = row_num + 1
                new_row = str(new_row_num)
                choice = collumn + new_row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        collumn, "place-col-small")
                    row_validity = valid_general_input(
                        new_row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        collumn, "place-col-medium")
                    row_validity = valid_general_input(
                        new_row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        collumn, "place-col-large")
                    row_validity = valid_general_input(
                        new_row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
            elif direction == 3:
                new_col_num = col_num - 1
                new_collumn = convert_number(new_col_num)
                choice = new_collumn + row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-small")
                    row_validity = valid_general_input(row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-medium")
                    row_validity = valid_general_input(row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-large")
                    row_validity = valid_general_input(row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
            elif direction == 4:
                new_row_num = row_num - 1
                new_row = str(new_row_num)
                choice = collumn + new_row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        collumn, "place-col-small")
                    row_validity = valid_general_input(
                        new_row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        collumn, "place-col-medium")
                    row_validity = valid_general_input(
                        new_row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        collumn, "place-col-large")
                    row_validity = valid_general_input(
                        new_row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
    elif a_i == "Hard":
        if core_hit == "":
            if game_map == "Small":
                col_num = random.randrange(1, 11)
                collumn = convert_number(col_num)
                row_num = random.randrange(1, 11)
                row = str(row_num)
                choice = collumn + row
                col_validity = valid_general_input(collumn, "place-col-small")
                row_validity = valid_general_input(row, "place-row-small")
                if col_validity and row_validity:
                    validity = True
                extra_validity = valid_specific_input(
                    choice, "shoot", "enemy", "", "", "")
            elif game_map == "Medium":
                col_num = random.randrange(1, 16)
                collumn = convert_number(col_num)
                row_num = random.randrange(1, 16)
                row = str(row_num)
                choice = collumn + row
                col_validity = valid_general_input(collumn, "place-col-medium")
                row_validity = valid_general_input(row, "place-row-medium")
                if col_validity and row_validity:
                    validity = True
                extra_validity = valid_specific_input(
                    choice, "shoot", "enemy", "", "", "")
            elif game_map == "Large":
                col_num = random.randrange(1, 16)
                collumn = convert_number(col_num)
                row_num = random.randrange(1, 16)
                row = str(row_num)
                choice = collumn + row
                col_validity = valid_general_input(collumn, "place-col-large")
                row_validity = valid_general_input(row, "place-row-large")
                if col_validity and row_validity:
                    validity = True
                extra_validity = valid_specific_input(
                    choice, "shoot", "enemy", "", "", "")
        else:
            collumn = hit_last[:1]
            col_num = convert_letter(collumn)
            row = hit_last[1:]
            row_num = int(row)
            if focus_direction == "right":
                new_col_num = col_num + 1
                new_collumn = convert_number(new_col_num)
                choice = new_collumn + row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-small")
                    row_validity = valid_general_input(row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-medium")
                    row_validity = valid_general_input(row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-large")
                    row_validity = valid_general_input(row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
            elif focus_direction == "down":
                new_row_num = row_num + 1
                new_row = str(new_row_num)
                choice = collumn + new_row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        collumn, "place-col-small")
                    row_validity = valid_general_input(
                        new_row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        collumn, "place-col-medium")
                    row_validity = valid_general_input(
                        new_row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        collumn, "place-col-large")
                    row_validity = valid_general_input(
                        new_row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
            elif focus_direction == "left":
                new_col_num = col_num - 1
                new_collumn = convert_number(new_col_num)
                choice = new_collumn + row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-small")
                    row_validity = valid_general_input(row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-medium")
                    row_validity = valid_general_input(row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        new_collumn, "place-col-large")
                    row_validity = valid_general_input(row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
            elif focus_direction == "up":
                new_row_num = row_num - 1
                new_row = str(new_row_num)
                choice = collumn + new_row
                if game_map == "Small":
                    col_validity = valid_general_input(
                        collumn, "place-col-small")
                    row_validity = valid_general_input(
                        new_row, "place-row-small")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Medium":
                    col_validity = valid_general_input(
                        collumn, "place-col-medium")
                    row_validity = valid_general_input(
                        new_row, "place-row-medium")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
                elif game_map == "Large":
                    col_validity = valid_general_input(
                        collumn, "place-col-large")
                    row_validity = valid_general_input(
                        new_row, "place-row-large")
                    if col_validity and row_validity:
                        validity = True
                    extra_validity = valid_specific_input(
                        choice, "shoot", "enemy", "", "", "")
    enemy_turn_output(choice, validity, extra_validity, difficulty, size)


def save_score(choice, difficulty):
    """function that controls saving the score"""
    print("placeholder")


def finish_game_output(difficulty, size, choice, validity):
    """function that controls output of finish_game"""
    global game_finished, current_turn, score, player_ships_sunk
    global enemy_ships_sunk, last_hit, focus_direction, core_hit
    global victory, player_map_input, player_invalid_h
    global player_invalid_v, enemy_map_input, enemy_invalid_h
    global enemy_invalid_v, all_hit_grids_player
    global all_hit_grids_enemy, battleship_pgrid1, battleship_pgrid2
    global battleship_pgrid3, battleship_pgrid4, battleship_pgrid5
    global battleship_egrid1, battleship_egrid2, battleship_egrid3
    global battleship_egrid4, battleship_egrid5
    if not validity:
        print("Invalid Input")
        print(f"Please enter one of the following: {ENDING_SCREEN}")
        finish_game(difficulty, size)
    elif validity:
        game_finished = False
        current_turn = ""
        score = 0
        player_ships_sunk = 0
        enemy_ships_sunk = 0
        last_hit = ""
        focus_direction = "right"
        core_hit = ""
        victory = False
        player_map_input = []
        player_invalid_h = []
        player_invalid_v = []
        enemy_map_input = []
        enemy_invalid_h = []
        enemy_invalid_v = []
        all_hit_grids_player = []
        all_hit_grids_enemy = []
        battleship_pgrid1 = ""
        battleship_pgrid2 = ""
        battleship_pgrid3 = ""
        battleship_pgrid4 = ""
        battleship_pgrid5 = ""
        battleship_egrid1 = ""
        battleship_egrid2 = ""
        battleship_egrid3 = ""
        battleship_egrid4 = ""
        battleship_egrid5 = ""
        if choice == "1" or choice == "s" or choice == "start":
            start_game(difficulty, size)
        elif choice == "2" or choice == "r" or choice == "return":
            menu_screen(0, 0)
        elif choice == "3" or choice == "l" or choice == "leaderboard":
            leaderboard_screen(difficulty, size)


def finish_game(difficulty, size):
    """function that controls the finishing of the game"""
    game_map = map_size(size)
    if game_map == "Small":
        print("Your Final Grid:")
        player_map_small.print_grid()
        print("The Enemy's Final Grid:")
        enemy_map_small.print_grid()
    elif game_map == "Medium":
        print("Your Final Grid:")
        player_map_medium.print_grid()
        print("The Enemy's Final Grid:")
        enemy_map_medium.print_grid()
    elif game_map == "Large":
        print("Your Final Grid:")
        player_map_large.print_grid()
        print("The Enemy's Final Grid:")
        enemy_map_large.print_grid()
    if victory:
        print("VICTORY!")
        print("Congratulations! You have sunk the enemy fleet.")
        print(f"Your final score was: {score}")
        print("Would you like to save your score?")
        print("1. [Y]es")
        print("2. [N]o")
        choice1 = input("Please enter your choice here: \n").lower()
        save_score(choice1, difficulty)
    elif not victory:
        print("DEFEATED!")
        print("Your fleet has been sunk. Better luck next time.")
        print(f"Your final score was: {score}")
    print("What would like to do now?")
    print("1. [S]tart again")
    print("2. [R]eturn to main menu")
    print("3. [L]eaderboard")
    choice2 = input("Please enter your choice here: \n").lower()
    validity = valid_general_input(choice2, "ending")
    finish_game_output(difficulty, size, choice2, validity)


def start_game(difficulty, size):
    """funtion that controls the game starting"""
    global current_turn, victory
    place_ships(size)
    first_turn = random.randrange(1, 3)
    if first_turn == 1:
        current_turn = "player"
    elif first_turn == 2:
        current_turn = "enemy"
    while not game_finished:
        if current_turn == "player":
            print("YOUR TURN")
            print("ENEMY GRID:")
            if size == 0:
                hidden_map_small.print_grid()
            elif size == 1:
                hidden_map_medium.print_grid()
            elif size == 1:
                hidden_map_large.print_grid()
            player_turn(size)
        elif current_turn == "enemy":
            print("AI TURN")
            enemy_turn(difficulty, size)
            if size == 0:
                player_map_small.print_grid()
            elif size == 1:
                player_map_medium.print_grid()
            elif size == 1:
                player_map_large.print_grid()
    if game_finished:
        finish_game(difficulty, size)


def menu_output(validity, choice, difficulty, size):
    """funtion controls result of user input on menu screen"""
    if not validity:
        print(
            f"Invalid input, please input one of the following: {MENU_INPUT}"
            )
        menu_screen(difficulty, size)

    if choice == "1" or choice == "s" or choice == "start":
        start_game(difficulty, size)
    elif choice == "2" or choice == "o" or choice == "options":
        options_screen(difficulty, size)
    elif choice == "3" or choice == "l" or choice == "leaderboard":
        leaderboard_screen(difficulty, size)


def menu_screen(difficulty, size):
    """function that controls menu screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)

    print("BATTLESHIPS")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [S]tart")
    print("2. [O]ptions")
    print("3. [L]eaderboard")
    choice = input("Please enter your choice here: \n").lower()
    validity = valid_general_input(choice, "menu")
    menu_output(validity, choice, difficulty, size)


def options_output(validity, choice, difficulty, size):
    """funtion controls result of user input on menu screen"""
    if not validity:
        print(
            f"Invalid input, please input one of the following:{OPTIONS_INPUT}"
            )
        options_screen(difficulty, size)

    if choice == "1" or choice == "d" or choice == "difficulty":
        difficulty_screen(difficulty, size)
    elif choice == "2" or choice == "m" or choice == "map":
        map_screen(difficulty, size)
    elif choice == "3" or choice == "b" or choice == "back":
        menu_screen(difficulty, size)


def options_screen(difficulty, size):
    """funtion that controls the options screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)
    print("OPTIONS")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [D]ifficulty")
    print("2. [M]ap")
    print("3. [B]ack")
    choice = input("Please enter your choice here: \n").lower()
    validity = valid_general_input(choice, "options")
    options_output(validity, choice, difficulty, size)


def difficulty_output(validity, choice, difficulty, size):
    """funtion controls result of user input on difficulty screen"""
    if not validity:
        print(
            f"Invalid input, please input one of the following: {AI_INPUT}"
            )
        difficulty_screen(difficulty, size)

    if choice == "1" or choice == "e" or choice == "easy":
        difficulty = 0
        difficulty_screen(difficulty, size)
    elif choice == "2" or choice == "n" or choice == "normal":
        difficulty = 1
        difficulty_screen(difficulty, size)
    elif choice == "3" or choice == "h" or choice == "hard":
        difficulty = 2
        difficulty_screen(difficulty, size)
    elif choice == "4" or choice == "b" or choice == "back":
        options_screen(difficulty, size)


def difficulty_screen(difficulty, size):
    """funtion that controls the difficulty screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)
    print("DIFFICULTY")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [E]asy")
    print("2. [N]ormal")
    print("3. [H]ard")
    print("4. [B]ack")
    choice = input("Please enter your choice here: \n").lower()
    validity = valid_general_input(choice, "difficulty")
    difficulty_output(validity, choice, difficulty, size)


def map_output(validity, choice, difficulty, size):
    """funtion controls result of user input on map size screen"""
    if not validity:
        print(
            f"Invalid input, please input from the following: {MAP_SIZE_INPUT}"
            )
        map_screen(difficulty, size)

    if choice == "1" or choice == "s" or choice == "small":
        size = 0
        map_screen(difficulty, size)
    elif choice == "2" or choice == "m" or choice == "medium":
        size = 1
        map_screen(difficulty, size)
    elif choice == "3" or choice == "l" or choice == "large":
        size = 2
        map_screen(difficulty, size)
    elif choice == "4" or choice == "b" or choice == "back":
        options_screen(difficulty, size)


def map_screen(difficulty, size):
    """funtion that controls the map size screen"""
    a_i = ai_difficulty(difficulty)
    game_map = map_size(size)
    print("MAP SIZE")
    print(f"Current Difficulty: {a_i} - Current Map Size: {game_map}")
    print("1. [S]mall (10x10)")
    print("2. [M]edium (15x15)")
    print("3. [L]arge (20x20)")
    print("4. [B]ack")
    choice = input("Please enter your choice here: \n").lower()
    validity = valid_general_input(choice, "size")
    map_output(validity, choice, difficulty, size)


def leaderboard_screen(difficulty, size):
    """function that controls the leaderboard screen"""
    print("placeholder")


# menu_screen(0, 0)
victory = True
finish_game(0, 0)
