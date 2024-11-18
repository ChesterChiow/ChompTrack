import mysql.connector
from server.DatabaseCtrl.credentials import SQL_CREDENTIALS



class DatabaseQueries:
    def __init__(self):
        # Initialize the connection
        self.connection = mysql.connector.connect(
            host=SQL_CREDENTIALS.get('host'),
            user=SQL_CREDENTIALS.get('user'),
            password=SQL_CREDENTIALS.get('password'),
            database=SQL_CREDENTIALS.get('database'),
            port=SQL_CREDENTIALS.get('port')
        )
        # Create the cursor
        self.cursor = self.connection.cursor()

    def close_connection(self):
        # Close cursor and connection
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed")


if __name__ == '__main__':
    db = DatabaseQueries()
    print("worked")
    db.close_connection()