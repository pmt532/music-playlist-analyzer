import csv
import matplotlib.pyplot as plt


class Song:
    """
    Represents one song in the playlist.
    """

    def __init__(self, title, artist, genre, duration, play_count):
        self.title = title.strip()
        self.artist = artist.strip()
        self.genre = genre.strip()
        self.duration = int(duration)
        self.play_count = int(play_count)

    def to_dict(self):
        """
        Convert the song object into a dictionary for CSV writing.
        """
        return {
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'duration': self.duration,
            'play_count': self.play_count
        }


def load_data(filename):
    """
    Load song data from a CSV file and return a list of Song objects.
    """
    songs = []

    try:
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)

            required_fields = ['title', 'artist', 'genre', 'duration', 'play_count']
            if reader.fieldnames is None:
                print("Error: The CSV file is empty or invalid.")
                return songs

            for field in required_fields:
                if field not in reader.fieldnames:
                    print(f"Error: Missing required column '{field}' in the CSV file.")
                    return songs

            for row_number, row in enumerate(reader, start=2):
                try:
                    song = Song(
                        row['title'],
                        row['artist'],
                        row['genre'],
                        row['duration'],
                        row['play_count']
                    )
                    songs.append(song)
                except ValueError:
                    print(f"Warning: Invalid numeric data in row {row_number}. Row skipped.")
                except KeyError:
                    print(f"Warning: Missing data in row {row_number}. Row skipped.")

    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: Permission denied when opening the file.")
    except Exception as error:
        print(f"Unexpected error while loading data: {error}")

    return songs


