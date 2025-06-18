from sqlmodel import Session, select, update
from db.models.user import User
from typing import List

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, role: User) -> User:
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def get_user_by_name(self, user_name2: str) -> User:
        statement = select(User).where(User.user_name == user_name2) 
        result = self.session.exec(statement).first()
        return result
    
    
    def get_user_by_role(self,role:str) -> User:
        statement = select(User).where(User.user_role == role)
        results = self.session.exec(statement).all()
        return results


    def get_all_users(self) -> List[User]:
        statement = select(User)
        results = self.session.exec(statement).all()
        return results
    
    def set_permissions(self, user_name: str, role: str) -> User:
        user = self.get_user_by_name(user_name)
        print(user)
        role = role
        if user:
            user.user_role = role
            self.session.commit()
            self.session.refresh(user)
            return user
        return user
