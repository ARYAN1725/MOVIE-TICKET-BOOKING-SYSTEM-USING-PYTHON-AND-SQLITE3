import sqlite3

# ✅ Use raw string (r"") or forward slashes ("/") to avoid escape sequence issues
DATABASE_PATH = r"C:\Users\Lenovo\OneDrive\Documents\PYTHON BY CHATGPT\MOVIE TICKET BOOKING\movies.db"

# Function to connect to the database and create necessary tables
def connect_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Creating the movies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            duration INTEGER NOT NULL,
            genre TEXT NOT NULL
        )
    ''')

    # Creating the bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,  
            customer_name TEXT NOT NULL,
            seat_number INTEGER NOT NULL,
            UNIQUE(movie_id, seat_number),  -- Prevent duplicate seat bookings
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

# Function to add a new movie
def add_movie(title, duration, genre):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Prevent adding duplicate movies
    cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
    existing_movie = cursor.fetchone()
    if existing_movie:
        print(f"Movie '{title}' already exists.")
    else:
        cursor.execute("INSERT INTO movies (title, duration, genre) VALUES (?, ?, ?)", (title, duration, genre))
        conn.commit()
        print(f"Movie '{title}' added successfully!")

    conn.close()

# Function to view all movies
def view_movies():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    conn.close()

    if movies:
        print("\nMovies List:")
        for movie in movies:
            print(f"ID: {movie[0]}, Title: {movie[1]}, Duration: {movie[2]} min, Genre: {movie[3]}")
    else:
        print("No movies found.")

# Function to add a booking
def add_booking(movie_id, customer_name, seat_number):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Check if the movie exists
    cursor.execute("SELECT title FROM movies WHERE movie_id = ?", (movie_id,))
    movie = cursor.fetchone()

    if movie:
        try:
            # Check if the seat is already booked
            cursor.execute("SELECT * FROM bookings WHERE movie_id = ? AND seat_number = ?", (movie_id, seat_number))
            if cursor.fetchone():
                print(f"Error: Seat {seat_number} is already booked for '{movie[0]}'.")
            else:
                cursor.execute("INSERT INTO bookings (movie_id, customer_name, seat_number) VALUES (?, ?, ?)", 
                               (movie_id, customer_name, seat_number))
                conn.commit()
                print(f"Seat number {seat_number} booked successfully for '{movie[0]}'!")
        except sqlite3.IntegrityError:
            print(f"Error: Could not book seat {seat_number}.")
    else:
        print(f"Error: Movie with ID {movie_id} does not exist.")

    conn.close()

# Function to view all bookings with movie details
def view_bookings():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bookings.booking_id, movies.title, bookings.customer_name, bookings.seat_number
        FROM bookings
        JOIN movies ON bookings.movie_id = movies.movie_id
        ORDER BY movies.title, bookings.seat_number
    """)
    
    bookings = cursor.fetchall()
    conn.close()

    if bookings:
        print("\nBooked Seats:")
        for booking in bookings:
            print(f"Booking ID: {booking[0]}, Movie: {booking[1]}, Customer: {booking[2]}, Seat: {booking[3]}")
    else:
        print("No bookings found.")

# Main function to interact with the user
def main():
    connect_db()  # Ensure tables are created before using them
    
    while True:
        print("\n1. Add Movie")
        print("2. View Movies")
        print("3. Book a Movie Ticket")
        print("4. View Bookings")
        print("5. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            title = input("Enter movie title: ")
            try:
                duration = int(input("Enter movie duration (in minutes): "))
            except ValueError:
                print("Invalid input. Duration should be a number.")
                continue
            genre = input("Enter movie genre: ")
            add_movie(title, duration, genre)

        elif choice == "2":
            view_movies()

        elif choice == "3":
            view_movies()  # Show available movies before booking
            try:
                movie_id = int(input("\nEnter the Movie ID to book: "))
                customer_name = input("Enter your name: ")
                seat_number = int(input("Enter the seat number: "))
                add_booking(movie_id, customer_name, seat_number)
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

        elif choice == "4":
            view_bookings()
            
        elif choice == "5":
            print("Exiting... Thank you for using the system!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
