import psycopg

connection = psycopg.connect("dbname=farming_market_db user=postgres password=MarSul23")

print("Connection successful", connection)
connection.close()
