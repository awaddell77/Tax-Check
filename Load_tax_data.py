import requests, sqlite3
from dictionarify import *

class Load_tax_data:
	def __init__(self, fname = ''):

		self.fname = fname
		if fname: self.data = dictionarify(fname)
		else: self.data = ''
		self.dbase= 'tax_rates.db'
		self.table = 'tax_rates'
		self._conn = sqlite3.connect(self.dbase)
		self.cursor = self._conn.cursor()

	def refresh(self):
		#should also be checking fname
		#if fname then it should check against csv contents
		self._load_tax_data()

	def _get_tax_data(self):
		 rdata = requests.get(
		 	"http://cdtfa.ca.gov/dataportal/api/odata/Effective_Sales_Tax_Rates").json()
		 data = rdata['value']
		 return data
	def _table_check(self):
		print("TABLE NAME:", self.table)
		t_query = "SELECT name FROM sqlite_master WHERE type = \"table\" AND name = \"{0}\"".format(self.table)

		self.cursor.execute(t_query)
		if not self.cursor.fetchall():
			t_query = "CREATE TABLE IF NOT EXISTS {0} (TAID INT(10), CITY CHAR(50), STATE CHAR(50), COUNTY CHAR(50), RATE FLOAT(53), ZIP INT(10), MONTH CHAR(9), YEAR INT(10), PRIMARY KEY (CITY, ZIP, MONTH, YEAR)".format(self.table) 
			self.cursor.execute(t_query)
			t_query = ["CREATE INDEX ZipIndex ON {0}(ZIP)".format(self.table), "CREATE INDEX MonthIndex ON {0}(Month)".format(self.table)]#can't do this because of zip duplicates
			for elem in t_query: self.cursor.execute(elem)
			self._conn.commit()
			print("Created table {0}".format(self.table))
		else: print("Did not create table {0}".format(self.table))
		return
	def execute_query(self, comm):
		#testing only
		#should not be in final version of class
		if comm.split(' ')[0].upper() in ["CREATE", "INSERT", "DELETE", "UPDATE"]: raise RuntimeError("Not a query")
		self.cursor.execute(comm)
		data = self.cursor.fetchall()
		return data
	def test(self):
		#self._table_check()
		#data  = self._form_data(["Destination City","Destination State", "Destination County","Combined Rate", "Destination Zip"])
		#return data
		self._load_tax_data()
	def _form_data(self, crits=[]):
		data = []
		for i in range(0, len(self.data)):
			if not crits: temp = data.append(tuple(self.data[i].values()))
			else:
				temp = []
				for i_2 in range(0, len(crits)):
					temp.append(self.data[i][crits[i_2]])
				data.append(tuple(temp))
		return data
	











	def _load_tax_data(self):
		#data = self._get_tax_data()
		self._table_check()

		self.cursor.execute("SELECT COUNT(*) FROM {0}".format(self.table))
		db_data = self.cursor.fetchall()

		#if the table doesn't have any rows it fills it with the data it took from cdtfa
		if not db_data[0][0]:
			data = self._form_data(["Destination City","Destination State", "Destination County","Combined Rate", "Destination Zip"])
			cmd = "INSERT INTO {0} ".format(self.table)
			self.cursor.executemany(cmd + '(CITY, STATE, COUNTY, RATE, ZIP) VALUES (?,?,?,?,?)', (data))
			self._conn.commit()
			'''for i in range(0, len(self.data)):
				
				if self.data[i]["IsIncorporated"] == 'False': inc = 0
				else: inc = 1 
				print("Inserting data now")
				cmd = "INSERT INTO {0} ".format(self.table)
				self.cursor.executemany(cmd + '(CITY, STATE, COUNTY, RATE, ZIP) VALUES (?,?,?,?)', 
					(data[i]["City"], data[i]["County"], data[i]["Rate"], inc ))
				self._conn.commit()'''
		#NEEDS TESTING!!

if __name__ == "__main__":
	m_inst = Load_tax_data("tax_november.csv")
	res = m_inst.test()
#m_inst.refresh()