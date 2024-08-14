from langchain_core.documents import Document

def embed_text(filepath: str, filename: str) -> list[Document]:
    documents = []
    curr_str = ""
    file = open(filepath, "r")

    for line in file.readlines():
        if line == "=========================================================\n":
            doc = Document(
                page_content=curr_str,
                metadata={"file_name": filename}
            )

            documents.append(doc)
            curr_str = ""
        else:
            curr_str += line

    documents.append(Document(
                page_content=curr_str,
                metadata={"file_name": filename}
            ))
    return documents

def locationsByPokemon(doc):
    file = open(doc, "r")
    lines = file.readlines()
    
    # dictionary to store constant levels
    levels = {"Old Rod": 10, "Good Rod": 25, "Super Rod": 50, "All Rods": "1 - 100"}

    # dictionary to store the pokemon to their locations
    pokemons = {} 

    line_num = 11
    location = None
    location_levels = {}

    while True:
        if line_num >= len(lines):
            break
        if not location:
            location = lines[line_num].strip()
            temp_loc_levels = lines[line_num + 1][7:].strip().split(", ")
            for temp in temp_loc_levels:
                num_split = temp.index(" (")
                location_levels[temp[num_split + 2:-1]] = temp[:num_split]
            line_num += 2
            continue
        elif lines[line_num].strip() == "=========================================================":
            location = None
            location_levels = {}
        else:
            method = lines[line_num][0:12].strip()

            if method in levels:
                level = levels[method]
            else:
                if method == "Surf":
                    level = location_levels["Surfing"]
                elif method == "Honey Tree":
                    level = location_levels["Honey Tree"]
                else:
                    level = location_levels["Walking"]

            method_pokemon = lines[line_num][12:].strip().split(", ")

            for pokemon in method_pokemon:
                percent_index = pokemon.index(" (")
                pokemon_name = pokemon[:percent_index]

                if pokemon_name == "Nidoranâ™":
                    pokemon_name = "Nidoran Female"
                elif pokemon_name == "Nidoranâ™€":
                    pokemon_name = "Nidoran Male"

                percent = pokemon[percent_index + 2:-1]

                if pokemon_name not in pokemons:
                    pokemons[pokemon_name] = []
                pokemons[pokemon_name].append(f"{location} by {method} at level {level} with a {percent} chance")
        line_num += 1

    file = open("documents/LocationsByPokemon.txt", "w")
    for pokemon in pokemons:
        file.write(f"{pokemon}:\n")
        for location in pokemons[pokemon]:
            file.write(f"{location}\n")
        file.write("=========================================================\n")
