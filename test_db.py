
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Alancrzs@09",
        database="warrantyvault"
    )

    if conn.is_connected():
        print("WarrantyVault database connected successfully!")

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")

        print("\nTables in WarrantyVault:")
        for table in cursor.fetchall():
            print(table[0])

        cursor.close()
        conn.close()

except mysql.connector.Error as error:
    print("Database connection failed!")
    print(error)
