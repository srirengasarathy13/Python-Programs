import mysql.connector

print("Testing MySQL connection...")

try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        use_pure=True,
        connection_timeout=5
    )

    if db.is_connected():
        print("MySQL connection successful!")

    db.close()

except mysql.connector.Error as e:
    print("MySQL connection failed!")
    print("Error:", e)