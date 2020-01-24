import time
from Eclipse_client import Eclipse_client
from dictionarify import *

class Tax_client(Eclipse_client):
	def __init__(self, fname):
		super().__init__()
		self.data = dictionarify(fname)
		self._fname = fname
	def req_report(self):
		results = []
		start = time.time()
		for i in range(0, len(self.data)):
			#print("Attempt #{0} [{1}, {2}]".format(i+1, self.data[i]["Destination Zip"], self.data[i]["Destination State"]))
			print("Attempt #{0} of {1}".format(i+1, len(self.data)) + ' '*5, end = "\r")
			mess = "TAX_RATE {0} {1}".format(self.data[i]["Destination Zip"], self.data[i]["Destination State"])
			#TODO: Needs error handling for .connect here
			self.connect()
			self._write_msg(mess)
			results.append(self._read_report())
			self._new_connection()
		duration = time.time() - start
		if duration > 60: print("Took {0} minutes to process {1} rows".format(round(duration/60,2), len(results)))
		else: print("Took {0} seconds to process {1} rows".format(round(duration,2), len(results)))
		return results



	def _read_report(self, buff_size = 1024):
		results = []
		first = True
		old_msg = bytes()
		while True:

			try:
				msg = self._read_msg(buff_size)
			except Exception as E:
				print("EXCEPTION: ", E)
				return results
			msg_len = len(msg)
			if msg_len <= 0: return results
			try:




				if msg[msg_len-1:msg_len] == b'\n' and old_msg:
					results += self._process_report_chunk(old_msg + msg)
					old_msg = bytes()
				elif msg[msg_len-1:msg_len] == b'\n' and not old_msg:
					results += self._process_report_chunk(msg)
				else: old_msg += msg
			except UnicodeDecodeError as UE:
				return msg
		return results
	def _process_report_chunk(self, msg, encoding = 'ascii'):
		#@TODO: needs error handling for the decoding
		results = []
		try:
			text=  msg.decode(encoding).split('\n')
		except UnicodeDecodeError as UE:
			text = self.__char_cleanse(msg).split('\n')
		text_len = len(text)
		#each element should be a list since they represent rows in a spreadsheet/report
		#text_len-1 because split('\n') leaves a single '' at the end of the list
		results = [text[i] for i in range(0, text_len-1)]
		#for i in range(0, text_len-1): results.append(text[i])
		return results
	def __char_cleanse(self, btext):

		#for char in [251, 250, 249, 248]: btext.replace(hex(char),'')
		pass

#m_inst = Tax_client('tax_data_test.csv')
m_inst = Tax_client('tax_test_1000.csv')
res = m_inst.req_report()