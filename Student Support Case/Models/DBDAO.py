from copy import copy

from Models.BookDAO import BookDAO
from Models.UserDAO import UserDAO
from Models.AdministratorRepository import AdministratorRepository

from Models.DatabaseGateway import DatabaseGateway

class DBDAO(DatabaseGateway):
	def __init__(self, app):
		super(DBDAO, self).__init__(app)

		self.book = BookDAO(copy(self))
		self.user = UserDAO(copy(self))
		self.admin = AdministratorRepository(copy(self))
