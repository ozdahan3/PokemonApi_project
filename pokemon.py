class Pokemon:
    def __init__(self, name, types, abilities):
        self.name = name  # Name of the Pokémon
        self.types = types  # List of types
        self.abilities = abilities  # List of abilities

    @staticmethod
    def from_api_data(data):
        """Create a Pokémon instance from API data."""
        name = data.get('name', 'Unknown')
        types = [type_info['type']['name'] for type_info in data.get('types', [])]  # Use .get to avoid KeyError
        abilities = [ability_info['ability']['name'] for ability_info in data.get('abilities', [])]  # Use .get for abilities
        return Pokemon(name, types, abilities)

    def display_info(self):
        """Print the Pokémon details in a readable format."""
        print(f"Pokémon: {self.name}")
        print(f"Types: {', '.join(self.types)}")
        print(f"Abilities: {', '.join(self.abilities)}")
