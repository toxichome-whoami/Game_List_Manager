import os
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class GameDatabaseManager:
    def __init__(self, filename="game_list.txt"):
        self.filename = filename
        self.database = self.load_database()

    def load_database(self):
        """Load existing database from file, or return an empty list if file doesn't exist."""
        try:
            with open(self.filename, "r") as file:
                return [self._parse_database_entry(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            return []
        except Exception as e:
            print(Fore.RED + f"An error occurred while loading the database: {e}")
            return []

    def save_database(self):
        """Save the current database to the file."""
        with open(self.filename, "w") as file:
            file.write("\n".join([self._format_database_entry(entry) for entry in self.database]))

    def display_database(self):
        """Display the current database in a formatted manner."""
        if not self.database:
            print(Fore.RED + "\nDatabase is empty.\n")
            return
        print(Fore.CYAN + "\n **Game Database** ")
        print(Fore.YELLOW + " Row -> Game Name -> APP ID")
        print(Fore.YELLOW + "-----------------------------------")
        for index, entry in enumerate(self.database, start=1):
            print(Fore.GREEN + f"{index}. {self._format_database_entry(entry)}")
        print()

    def update_info(self):
        """Update an existing game's information in the database."""
        while True:
            self.display_database()
            row_number = input(
                Fore.CYAN
                + "Enter the row number to update (or 'm' for main menu, 'r' to refresh): "
            )
            if row_number.lower() == "m":
                return
            elif row_number.lower() == "r":
                continue
            try:
                row_number = int(row_number)
                if row_number < 1 or row_number > len(self.database):
                    print(Fore.RED + "Invalid row number. Please try again.")
                    continue
                break
            except ValueError:
                print(
                    Fore.RED
                    + "Invalid input. Please enter a number, 'm' for main menu, or 'r' to refresh."
                )

        # Extract current game info
        game_name, app_id = self.database[row_number - 1]

        print(Fore.YELLOW + f"Current Game Name: {game_name}, Current APP ID: {app_id}")

        new_game_name = input(
            Fore.CYAN + "Enter new game name (press Enter to keep current): "
        )
        new_app_id = input(
            Fore.CYAN + "Enter new APP ID (press Enter to keep current): "
        )

        if new_game_name:
            if any(game[0] == new_game_name for game in self.database):
                print(Fore.RED + "\nError: Game name already exists. Please try again.")
                return

        if new_app_id:
            if any(game[1] == new_app_id for game in self.database):
                print(Fore.RED + "\nError: APP ID already exists. Please try again.")
                return

        new_game_name = new_game_name if new_game_name else game_name
        new_app_id = new_app_id if new_app_id else app_id

        self.database[row_number - 1] = (new_game_name, new_app_id)
        self.save_database()
        print(Fore.GREEN + "Update successful.")
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

            app_id = input(Fore.CYAN + "Enter the APP ID of the new game (or 'm' for main menu): ").strip()
            if app_id.lower() == 'm':
                return
            if not app_id:
                print(Fore.RED + "\nError: APP ID is required. Please try again.")
                continue

            if any(game[0] == game_name for game in self.database):
                print(Fore.RED + "\nError: Game name already exists. Please try again.")
                continue

            if any(game[1] == app_id for game in self.database):
                print(Fore.RED + "\nError: APP ID already exists. Please try again.")
                continue

            new_entry = (game_name, app_id)
            self.database.append(new_entry)
            self.save_database()
            print(Fore.GREEN + "Game added successfully.")
            self.display_database()
            self._prompt_again("Add another game?", self.add_new_game)
            break

    def remove_game(self):
        """Remove a game from the database."""
        while True:
            self.display_database()
            row_number = input(
                Fore.CYAN
                + "Enter the row number to remove (or 'm' for main menu, 'r' to refresh): "
            )
            if row_number.lower() == "m":
                return
            elif row_number.lower() == "r":
                continue
            try:
                row_number = int(row_number)
                if row_number < 1 or row_number > len(self.database):
                    print(Fore.RED + "Invalid row number. Please try again.")
                    continue
                break
            except ValueError:
                print(
                    Fore.RED
                    + "Invalid input. Please enter a number, 'm' for main menu, or 'r' to refresh."
                )

        # Extract game info to confirm removal
        game_name, app_id = self.database[row_number - 1]

        confirm_removal = input(
            Fore.YELLOW
            + f"Confirm removal of '{game_name}' (APP ID: {app_id})? (y/n): "
        ).lower()
        if confirm_removal == "y":
            del self.database[row_number - 1]
            self.save_database()
            print(Fore.GREEN + "Game removed successfully.")
            self.display_database()  # Show updated database
            self._prompt_again("Remove another game?", self.remove_game)
        else:
            print(Fore.RED + "Removal cancelled.")
            self.display_database()  # Show original database
            self._prompt_again("Remove another game?", self.remove_game)

    def _parse_database_entry(self, entry):
        """Parse a database entry from a string into a tuple (game_name, app_id)."""
        parts = entry.split(" -> ")
        return parts[0].strip(), parts[1].strip()

    def _format_database_entry(self, entry):
        """Format a database entry tuple (game_name, app_id) into a string."""
        return f"{entry[0]} -> {entry[1]}"

    def _prompt_again(self, prompt, action):
        """Prompt user if they want to perform the action again."""
        choice = input(Fore.CYAN + f"{prompt} (y/n): ").lower()
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
        choice = input(Fore.CYAN + "Choose an option: ")

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
