
#testing
from Load_tax_data import *
m_inst = Load_tax_data("tax_november.csv")
def dupe_check():
	resp = m_inst.execute_query("SELECT ID, ZIP, STATE FROM tax_rates ORDER BY ZIP")
	dupe_lst = []
	old_temp = ''
	for i in range(0, len(resp)):
		temp = resp[i]
		#now only adds if the states are the same
		#if old_temp and temp[1] == old_temp[1] and temp[2] == old_temp[2]: dupe_lst.append(resp[i])
		if old_temp and temp[1] == old_temp[1]: dupe_lst.append([old_temp, resp[i]])
		old_temp = temp
	return dupe_lst




