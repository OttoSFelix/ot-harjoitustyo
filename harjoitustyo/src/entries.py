import pandas as pd
import os
from database_connection import get_database_connection

def get_player_classes_from_file(file_path):
    """
    Reads the classes each player plays from a entry excel file
    Args:
        file_path: path to the entry excel file
    Returns:
        dictionary of classes that each player plays eg. {player1: [class1, class2, class3]}
    """
    if not os.path.exists(file_path):
        return "Virhe: Tiedostoa ei löydy."

    try:
        df = pd.read_excel(file_path, engine='openpyxl', header=None)
        
        player_data = {}

        connection = get_database_connection()
        cursor = connection.cursor()
        for index, row in df.iterrows():
            player_name = False
            cleaned_row = [str(item).strip() for item in row.values if pd.notna(item) and str(item).strip() != '']
            
            if not cleaned_row:
                continue
            cursor.execute('SELECT name FROM Ratinglist')
            rows = cursor.fetchall()
            names = [row[0].split(' ')[-1] for row in rows]
            for row in rows:
                names.append(row[0].split(' ')[0])

            for cell in cleaned_row:
                name = cell.split(' ')
                if len(name) > 1:
                    if name[-1].lower().capitalize() in names or name[-2].lower().capitalize() in names:
                        player_name = cell
                        break
            if not player_name:
                continue

            player_index = cleaned_row.index(player_name)
            classes = cleaned_row[player_index+1:]

            if player_name.lower() in ['nimi', 'name', 'sija', 'rank']:
                continue

            player_name = cleaned_row[player_index].split(' ')
            reverse_name = ' '.join(reversed(player_name[-2:]))
            player_name = ' '.join(player_name[-2:])
            if player_name and classes:
                if player_name in player_data.keys():
                    for c in classes:
                        player_data[player_name].append(c)
                elif reverse_name in player_data.keys():
                    for c in classes:
                        player_data[reverse_name].append(c)
                else:
                    full_names = [row[0] for row in rows]
                    if player_name in full_names:
                        player_data[player_name] = classes
                    elif reverse_name in full_names:
                        player_data[reverse_name] = classes
                    else:
                        player_data[player_name] = classes

        return player_data

    except Exception as e:
        return f"Virhe tiedoston luvussa: {e}"

