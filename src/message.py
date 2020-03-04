from messageenums.py import (
	MessageTypes,
	Codes,
	OptionNums
)
from random import randint
import socket

class Message(object):
	class Header(object):
		# Header is 4 bytes
		def __init__(self, msg_type, code_type, code, token, message_id):
			self.code = Code(code_type)
			token_len = len(token)
			self.m_type = MessageTypes(msg_type)
			if token_len > 8:
				raise ValueError('Token length must be between 0 and 8')
			self.tkl = token_len
			self.mid = message_id
			self.version = 1

	class Option(object):

		def __init__(self, number, value):
			self._number = OptionNums(number)
			self._value = None 

		@property
		def number(self):
			return self._number

		@property
		def value(self):
			return self._value


	def __init__(self, msg_type, code_type, code, token, message_id, msg_class):
		self.header = Header(msg_type, code_type, code, token, message_id)
		is_message_type_correct = self.__allowed_msg_types(msg_class, self.header.m_type)
		if not is_message_type_correct:
			raise ValueError('Choose the correct message type for the message')
		self._token = token
		self._options = []
		self._payload = None
		self._acknowledged = False
		self._rejected = False

	def __allowed_msg_types(self, msg_class, msg_type):
		if msg_class == 'Response':
			return msg_type in [MessageTypes.CON, MessageTypes.NON, MessageTypes.ACK]
		if msg_class == 'Request':
			return msg_type in [MessageTypes.CON, MessageTypes.NON]
		if msg_class == 'Empty':
			return msg_type in [MessageTypes.CON, MessageTypes.ACK, MessageTypes.RST]

	@property
	def message_id(self):
		# 16 bit unsigned integer in network byte order
		return self.header.mid

	@property
	def code(self):
		# 8 bit unsigned integer 0-65,355
		return self.header.code

	@property
	def token_length(self):
		# 4 bit unsigned integer
		return self.header.tkl

	@property
	def message_type(self):
		return self.header.m_type

	@property
	def version(self):
		return self.header.version

	@property
	def token(self):
		return self._token

	@property
	def options(self):
		return self._options

	@property
	def payload(self):
		return self._payload

	@property
	def acknowledged(self):
		return self._acknowledged

	@property
	def rejected(self):
		return self._rejected

class Response(Message):
	def __init__(self, msg_type, code_type, code, token, message_id):
		super().__init__(msg_type, code_type, code, token, message_id, cls.__name__)



# class SuccessReponse(Message):

# 	def __init__(self, msg_type, code, token, message_id):
# 		super().__init__(msg_type, cls.__name__, code, token, message_id)

# class ClientError(Message):

# 	def __init__(self, msg_type, code, token, message_id):
# 		super().__init__(msg_type, cls.__name__, code, token, message_id)

# class ServerError(Message):

# 	def __init__(self, msg_type, code, token, message_id):
# 		super().__init__(msg_type, cls.__name__, code, token, message_id)

# class Request(object):

# 	def __init__(self, msg_type, code, token, message_id):
# 		super().__init__(msg_type, cls.__name__, code, token, message_id)