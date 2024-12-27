import os
import colorama
from colorama import Fore, Style, Back
import time

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

def get_user_input(prompt, valid_options=None):
    """Prompt user for input and validate against valid options if provided."""
    while True:
        user_input = input(Fore.CYAN + prompt).strip().lower()
        if valid_options and user_input not in valid_options:
            print(Fore.RED + f"Invalid option. Valid options are: {', '.join(valid_options)}")
        else:
            return user_input

class GameDatabaseManager:
    def __init__(self, filename="D:\Python\Git repos\server_free_game_list\game_list.txt"):
        self.filename = filename
        self.database = self.load_database()

    def load_database(self):
        """Load existing database from file, or return an empty list if file doesn't exist."""
        print(Fore.GREEN + "Loading database...", end="")
        time.sleep(1)  # Simulate loading time
        try:
            with open(self.filename, "r") as file:
                database = [self._parse_database_entry(line.strip()) for line in file.readlines()]
                print(Fore.GREEN + " [Done]")
                return database
        except FileNotFoundError:
            print(Fore.GREEN + " [Done]")
            return []
        except Exception as e:
            print(Fore.RED + f"An error occurred while loading the database: {e}")
            return []

    def save_database(self):
        """Save the current database to the file."""
        print(Fore.GREEN + "Saving database...", end="")
        time.sleep(1)  # Simulate saving time
        with open(self.filename, "w") as file:
            file.write("\n".join([self._format_database_entry(entry) for entry in self.database]))
        print(Fore.GREEN + " [Done]")

    def display_database(self):
        """Display the current database in a formatted manner."""
        clear_screen()
        if not self.database:
            print(Fore.RED + "\nDatabase is empty.\n")
            return
        print(Fore.CYAN + "\n" + Back.BLUE + " ** Game Database ** " + Back.RESET)
        print(
            Fore.YELLOW
            + "Row   | Game Name                                           | APP ID"
        )
        print(
            Fore.YELLOW
            + "---------------------------------------------------------------------"
        )
        for index, entry in enumerate(self.database, start=1):
            print(Fore.GREEN + f"{index:<6}| {entry[0]:<51} | {entry[1]}")
        print()

    def update_info(self):
        """Update an existing game's information in the database."""
        while True:
            self.display_database()
            row_number = input(Fore.CYAN + "Enter the row number to update (or 'm' for main menu, 'r' to refresh): ").strip().lower()

            if row_number == "m":
                return
            elif row_number == "r":
                continue
            elif not row_number:
                print(Fore.RED + "Row number cannot be empty. Please enter a valid row number.")
                continue

            try:
                row_number = int(row_number)
                if row_number < 1 or row_number > len(self.database):
                    print(Fore.RED + "Invalid row number. Please try again.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number, 'm' for main menu, or 'r' to refresh.")

        # Extract current game info
        game_name, app_id = self.database[row_number - 1]

        print(Fore.YELLOW + f"Current Game Name: {game_name}, Current APP ID: {app_id}")

        while True:
            new_game_name = input(Fore.CYAN + "Enter new game name (press Enter to keep current): ").strip()
            if new_game_name and any(game[0] == new_game_name for game in self.database):
                print(Fore.RED + "\nError: Game name already exists. Please try again.")
                continue
            break

        while True:
            new_app_id = input(Fore.CYAN + "Enter new APP ID (must be an integer, press Enter to keep current): ").strip()
            if new_app_id:
                try:
                    new_app_id = int(new_app_id)
                    if any(game[1] == new_app_id for game in self.database):
                        print(Fore.RED + "\nError: APP ID already exists. Please try again.")
                        continue
                    break
                except ValueError:
                    print(Fore.RED + "Invalid APP ID. It must be an integer. Please try again.")
            else:
                break

        new_game_name = new_game_name if new_game_name else game_name
        new_app_id = new_app_id if new_app_id else app_id

        confirm = get_user_input(Fore.YELLOW + f"Confirm update to '{new_game_name}' with APP ID '{new_app_id}'? (y/n): ", valid_options=['y', 'n'])
        if confirm == 'y':
            self.database[row_number - 1] = (new_game_name, new_app_id)
            self.save_database()
            print(Fore.GREEN + "Update successful.")
        else:
            print(Fore.RED + "Update cancelled.")

        self.display_database()  # Show updated database

    def add_new_game(self):
        """Add a new game to the database."""
        while True:
            game_name = input(Fore.CYAN + "Enter the name of the new game (or 'm' for main menu): ").strip()
            if game_name.lower() == 'm':
                return
            if not game_name:
                print(Fore.RED + "\nError: Game name is required. Please try again.")
                continue

            while True:
                app_id = input(Fore.CYAN + "Enter the APP ID of the new game (must be an integer, or 'm' for main menu): ").strip()
                if app_id.lower() == 'm':
                    return
                if not app_id:
                    print(Fore.RED + "\nError: APP ID is required. Please try again.")
                    continue
                try:
                    app_id = int(app_id)
                    break
                except ValueError:
                    print(Fore.RED + "Invalid APP ID. It must be an integer. Please try again.")

            if any(game[0] == game_name for game in self.database):
                print(Fore.RED + "\nError: Game name already exists. Please try again.")
                continue

            if any(game[1] == app_id for game in self.database):
                print(Fore.RED + "\nError: APP ID already exists. Please try again.")
                continue

            new_entry = (game_name, app_id)
            confirm = get_user_input(Fore.YELLOW + f"Confirm adding '{game_name}' with APP ID '{app_id}'? (y/n): ", valid_options=['y', 'n'])
            if confirm == 'y':
                self.database.append(new_entry)
                self.save_database()
                print(Fore.GREEN + "Game added successfully.")
                self.display_database()
                self._prompt_again("Add another game?", self.add_new_game)
                break
            else:
                print(Fore.RED + "Addition cancelled.")
                return

    def remove_game(self):
        """Remove a game from the database."""
        while True:
            self.display_database()
            row_number = input(Fore.CYAN + "Enter the row number to remove (or 'm' for main menu, 'r' to refresh): ").strip().lower()
            if row_number == "m":
                return
            elif row_number == "r":
                continue
            elif not row_number:
                print(Fore.RED + "Row number cannot be empty. Please enter a valid row number.")
                continue

            try:
                row_number = int(row_number)
                if row_number < 1 or row_number > len(self.database):
                    print(Fore.RED + "Invalid row number. Please try again.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number, 'm' for main menu, or 'r' to refresh.")

        # Extract game info to confirm removal
        game_name, app_id = self.database[row_number - 1]

        confirm_removal = get_user_input(Fore.YELLOW + f"Confirm removal of '{game_name}' (APP ID: {app_id})? (y/n): ", valid_options=['y', 'n'])
        if confirm_removal == "y":
            del self.database[row_number - 1]
            self.save_database()
            print(Fore.GREEN + "Game removed successfully.")
        else:
            print(Fore.RED + "Removal cancelled.")

        self.display_database()  # Show updated database

    def _parse_database_entry(self, entry):
        """Parse a database entry from a string into a tuple (game_name, app_id)."""
        parts = entry.split(" -> ")
        return parts[0].strip(), int(parts[1].strip())

    def _format_database_entry(self, entry):
        """Format a database entry tuple (game_name, app_id) into a string."""
        return f"{entry[0]} -> {entry[1]}"

    def _prompt_again(self, prompt, action):
        """Prompt user if they want to perform the action again."""
        choice = get_user_input(Fore.CYAN + f"{prompt} (y/n): ", valid_options=['y', 'n'])
        if choice == "y":
            action()

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def main():
    clear_screen()
    manager = GameDatabaseManager()

    while True:
        clear_screen()
        print(Fore.CYAN + "\n--- **Game List Manager** ---")
        print(Fore.YELLOW + "1. Display Database")
        print(Fore.YELLOW + "2. Add New Game")
        print(Fore.YELLOW + "3. Update Game Info")
        print(Fore.YELLOW + "4. Remove Game")
        print(Fore.YELLOW + "5. Quit")
        choice = get_user_input(Fore.CYAN + "Choose an option: ", valid_options=['1', '2', '3', '4', '5'])

        if choice == "1":
            clear_screen()
            manager.display_database()
            input(Fore.CYAN + "Press Enter to continue...")
        elif choice == "2":
            manager.add_new_game()
        elif choice == "3":
            manager.update_info()
        elif choice == "4":
            manager.remove_game()
        elif choice == "5":
            clear_screen()
            print(Fore.GREEN + "Goodbye!")
            break
        else:
            clear_screen()
            print(Fore.RED + "Invalid choice. Please choose a valid option.")
            input(Fore.CYAN + "Press Enter to continue...")

if __name__ == "__main__":
    main()

# Made by Toxic Home...