import os

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

    def save_database(self):
        """Save the current database to the file."""
        with open(self.filename, "w") as file:
            file.write("\n".join([self._format_database_entry(entry) for entry in self.database]))

    def display_database(self):
        """Display the current database in a formatted manner."""
        if not self.database:
            print("Database is empty.")
            return
        print(" **Game Database** ")
        print(" Row -> Game Name -> APP ID")
        print("-----------------------------------")
        for index, entry in enumerate(self.database, start=1):
            print(f"{index}. {self._format_database_entry(entry)}")

    def update_info(self):
        """Update an existing game's information in the database."""
        self.display_database()
        while True:
            row_number = input(
                "Enter the row number to update (or 'c' to cancel, 'r' to refresh): "
            )
            if row_number.lower() == "c":
                return
            elif row_number.lower() == "r":
                self.display_database()
                continue
            try:
                row_number = int(row_number)
                if row_number < 1 or row_number > len(self.database):
                    print("Invalid row number. Please try again.")
                    continue
                break
            except ValueError:
                print(
                    "Invalid input. Please enter a number, 'c' to cancel, or 'r' to refresh."
                )

        # Extract current game info
        game_name, app_id = self.database[row_number - 1]

        print(f"Current Game Name: {game_name}, Current APP ID: {app_id}")

        new_game_name = input("Enter new game name (press Enter to keep current): ")
        new_app_id = input("Enter new APP ID (press Enter to keep current): ")

        new_game_name = new_game_name if new_game_name else game_name
        new_app_id = new_app_id if new_app_id else app_id

        self.database[row_number - 1] = (new_game_name, new_app_id)
        self.save_database()
        print("Update successful.")
        self.display_database()  # Show updated database
        self._prompt_again("Update another game?", self.update_info)

    def add_new_game(self):
        """Add a new game to the database."""
        while True:
            game_name = input("Enter the name of the new game: ")
            app_id = input("Enter the APP ID of the new game: ")
            
            # Input validation
            if not game_name.strip() or not app_id.strip():
                print("\nError: Both Game Name and APP ID are required. Please try again.")
                continue
            
            new_entry = (game_name, app_id)
            self.database.append(new_entry)
            self.save_database()
            print("Game added successfully.")
            self.display_database()  # Show updated database
            self._prompt_again("Add another game?", self.add_new_game)
            break

    def remove_game(self):
        """Remove a game from the database."""
        self.display_database()
        while True:
            row_number = input(
                "Enter the row number to remove (or 'c' to cancel, 'r' to refresh): "
            )
            if row_number.lower() == "c":
                return
            elif row_number.lower() == "r":
                self.display_database()
                continue
            try:
                row_number = int(row_number)
                if row_number < 1 or row_number > len(self.database):
                    print("Invalid row number. Please try again.")
                    continue
                break
            except ValueError:
                print(
                    "Invalid input. Please enter a number, 'c' to cancel, or 'r' to refresh."
                )

        # Extract game info to confirm removal
        game_name, app_id = self.database[row_number - 1]

        confirm_removal = input(
            f"Confirm removal of '{game_name}' (APP ID: {app_id})? (y/n): "
        ).lower()
        if confirm_removal == "y":
            del self.database[row_number - 1]
            self.save_database()
            print("Game removed successfully.")
            self.display_database()  # Show updated database
            self._prompt_again("Remove another game?", self.remove_game)
        else:
            print("Removal cancelled.")
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
        choice = input(f"{prompt} (y/n): ").lower()
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
        print("\n--- **Game List Manager** ---")
        print("1. Display Database")
        print("2. Add New Game")
        print("3. Update Game Info")
        print("4. Remove Game")
        print("5. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            clear_screen()
            manager.display_database()
            input("Press Enter to continue...")
        elif choice == "2":
            manager.add_new_game()
        elif choice == "3":
            manager.update_info()
        elif choice == "4":
            manager.remove_game()
        elif choice == "5":
            clear_screen()
            print("Goodbye!")
            break
        else:
            clear_screen()
            print("Invalid choice. Please choose a valid option.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()

           
