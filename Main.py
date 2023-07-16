import sys
import json
from Rules import Rules
from Matches import Match, Matches
from Results import Results

def main():
    # Verificar la cantidad de argumentos recibidos
    if len(sys.argv) < 3:
        print("Uso: Main.py --rules <rules_json> --match <match_json> [--match <match_json> ...]")
        return

    # Variables para almacenar los nombres de archivo JSON de las reglas y los partidos
    rules_json_file = None
    matches_json_files = []

    # Obtener los nombres de archivo JSON de las reglas y los partidos desde los argumentos de la línea de comandos
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--rules":
            if i + 1 < len(sys.argv):
                rules_json_file = sys.argv[i + 1]
                i += 1
            else:
                print("Error: Se esperaba un nombre de archivo JSON después de --rules")
                return
        elif sys.argv[i] == "--match":
            if i + 1 < len(sys.argv):
                matches_json_files.append(sys.argv[i + 1])
                i += 1
            else:
                print("Error: Se esperaba un nombre de archivo JSON después de --match")
                return
        else:
            print("Error: Argumento no reconocido:", sys.argv[i])
            return

        i += 1

    # Cargar las reglas desde el archivo JSON si se especificó
    rules = None
    if rules_json_file:
        with open(rules_json_file) as file:
            rules_data = json.load(file)
        rules = Rules(rules_data)
    else:
        # Crear las reglas con un JSON vacío
        rules = Rules({})

    # Crear la lista de partidos
    matches = Matches()

    # Cargar los partidos desde los archivos JSON
    for match_json_file in matches_json_files:
        with open(match_json_file) as file:
            match_data = json.load(file)

        match = Match(match_data)
        matches.add_match(match)

    # Calcular los resultados utilizando la clase Results y el método calculate_points
    results = Results(matches, rules)
    results_json = results.calculate_points()

    # Imprimir los resultados en formato JSON
    print(results_json)

if __name__ == "__main__":
    main()
