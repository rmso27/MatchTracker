import json
import configparser
from tabulate import tabulate

# Read configurations
config = configparser.ConfigParser()
config.read('configs/configs.ini')

PLAYERS_LIST = config['players']['PLAYERS_LIST']

def create_player():

    players_data_dump = open(PLAYERS_LIST)
    players_data_load = json.load(players_data_dump)

    player_name = input("Nome: ")

    player_data = {
        "id": len(players_data_load['players']) + 1,
        "name": player_name,
        "matches": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "ratio": "0.00%"
    }

    players_data_load['players'] += [player_data]

    json_object = '{"players":' + json.dumps(players_data_load['players']) + '}'

    with open (PLAYERS_LIST, 'w') as outfile:
        outfile.write(json_object)

    print_table()

    add_new_player = input("Queres adicionar outro  jogador? (S / N)")

    if add_new_player == "S":
        create_player()
    if add_new_player == "N":
        exit()

def read_players():

    players_data_dump = open(PLAYERS_LIST)
    players_data_load = json.load(players_data_dump)
    players_data = []

    for player in range(len(players_data_load['players'])):
        players_data += [[
            players_data_load['players'][player]['id'],
            players_data_load['players'][player]['name'],
            players_data_load['players'][player]['matches'],
            players_data_load['players'][player]['wins'],
            players_data_load['players'][player]['draws'],
            players_data_load['players'][player]['losses'],
            players_data_load['players'][player]['ratio']
        ]]

    return players_data

def print_table():

    players_table_data = [["ID", "Nome", "Jogos", "Vitorias", "Empates", "Derrotas", "Ratio"]]
    players_table_data += read_players()
    players_table = tabulate(players_table_data, headers = 'firstrow')

    print(players_table)

# Main
option = input("Opções:\n1 - Ver tabela classificativa\n2 - Criar jogador\n")
if option == "1":
    print_table()
if option == "2":
    create_player()