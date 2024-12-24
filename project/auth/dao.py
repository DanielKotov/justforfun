from dao.base import BaseDAO
from dao.database import User

class UsersDAO(BaseDAO):
    model = User
