
import requests, sqlite3

class Tax_conn:
	def __init__(self):
		self.dbase= 'tax_rates.db'
		self.table = 'tax_rates'
		self._conn = sqlite3.connect(self.dbase)
		self.cursor = self._conn.cursor()
	def execute_query(self, comm):
		#testing only
		#should not be in final version of class
		if comm.split(' ')[0].upper() in ["CREATE", "INSERT", "DELETE", "UPDATE"]: raise RuntimeError("Not a query")
		self.cursor.execute(comm)
		data = self.cursor.fetchall()
		return data
