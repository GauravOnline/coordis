from db.repositories.user_repo import UserRepository
from db.models.user import User
from datetime import datetime
from typing import List, Optional


class UserService:
    def __init__(self, session):
        self.repo = UserRepository(session)

    def add_user(self, user_name: str, date_assigned: datetime, user_role: str = "Student") -> User:
        user = User(
            user_name=user_name,
            date_assigned=date_assigned,
            user_role=user_role
        )
        return self.repo.add_user(user)

    def list_users(self) -> List[User]:
        return self.repo.get_all_users()
    
    def list_user_by_role(self, role: str) -> List[User]:
        return self.repo.get_user_by_role(role)

    def get_user(self, user_name: str) -> Optional[User]:
        return self.repo.get_user_by_name(user_name)

    def set_permissions(self, user_name: str, role: str) -> bool:
        return self.repo.set_permissions(user_name, role)
