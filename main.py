import sqlite3

# Database file
DB_FILE = "quiz_app.db"


# Initialize the database
def initialize_db():
    """Create database tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Questions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_option INTEGER NOT NULL
    )
    """)

    # Scores table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()


# Add sample questions
def add_sample_questions():
    """Add initial sample questions to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM questions")
    if cursor.fetchone()[0] == 0:  # Add questions if the table is empty
        sample_questions = [
            # Python questions
            ("Python", "What is the output of `print(2 ** 3)`?", "6", "8", "9", "10", 2),
            ("Python", "Which keyword is used to define a function in Python?", "func", "define", "def", "lambda", 3),
            ("Python", "What is the default data type for numbers in Python?", "int", "float", "complex", "str", 1),
            ("Python", "Which library is used for data visualization in Python?", "numpy", "matplotlib", "pandas", "os",
             2),
            ("Python", "How do you declare a string in Python?", "'hello'", "hello", "String hello", "None of these", 1),

            # DSA questions
            ("DSA", "What is the time complexity of binary search?", "O(n)", "O(log n)", "O(n^2)", "O(1)", 2),
            ("DSA", "Which data structure is used in BFS?", "Stack", "Queue", "Deque", "Priority Queue", 2),
            ("DSA", "What is the worst-case time complexity of merge sort?", "O(n)", "O(log n)", "O(n^2)", "O(n log n)",
             4),
            ("DSA", "Which algorithm is used to find the shortest path in a graph?", "Dijkstra's", "Kruskal's", "Prim's","DFS", 1),
            ("DSA", "Which traversal technique visits the left subtree first?", "Inorder", "Preorder", "Postorder",
             "Breadth-First", 1),

            # DBMS questions
            ("DBMS", "Which SQL clause is used to filter rows?", "WHERE", "GROUP BY", "ORDER BY", "HAVING", 1),
            ("DBMS", "Which normal form removes transitive dependency?", "1NF", "2NF", "3NF", "BCNF", 3),
            ("DBMS", "What is the purpose of a transaction log?", "Backup data", "Ensure atomicity",
             "Maintain user access", "Optimize query", 2),
            ("DBMS", "What is the main advantage of a clustered index?", "Faster retrieval", "Easier joins",
             "Reduces duplicates", "None of the above", 1),
            ("DBMS", "Which of the following is a NoSQL database?", "MySQL", "PostgreSQL", "MongoDB", "Oracle", 3),
        ]
        cursor.executemany("""
        INSERT INTO questions (subject, question, option1, option2, option3, option4, correct_option)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_questions)

    conn.commit()
    conn.close()


# User registration and login
def register_user():
    """Register a new user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("\n--- Registration ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Try logging in.")
    finally:
        conn.close()


def login_user():
    """Log in an existing user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("\n--- Login ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login successful!")
        return user[0]  # Return user ID
    else:
        print("Invalid username or password.")
        return None


# Quiz functionality
def get_questions(subject):
    """Retrieve questions for a specific subject."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, question, option1, option2, option3, option4, correct_option FROM questions WHERE subject = ?",
        (subject,))
    questions = cursor.fetchall()
    conn.close()
    return questions


def attempt_quiz(user_id, subject):
    """Allow the user to attempt a quiz."""
    print(f"\n--- {subject} Quiz ---")
    questions = get_questions(subject)

    if not questions:
        print("No questions available for this subject.")
        return

    score = 0
    for q in questions:
        print(f"\n{q[1]}")
        print(f"1. {q[2]}  2. {q[3]}  3. {q[4]}  4. {q[5]}")
        answer = input("Your answer (1-4): ").strip()
        if answer.isdigit() and int(answer) == q[6]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was option {q[6]}.")

    print(f"\nYou scored {score}/{len(questions)}.")
    save_score(user_id, subject, score)


def save_score(user_id, subject, score):
    """Save the user's score."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO scores (user_id, subject, score) VALUES (?, ?, ?)", (user_id, subject, score))
    conn.commit()
    conn.close()


def show_results():
    """Display quiz results."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.username, s.subject, s.score
    FROM scores s
    JOIN users u ON s.user_id = u.id
    """)
    results = cursor.fetchall()
    conn.close()

    print("\n--- Quiz Results ---")
    for username, subject, score in results:
        print(f"{username} scored {score} in {subject} quiz.")


# Main menu
def display_menu():
    """Display the main menu."""
    print("\n--- Quiz App ---")
    print("1. Register")
    print("2. Login")
    print("3. Attempt Quiz")
    print("   a. DSA")
    print("   b. DBMS")
    print("   c. Python")
    print("4. Show Results")
    print("5. Exit")


def main():
    """Main function to run the quiz app."""
    initialize_db()
    add_sample_questions()

    current_user = None

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            current_user = login_user()
        elif choice == "3":
            if not current_user:
                print("Please login first.")
                continue

            print("\nChoose a quiz:")
            print("a. DSA")
            print("b. DBMS")
            print("c. Python")
            subject_choice = input("Enter your choice (a/b/c): ").strip().lower()

            subject_map = {"a": "DSA", "b": "DBMS", "c": "Python"}
            subject = subject_map.get(subject_choice)
            if subject:
                attempt_quiz(current_user, subject)
            else:
                print("Invalid choice.")
        elif choice == "4":
            show_results()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
