from dictionarify import *
from Tax_conn import *

class Tax_check(Tax_conn):
	def __init__(self, fname):
		super().__init__()
		self.fname = fname
		self._data = dictionarify(fname)


	def main(self):
		pass
	def check_tax_data(self):
		change_lst = []
		for i in range(0, len(self._data)):
			query = "SELECT RATE, ID FROM {0} ".format(self.table)
			self.cursor.execute(query+" WHERE ZIP = ? AND STATE = ?", (self._data[i]["Destination Zip"], self._data[i]["Destination State"]))
			resp = self.cursor.fetchall()
			if not resp: raise RuntimeError("Could not find record")
			elif len(resp) > 1: raise RuntimeError("Duplicates discovered for {0} and {1}".format(self._data["Destination Zip"], self._data["Destination State"]))
			else:
				#sqlite3 cursor returns floats as floats in python whereas dictionarify leaves them as str
				#so a converison is in order 
				if resp[0][0] != float(self._data[i]["Combined Rate"]): change_lst.append([self._data[i]["Destination Zip"], self._data[i]["Destination State"], resp[0][1]])
		return change_lst



m_inst = Tax_check("tax_november_changes.csv")
ch_lst = m_inst.check_tax_data()

