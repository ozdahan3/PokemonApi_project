import random
import pygame  # type: ignore # Ensure you have pygame installed
from colorama import Fore, Style  # type: ignore # For colored terminal output
from api_handler import APIHandler  # Import API handler
from pokemon import Pokemon  # Import Pokémon class
from pokemon_collection import PokemonCollection  # Import Pokémon collection class
import os
import time 

# Initialize pygame (if using for sounds)
pygame.init()

# Load the music files
pygame.mixer.music.load('game_music.wav')  # Load the menu music
draw_sound = pygame.mixer.Sound('draw_sound.wav')  # Load the draw Pokémon sound effect

# Function to play menu music
def play_menu_music():
    """Play background music on a loop for the menu screen."""
    pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Loop the music indefinitely (-1 for infinite)

def stop_menu_music():
    """Stop the background music."""
    pygame.mixer.music.stop()


pokemon_facts = [
    "Did you know? Pikachu is the mascot of the Pokémon franchise!",
    "Did you know? Bulbasaur is the first Pokémon in the Pokédex!",
    "Did you know? Charizard can fly at speeds of over 100 km/h!",
    "Did you know? Squirtle evolves into Wartortle at level 16!",
    "Did you know? Jigglypuff can put others to sleep by singing!",
    "Did you know? Gengar is known as the Shadow Pokémon!",
    "Did you know? Mewtwo was genetically engineered from Mew!",
    "Did you know? Eevee can evolve into eight different forms!",
]

def show_random_fact():
    """Display a random Pokémon fact."""
    fact = random.choice(pokemon_facts)  # Randomly select a fact from the list
    print(Fore.CYAN + fact + Style.RESET_ALL)  # Print the fact in cyan color


# Define a dictionary for Pokémon types and emojis
pokemon_types = {
    "fire": "🔥",
    "water": "💧",
    "grass": "🍃",
    "electric": "⚡",
    "normal": "🐾",
    "flying": "🕊️",
 
}

def draw_pokemon(collection):
    """Draw a Pokémon from the API and add it to the collection."""
    draw_sound.play() # Play sound when drawing a Pokémon

    # Fetch a list of Pokémon names from the API
    pokemon_list = APIHandler.get_pokemon_list(limit=100)  # Get a larger list of Pokémon
    if not pokemon_list:
        print(Fore.RED + "No Pokémon available to draw." + Style.RESET_ALL)
        return

    # Randomly select a Pokémon from the fetched list
    selected_pokemon = random.choice(pokemon_list)["name"]  

    existing_pokemon = collection.find_pokemon(selected_pokemon)  # Check if it's already in the collection
    if existing_pokemon:
        print(Fore.RED + f"{selected_pokemon} is already in your collection:" + Style.RESET_ALL)
        collection.show_collection()  # Show the existing collection
    else:
        # Fetch actual Pokémon details from the API
        pokemon_data = APIHandler.get_pokemon_details(selected_pokemon)  # Use APIHandler to get Pokémon details
        if pokemon_data:  # Check if data was retrieved successfully
            pokemon_instance = Pokemon.from_api_data(pokemon_data)  # Create a Pokémon instance from API data
            collection.add_pokemon(pokemon_instance)  # Add the new Pokémon to the collection
            print(Fore.GREEN + f"{selected_pokemon} added to your collection!" + Style.RESET_ALL)  # Notify the user of addition
            types_emojis = ", ".join(pokemon_instance.types)  # Join types for display
            print(f"Name: {Fore.GREEN}{pokemon_instance.name}{Style.RESET_ALL}, Types: {types_emojis}, Abilities: {', '.join(pokemon_instance.abilities)}")
        else:
            print(Fore.RED + f"Failed to fetch details for {selected_pokemon}." + Style.RESET_ALL)  # Error message

def print_pokemon_logo():
    """Print the Pokémon logo in ASCII art."""
    logo = r"""
                                      ,'\
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|
    """
    print(Fore.RED + logo + Style.RESET_ALL)

#def print_pokeball():
#    """Print a Pokéball in ASCII art."""
#    pokeball = r"""
 #⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣶⣶⣶⣶⣶⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⡿⠿⠛⠛⠋⠉⠉⠉⠉⠉⠙⠛⠻⠿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀
