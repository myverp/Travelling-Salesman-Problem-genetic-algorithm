import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="04082005",
        database="genetic_algorithm"
    )
    return connection

def insert_result(solution, distance):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO results (solution, distance) VALUES (%s, %s)", (str(solution), distance))
    connection.commit()
    cursor.close()
    connection.close()

def fetch_all_results():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM results")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
