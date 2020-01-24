import socket, time
#will be used mostly as a proof of concept and for testing
#actual "Eclipse client" will be functional or a collection of static methods
class Eclipse_client:
	def __init__(self):
		self._host = '192.168.99.249'
		self._port = 3210
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._sock.settimeout(45.0)
		self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	def connect(self):
		self._sock.connect((self._host, self._port))
	def disconnect(self):
		self._sock.close()
	def _new_connection(self):
		#replaces the old socket with a new one on the same port and host
		self._sock.close()
		#socket.shutdown(how) <- need this!
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._sock.settimeout(45.0)
		self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

	def _read_msg(self, buff_size=1024):
		while True: 
			mess = self._sock.recv(buff_size)
			return mess
	def _write_msg(self, message, encoding='ascii'):
		self._sock.send(bytes(message, encoding))
	def _read_report(self):
		pass







def connect(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))
	sock.settimeout(45.0)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	return sock
def read_msg(sock, buff_size = 1024):
	while True:
		mess = sock.recv(buff_size)

		#if len(mess) <= 0: return mess

		#n_mess = mess.decode('ascii')
		return mess
def write_msg(sock, message, encoding='ascii'):
	sock.send(bytes(message, encoding))
	return
def read_report(sock, buff_size=1024):
	results = []
	first = True
	old_msg = bytes()
	while True:
		'''if first:
			msg = read_msg(sock, buff_size)
			buff_size = int(msg.decode('ascii')) #just changed
			print(buff_size)
			first = False'''
		try:
			msg = read_msg(sock, buff_size)
		except Exception as E:
			print("EXCEPTION: ", E)
			return results
		msg_len = len(msg)
		if msg_len <= 0: return results


		#print("Recieved:")
		#print(msg)
		#print(msg_len)

		if msg[msg_len-1:msg_len] == b'\n' and old_msg:
			results += process_report_chunk(old_msg + msg)
			old_msg = bytes()
		elif msg[msg_len-1:msg_len] == b'\n' and not old_msg:
			results += process_report_chunk(msg)
		else: old_msg += msg

			


		#st = msg.decode('ascii')
		#results.append(chunk)

	return results




def process_report_chunk(data, encoding = 'ascii'):
	#@TODO: needs error handling for the decoding
	results = []
	text=  data.decode(encoding).split('\n')
	text_len = len(text)
	#each element should be a list since they represent rows in a spreadsheet/report
	#text_len-1 because split('\n') leaves a single '' at the end of the list
	results = [text[i] for i in range(0, text_len-1)]
	#for i in range(0, text_len-1): results.append(text[i])
	return results