##⠀⠀⠀⠀⠀⢀⣴⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣦⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣠⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣷⡄⠀⠀⠀
#⠀⠀⠀⣼⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣆⠀⠀
#⠀⠀⣼⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣆⠀
#⠀⢰⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡄
#⠀⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣧
#⢸⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
#⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
#⢸⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿
#⠈⣿⣿⣿⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡿
#⠀⢻⣿⡿⢿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⠿⠟⠛⠿⢿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⡿⣿⣿⡇
#⠀⠈⢿⣿⡄⠉⠛⠿⣿⣷⣶⣤⣤⣀⣠⣿⡿⠋⢠⠴⠒⠒⠲⢤⡈⠻⣿⣷⣀⣠⣤⣴⣶⣿⡿⠿⠋⠁⣰⣿⡟⠀
#⠀⠀⠈⢿⣿⡄⠀⠀⠀⠌⠉⠛⠻⠿⣿⣿⡇⠀⡏⠀⠀⠀⠀⠈⡇⠀⢻⣿⡿⠿⠛⠛⠉⠁⠀⠀⠀⣰⣿⡟⠀⠀
#⠀⠀⠀⠈⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⡀⠻⣄⡀⠀⣀⡴⠃⢠⣿⣿⠁⠀⠀⠀⠀⠀⠀⢀⣼⣿⠟⠀⠀⠀
#⠀⠀⠀⠀⠻⣿⣷⣄⡀⠀⠀⠀⠀⠀⠙⢿⣿⣦⣄⣉⣉⣁⣤⣶⣿⠿⠁⠀⠀⠀⠀⠀⢀⣴⣿⡿⠋⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣦⣀⠀⠀⠀⠀⠀⠉⠛⠿⠿⠿⠿⠟⠋⠁⠀⠀⠀⠀⠀⣠⣴⣿⡿⠋⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣶⣿⡿⠟⠉⠀⠈⠈⠁⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⢿⣿⣿⣷⣶⣶⣶⣿⣿⣿⡿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#    """
#    print(pokeball)
#
def print_welcome():
    """Print a stylized welcome message."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    print_pokemon_logo()  # Print the Pokémon logo
    #print_pokeball()  # Print the Pokéball
    print(Fore.YELLOW + "\n" + "=" * 60 +Style.RESET_ALL)
    print("       Hello and welcome to the Pokémon Collection!   ")
    print(Fore.YELLOW + "=" * 60 +Style.RESET_ALL)


def print_menu():
    """Print the menu with stylized formatting."""

    menu_art = r""" __  __                  
|  \/  | ___ _ __  _   _ 
| |\/| |/ _ \ '_ \| | | |
| |  | |  __/ | | | |_| |
|_|  |_|\___|_| |_|\__,_| 
"""
    
    print(Fore.BLUE + menu_art + Style.RESET_ALL)
    print(Fore.WHITE + "1. 🎨 Draw a Pokémon")
    print("2. 📚 View My Pokémon Collection")
    print("3. 🔍 Search for a Pokémon")
    print("4. 📖 Show a Random Pokémon Fact")
    print("5. ❌ Exit the Application" + Style.RESET_ALL)  
    print('')

def print_notification(message, color=Fore.GREEN):
    """Print a notification in the specified color."""
    print(color + f"[INFO] {message}" + Style.RESET_ALL)

def loading_effect(duration=1):
    """Simulate a loading effect for the given duration in seconds."""
    for _ in range(duration):
        time.sleep(1)  # Simulating a delay of 2 second
    print(" Done! this is a pokemon fact : ")

def main():
    """Main function to run the Pokémon collection program."""
    play_menu_music()
    collection = PokemonCollection('pokemon_collection.json')  # Create a PokémonCollection object
    running = True  # Flag variable to control the loop

    while running:
        print_welcome()  # Print the welcome message
        print_menu()  # Print the menu

        choice = input("Please enter your choice from the Menu: ")

        # Menu Functionality
        if choice == "1":
            stop_menu_music()  # Stop the music before drawing the Pokémon
            print('')
            print('The pokemon that has been draw is : ')
            print('')
            draw_pokemon(collection)  
            print('')  
            print(Fore.GREEN + '✨ Awesome!' + Style.RESET_ALL, end=" ")  # Green text
            print(Fore.YELLOW + 'You just drew a Pokémon!' + Style.RESET_ALL)  # Yellow text
            loading_effect()
            play_menu_music()  # Resume the music after action


        elif choice == "2":
            print('')
            print('This is Your Pokémon Collection!')
            collection.show_collection()  # Show collection
            print('')  
            print(Fore.BLUE + 'WoW!!' + Style.RESET_ALL, end=" ")  
            print(Fore.WHITE + 'what a nice collection!!' + Style.RESET_ALL)

        elif choice == "3":
            # Search for a Pokémon in the collection
            search_name = input("🔍 Enter the name of the Pokémon to search for: ")
            pokemon = collection.find_pokemon(search_name)  # Check if Pokémon exists in the collection
            if pokemon:
                types = ', '.join(pokemon["types"])  # Join types for display
                abilities = ', '.join(pokemon["abilities"])  # Join abilities for display
                print(Fore.LIGHTYELLOW_EX + f"Found Pokémon: Name: {pokemon['name']}, Types: {types}, Abilities: {abilities}" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"{search_name} is not found in your collection." + Style.RESET_ALL)

        elif choice == "4":
            loading_effect()  # Simulate loading for 1 second
            show_random_fact()  # Show a random Pokémon fact
     
        elif choice == "5":
            print_notification("Goodbye! Thanks for visiting the Pokémon Collection!")
            running = False  # Flag to exit the loop
        else:
            print_notification("Invalid choice. Please try again.", Fore.RED)

        input("\nPress Enter to continue...")  # Pause before clearing the screen again


if __name__ == "__main__":
    main()  # Start the program