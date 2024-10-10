import requests  # type: ignore # Import requests for making API calls

class APIHandler:
    BASE_URL = "https://pokeapi.co/api/v2"  # Base URL for the Pokémon API

    @staticmethod
    def get_pokemon_list(limit=10):
        """Fetch a list of Pokémon names."""
        url = f"{APIHandler.BASE_URL}/pokemon?limit={20}"  # Create URL for fetching Pokémon list
        response = requests.get(url)  # Make the API request
        if response.status_code == 200:  # Check if the response was successful
            return response.json()["results"]  # Return the list of Pokémon names
        else:
            print("Failed to fetch Pokémon list.")  # Notify on failure
            return []  # Return an empty list if the fetch fails

    @staticmethod
    def get_pokemon_details(pokemon_name):
        """Fetch Pokémon details by name."""
        url = f"{APIHandler.BASE_URL}/pokemon/{pokemon_name.lower()}"  # Create URL for fetching specific Pokémon details
        response = requests.get(url)  # Make the API request
        if response.status_code == 200:  # Check if the response was successful
            return response.json()  # Return the detailed Pokémon data
        else:
            print(f"Failed to fetch details for {pokemon_name}.")  # Notify on failure
            return None  # Return None if the fetch fails
