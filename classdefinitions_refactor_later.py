# class Assignment(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     date_due: str = None
#     date_assign: str
#     wght: int
#
# class AssignmentResult(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     stu_id: int
#     stu_mark: float
#     wght: int
#
# class AssignmentList(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     class_id : Optional[int]
#     name: str


# class EventAttendence (SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     stu_id: int
#     class_id: int
#     attend: bool

# class ClassInfo(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     grade: int
#     tea_id: int
#     tea_name: str
#
# class ClassList(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str

# class ClassAttendence(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     stu_id: int
#     attend:bool
#
# class StudentList(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     grade: Optional[int] = None
#
# class StudentGrades(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     class_id:int
#     curr_mark:int
#
# class Student(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     f_name: str
#     l_name: str
#     age: Optional[int] = None
#     grade: int
#     disc_name: str
#
# class TeacherList(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#
# class Teacher(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     f_name: str
#     l_name: str
#     #classes_teaching: list[int]
#     age: Optional[int] = None
#     disc_name: str