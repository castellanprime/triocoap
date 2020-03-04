from enum import Enum
from collections import namedtuple

class MessageTypes(Enum):
	CON = 0
	NON = 1
	RST = 3
	ACK = 2

	def get_long_type(self):
		if self.value == 0:
			return 'CONFIRMABLE'
		if self.value == 1:
			return 'NONCONFIRMABLE'
		if self.value == 2:
			return 'RESET'
		if self.value == 3:
			return 'ACKNOWLEDGEMENT'

class Codes(Enum):

	# Request Codes Begin
	EMPTY = 0
	GET = 1
	POST = 2
	PUT = 3
	DELETE = 4
	# Request Codes End

	# Response Codes Begin
	CREATED = 33
	DELETED = 34
	VALID = 35
	CHANGED = 36
	CONTENT = 37

	# Client Error Codes Begin
	BAD_REQUEST = 128
	UNAUTHORIZED = 129
	BAD_OPTION = 130
	FORBIDDEN = 131
	NOT_FOUND = 132
	METHOD_NOT_ALLOWED = 133
	NOT_ACCEPTABLE = 134
	PRECONDITION_FAILED= 140
	REQUST_ENTITY_TOO_LARGE = 141
	UNSUPPORTED_CONTENT_FORMAT = 143
	# Client Error Codes End

	# Server Error Codes Begin
	INTERNAL_SERVER_ERROR = 160
	NOT_IMPLEMENTED = 161
	BAD_GATEWAY = 162
	SERVICE_UNAVAILABLE = 163
	GATEWAY_TIMEOUT = 164
	PROXYING_NOT_SUPPORTED = 165
	# Server Error Codes End

	def is_request(self):
		return all([self.value >= 0, self.value <= 4])

	def is_successful_response(self):
		return all([self.value >= 35, self.value <= 37])

	def is_client_error(self):
		return all([self.value >= 128, self.value <= 143])

	def is_server_error(self):
		return all([self.value >= 160, self.value <= 165])

BitLength = namedtuple('Length', 'min max')

class OptionNums(Enum):

	RESERVED = 0
	IF_MATCH = 1
	URI_HOST = 3
	ETAG = 4
	IF_NONE_MATCH = 5
	URI_PORT = 7
	LOCATION_PATH = 8
	URI_PATH = 11
	CONTENT_FORMAT = 12
	MAX_AGE = 14
	URI_QUERY = 15
	ACCEPT = 17
	LOCATION_QUERY = 20
	PROXY_URI = 35
	PROXY_SCHEME = 39
	SIZE1 = 60

	def has_opaque_format(self):
		return self.value in [1, 4]

	def has_unsigned_integer_format(self):
		return self.value in [7, 12, 14, 17, 60]

	def has_string_format(self):
		return self.value in [3, 8, 11, 15, 20, 35, 39]
	
	def has_empty_format(self):
		return self.value == 5

	def get_default_value(self):
		if self.value in [1, 4, 5, 8, 11, 12, 15, 17, 20, 35, 39, 60]:
			return
		elif self.value in 14:
			return 60

	def is_repeatable(self):
		pass

	def get_length(self):
		if self.value == 1:
			return BitLength(min=0, max=8)
		if self.value in [3, 39]:
			return BitLength(min=1, max=255)
		if self.value in [8, 11, 15, 20]:
			return BitLength(min=0, max=255)
		if self.value == 4:
			return BitLength(min=1, max=8)
		if self.value == 5:
			return BitLength(min=0, max=0)
		if self.value in [7, 12, 17]:
			return BitLength(min=0, max=2) 
		if self.value in [14, 60]:
			return BitLength(min=0, max=4)
		if self.value == 35:
			return BitLength(min=1, max=1035)