def save_data(filename, songs):
    """
    Save all songs back to the CSV file.
    """
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['title', 'artist', 'genre', 'duration', 'play_count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for song in songs:
                writer.writerow(song.to_dict())

        print("Playlist data saved successfully.")

    except PermissionError:
        print("Error: Permission denied. Could not save the file.")
    except Exception as error:
        print(f"Unexpected error while saving data: {error}")


def format_duration(seconds):
    """
    Convert seconds into minutes and seconds.
    Example: 203 -> 3m 23s
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds}s"


def display_songs(songs):
    """
    Display all songs in a clear table-like format.
    """
    if len(songs) == 0:
        print("No songs available.")
        return

    print("\n" + "-" * 90)
    print(f"{'No.':<5}{'Title':<25}{'Artist':<20}{'Genre':<15}{'Duration':<12}{'Plays':<8}")
    print("-" * 90)

    for index, song in enumerate(songs, start=1):
        print(
            f"{index:<5}"
            f"{song.title[:23]:<25}"
            f"{song.artist[:18]:<20}"
            f"{song.genre[:13]:<15}"
            f"{format_duration(song.duration):<12}"
            f"{song.play_count:<8}"
        )

    print("-" * 90)


def get_non_empty_text(prompt):
    """
    Keep asking until the user enters non-empty text.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_positive_integer(prompt):
    """
    Keep asking until the user enters a valid non-negative integer.
    """
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
            if number < 0:
                print("Please enter a number that is 0 or more.")
            else:
                return number
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def search_songs(songs):
    """
    Search songs by title, artist, or genre.
    """
    if len(songs) == 0:
        print("No songs available.")
        return

    print("\nSearch by:")
    print("1. Title")
    print("2. Artist")
    print("3. Genre")

    choice = input("Choose search type: ").strip()

    if choice not in ["1", "2", "3"]:
        print("Invalid search choice.")
        return

    keyword = input("Enter search keyword: ").strip().lower()

    if keyword == "":
        print("Search keyword cannot be empty.")
        return

    results = []

    for song in songs:
        if choice == "1" and keyword in song.title.lower():
            results.append(song)
        elif choice == "2" and keyword in song.artist.lower():
            results.append(song)
        elif choice == "3" and keyword in song.genre.lower():
            results.append(song)

    if len(results) == 0:
        print("No matching songs were found.")
    else:
        print(f"\nFound {len(results)} matching song(s):")
        display_songs(results)


def sort_songs(songs):
    """
    Sort songs by title, duration, or play count.
    """
    if len(songs) == 0:
        print("No songs available.")
        return

    print("\nSort by:")
    print("1. Title (A-Z)")
    print("2. Duration (shortest to longest)")
    print("3. Play count (highest to lowest)")

    choice = input("Choose sort type: ").strip()

    if choice == "1":
        sorted_songs = sorted(songs, key=lambda song: song.title.lower())
        print("\nSongs sorted by title:")
        display_songs(sorted_songs)

    elif choice == "2":
        sorted_songs = sorted(songs, key=lambda song: song.duration)
        print("\nSongs sorted by duration:")
        display_songs(sorted_songs)

    elif choice == "3":
        sorted_songs = sorted(songs, key=lambda song: song.play_count, reverse=True)
        print("\nSongs sorted by play count:")
        display_songs(sorted_songs)

    else:
        print("Invalid sort choice.")


def calculate_genre_count(songs):
    """
    Count how many songs belong to each genre.
    """
    genre_count = {}

    for song in songs:
        if song.genre in genre_count:
            genre_count[song.genre] += 1
        else:
            genre_count[song.genre] = 1

    return genre_count


def show_statistics(songs):
    """
    Show playlist statistics such as total songs,
    most played song, average duration, and most common genre.
    """
    if len(songs) == 0:
        print("No data available.")
        return

    total_songs = len(songs)
    most_played = max(songs, key=lambda song: song.play_count)
    total_duration = sum(song.duration for song in songs)
    average_duration = total_duration / total_songs
    total_plays = sum(song.play_count for song in songs)

    genre_count = calculate_genre_count(songs)
    most_common_genre = max(genre_count, key=genre_count.get)

   print("\n--- Playlist Statistics Summary ---")
    print(f"Total number of songs: {total_songs}")
    print(f"Most played song: {most_played.title} by {most_played.artist} ({most_played.play_count} plays)")
    print(f"Average duration: {average_duration:.2f} seconds ({format_duration(int(average_duration))})")
    print(f"Most common genre: {most_common_genre}")
    print(f"Total play count: {total_plays}")


def show_chart(songs):
    """
    Display a bar chart of genre distribution.
    """
    if len(songs) == 0:
        print("No data available.")
        return

    genre_count = calculate_genre_count(songs)

    genres = list(genre_count.keys())
    counts = list(genre_count.values())

    plt.figure(figsize=(8, 5))
    plt.bar(genres, counts)
    plt.title("Genre Distribution")
    plt.xlabel("Genre")
    plt.ylabel("Number of Songs")
    plt.tight_layout()
    plt.show()


def add_song(songs):
    """
    Add a new song to the playlist with input validation.
    """
    print("\nEnter new song details:")

    title = get_non_empty_text("Title: ")
    artist = get_non_empty_text("Artist: ")
    genre = get_non_empty_text("Genre: ")
    duration = get_positive_integer("Duration (seconds): ")
    play_count = get_positive_integer("Play count: ")

    new_song = Song(title, artist, genre, duration, play_count)
    songs.append(new_song)

    print(f"Song '{title}' was added successfully.")


def main():
    """
    Main menu for the Music Playlist Analyzer program.
    """
    filename = "songs.csv"
    songs = load_data(filename)

    while True:
        print("\n--- Music Playlist Analyzer ---")
        print("1. Show all songs")
        print("2. Search for songs")
       print("3. Sort playlist")
        print("4. Show statistics")
        print("5. Show genre chart")
        print("6. Add new song")
        print("7. Save and Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_songs(songs)

        elif choice == "2":
            search_songs(songs)

        elif choice == "3":
            sort_songs(songs)

        elif choice == "4":
            show_statistics(songs)

        elif choice == "5":
            show_chart(songs)

        elif choice == "6":
            add_song(songs)

        elif choice == "7":
            save_data(filename, songs)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
