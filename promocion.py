import sys
from copy import deepcopy

class Influencer:
    def __init__(self, id_, name, value):
        self.id = id_
        self.name = name
        self.value = value
        self.incompatible_ids = set()

# Parseo de linea de archivo
def parse_line(line):
    parts = line.strip().split(',')
    try:
        id_ = int(parts[0])
        name = parts[1]
        value = int(parts[2])
        influencer = Influencer(id_, name, value)
        influencer.incompatible_ids = set(int(x) for x in parts[3:] if x.isdigit())
        return influencer
    except (IndexError, ValueError):
        return None

def calculate_total_value(selected_influencers):
    return sum(influencer.value for influencer in selected_influencers)

def is_compatible(influencer, selected_influencers):
    for selected in selected_influencers:
        if influencer.id in selected.incompatible_ids or selected.id in influencer.incompatible_ids:
            return False
    return True

def branch_and_bound(influencers_list, selected_influencers, max_value, current_value, idx):
    if idx == len(influencers_list):
        return selected_influencers, current_value

    influencer = influencers_list[idx]

    if not is_compatible(influencer, selected_influencers):
        return branch_and_bound(influencers_list, selected_influencers, max_value, current_value, idx + 1)

    selected_influencers.append(influencer)
    selected, value = branch_and_bound(influencers_list, deepcopy(selected_influencers), max_value, current_value + influencer.value, idx + 1)
    selected_influencers.pop()
    
    if value > max_value:
        max_value = value
        selected_influencers = selected

    selected, value = branch_and_bound(influencers_list, deepcopy(selected_influencers), max_value, current_value, idx + 1)
    if value > max_value:
        max_value = value
        selected_influencers = selected

    return selected_influencers, max_value

if __name__ == "__main__":
    
    # Chequeo de parametros
    if len(sys.argv) != 2:
        print("Usage: python promocion.py filename")
        sys.exit(1)

    # Leer el archivo
    filename = sys.argv[1]
    influencers_list = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                influencer = parse_line(line)
                if influencer:
                    influencers_list.append(influencer)
    except FileNotFoundError:
        print("File not found:", filename)
        sys.exit(1)

    # Ordenar influencers por valor
    influencers_list.sort(key=lambda x: x.value, reverse=True)

    # Inicializar variables
    selected_influencers = []
    max_value = float('-inf')

    # Branch and Bound
    selected_influencers, max_value = branch_and_bound(influencers_list, selected_influencers, max_value, 0, 0)

    # Output
    print("Valor conseguido:", max_value,"\n")
    for influencer in selected_influencers:
        print(f"{influencer.name}")
   
