import json
import os

# Define a mapping of Pokémon types to emojis
pokemon_types = {
  "normal": "🐾",
    "fire": "🔥",
    "water": "💧",
    "electric": "⚡",
    "grass": "🌿",
    "ice": "❄️",
    "fighting": "🥊",
    "poison": "☠️",
    "ground": "🌍",
    "flying": "🕊️",
    "psychic": "🔮",
    "bug": "🐛",
    "rock": "🪨",
    "ghost": "👻",
    "dragon": "🐉",
    "dark": "🌑",
    "steel": "🔩",
    "fairy": "✨"
}

class PokemonCollection:
    def __init__(self, filename="pokemon_collection.json"):
        self.filename = filename
        self.pokemon_list = self.load_collection()

    def load_collection(self):
        """Load Pokémon collection from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_collection(self):
        """Save the current Pokémon collection to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.pokemon_list, file, indent=4)

    def add_pokemon(self, pokemon):
        """Add a new Pokémon to the collection."""
        self.pokemon_list.append(pokemon.__dict__)
        self.save_collection()

    def find_pokemon(self, name):
        """Check if a Pokémon is already in the collection by name."""
        for poke in self.pokemon_list:
            if poke["name"].lower() == name.lower():
                return poke
        return None

    def show_collection(self):
        """Display the entire Pokémon collection."""
        if not self.pokemon_list:
            print("Your Pokémon collection is empty.")
            return

        for poke in self.pokemon_list:
            # Prepare a list of type strings with emojis
            types_with_emojis = [f"{type_name} {pokemon_types[type_name]}" for type_name in poke['types'] if type_name in pokemon_types]  # Combine type names with emojis
            types_display = ', '.join(types_with_emojis)  # Join for display
            abilities_display = ', '.join(poke['abilities'])  # Join abilities for display
            print(f"Name: {poke['name']}, Types: {types_display}, Abilities: {abilities_display}")
