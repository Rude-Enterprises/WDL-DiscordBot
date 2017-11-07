import pandas as pd

def rename_dataframe_index_player(dataframe):
    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index().dropna().set_index("nick")
    dataframe = dataframe.rename(lambda x: x.lower())
    dataframe = dataframe.drop(["index"], axis=1)
    return dataframe

player_totals_column_names = ["nick", "rat", "orat",
                              "drat", "eff", "frags",
                              "kdr", "dmg", "def",
                              "pow", "touches", "ptouches",
                              "caps", "pcaps", "points",
                              "cap%", "assists", "win%",
                              "rp", "gp"]


season_column_names = ["nick", "rat", "orat",
                       "drat", "eff", "frags",
                       "kdr", "dmg", "def",
                       "pow", "touches", "ptouches",
                       "caps", "pcaps", "points",
                       "cap%", "rp", "gp"]

alltime_playoff_column_names = ["nick", "rat", "orat",
                                "drat", "eff", "frags",
                                "kdr", "dmg", "def",
                                "pow", "touches", "ptouches",
                                "caps", "pcaps", "points",
                                "cap%", "win%", "rp", "gp"]

all_rounds_column_names = ["nick", "team", "rat",
                           "orat", "drat", "eff",
                           "frags", "deaths", "dmg",
                           "def", "pow", "touches",
                           "ptouches", "caps", "pcaps",
                           "assists", "cap%", "res",
                           "kdr", "id", "sid"]

team_stats_column_names = ["team", "rat", "orat",
                           "drat", "deaths", "eff",
                           "frags", "dmg", "kdr",
                           "pow", "touches", "ptouches",
                           "caps", "pcaps", "points",
                           "assists", "cap%", "win%",
                           "rp", "gp", "season",
                           "eff2", "def2", "spoints",
                           "wins", "losses", "ties"]

#all sheets to be used from Jwarrier's wdlstatsv4 read with Pandas
workbook = pd.ExcelFile("WDLSTATSv4.xlsx")
player_totals = pd.read_excel(workbook, "PT Player Totals", names=player_totals_column_names)
player_avg = pd.read_excel(workbook, "PT PlayerAVG")
all_time_playoff = pd.read_excel(workbook, "ALL TIME Playoffs", skiprows=[0], names=alltime_playoff_column_names)
season7 = pd.read_excel(workbook, "Season 7", skiprows=[0], names=season_column_names)
season6 = pd.read_excel(workbook, "Season 6", skiprows=[0], names=season_column_names)
season5 = pd.read_excel(workbook, "Season 5", skiprows=[0], names=season_column_names)
season4 = pd.read_excel(workbook, "Season 4", skiprows=[0], names=season_column_names)
season3 = pd.read_excel(workbook, "Season 3", skiprows=[0], names=season_column_names)
season2 = pd.read_excel(workbook, "Season 2", skiprows=[0], names=season_column_names)
season1 = pd.read_excel(workbook, "Season 1", skiprows=[0], names=season_column_names)
team_stats = pd.read_excel(workbook, "Team Stats", skiprows=[0], index_col=[1], names=team_stats_column_names)
all_rounds = pd.read_excel(workbook, "All Rounds", names=all_rounds_column_names, parse_cols=20)
map_data = pd.read_excel(workbook, "Map Data", index_col=[11])
map_rat_player = pd.read_excel(workbook, "Map RAT by Player", index_col=[1])
map_rat_team = pd.read_excel(workbook, "Map RAT by Team", index_col=[0])


#Renaming dataframe indexes
player_totals = rename_dataframe_index_player(player_totals)
season7 = rename_dataframe_index_player(season7)
season6 = rename_dataframe_index_player(season6)
season5 = rename_dataframe_index_player(season5)
season4 = rename_dataframe_index_player(season4)
season3 = rename_dataframe_index_player(season3)
season2 = rename_dataframe_index_player(season2)
season1 = rename_dataframe_index_player(season1)
all_rounds = all_rounds.dropna()
all_rounds = all_rounds.reset_index().dropna().set_index("nick")


stat_dict = {"rat": "RAT",
             "orat": "oRAT",
             "drat": "dRAT",
             "frags": "Frags",
             "eff": "EFF",
             "kdr": "K/D",
             "dmg": "DMG",
             "def": "DEF",
             "pow": "POW",
             "touches": "Touches",
             "ptouches": "PTouches",
             "caps": "Caps",
             "pcaps": "PCaps",
             "points": "Points",
             "assists": "Assists",
             "cap%": "Cap%",
             "win%": "Win%",
             "season": "Season",
             "wins": "Wins",
             "losses": "Losses",
             "ties": "Ties",
             "deaths": "Deaths"
             }

team_dict = {1: "ADD 1", 2: "SUC 1", 3: "SDC 1",
             4: "TMC 1", 5: "SUP 1", 6: "SHQ 1",
             7: "SUC 2", 8: "GPS 2", 9: "WUM 2",
             10: "SDC 2", 11: "NSP 2", 12: "SSG 2",
             13: "SUC 3", 14: "SDC 3", 15: "CDC 3",
             16: "GPS 3", 17: "TDT 3", 18: "REG 3",
             19: "SUC 4", 20: "DEA 4", 21: "REG 4",
             22: "OVS 4", 23: "GPS 4", 24: "SXP 4",
             25: "SUC 5", 26: "GPS 5", 27: "SXP 5",
             28: "TDT 5", 29: "WUM 5", 30: "BST 5",
             32: "SDM 6", 33: "SUC 6", 34: "SXP 6",
             35: "CDC 6", 36: "TDT 6", 37: "GPS 6",
             38: "SUC 7", 39: "GPS 7", 40: "HYP 7",
             41: "TDT 7", 42: "HFM 7", 43: "SXP 7",
             44: "TKV 7", 45: "REG 7"
             }

team_dict_inverse = {a: b for b, a in team_dict.items()}

team_dict_two = {"!add": "Adderall Drunk Drivers",
                 "!suc": "Super Chargers",
                 "!sdc": "Stardust Crusaders",
                 "!shq": "Shaq Fu",
                 "!tmc": "The Mall Cops",
                 "!sup": "SuperBots",
                 "!wum": "Wumbologists",
                 "!gps": "Giant Pea Shooters",
                 "!nsp": "None Shall Pass",
                 "!ssg": "Sunday School Gangsters",
                 "!cdc": "Capo Dont Care",
                 "!tdt": "The Dream Team",
                 "!reg": "The Regulators",
                 "!dea": "Doom Enforcement Agency",
                 "!sxp": "Sexual Panthers",
                 "!ovs": "OverratedScumWads",
                 "!bst": "Best Ever",
                 "!sdm": "Super Dank Memes",
                 "!tkv": "Techno Vikings",
                 "!hfm": "High Friction Men",
                 "!hyp": "Hurt You Plenty",
                 "!dem": "Damn!",
                 "!tpt": "The Phantom Troupe"
                 }