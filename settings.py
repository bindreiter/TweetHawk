
import MySQLdb
def connection():
	db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     db="tweethawk")   
	return db
