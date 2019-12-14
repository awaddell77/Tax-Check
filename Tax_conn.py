
import requests, sqlite3

class Tax_conn:
	def __init__(self):
		self.dbase= 'tax_rates.db'
		self.table = 'tax_rates'
		self._conn = sqlite3.connect(self.dbase)
		#using dict instead of list because we need 1-1 (0) to map to december 
		self._months = {1:"january", 2:"february", 3:"march", 4:"april", 5:"may", 6:"june", 7:"july", 8:"august", 9:"september", 10:"october", 11:"november", 12:"december", 0:"december"}
		self.cursor = self._conn.cursor()
	def execute_query(self, comm):
		#testing only
		#should not be in final version of class
		if comm.split(' ')[0].upper() in ["CREATE", "INSERT", "DELETE", "UPDATE"]: raise RuntimeError("Not a query")
		self.cursor.execute(comm)
		data = self.cursor.fetchall()
		return data
