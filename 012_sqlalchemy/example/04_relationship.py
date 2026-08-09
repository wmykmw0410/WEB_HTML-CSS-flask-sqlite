import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

base_dir = os.path.dirname(__file__)
database = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
engine = create_engine(database, echo=False)
Base   = declarative_base()


# ---- モデル定義（1対多：1つの部署に複数の社員）----

class Department(Base):
    __tablename__ = 'departments'
    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    # 1対多：dept.employees → その部署の社員リスト
    employees = relationship('Employee', back_populates='department')

    def __str__(self):
        return f"Department(id={self.id}, name={self.name})"


class Employee(Base):
    __tablename__ = 'employees'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))  # 外部キー
    # 多対1：emp.department → その社員の部署（uselist=False で単一オブジェクトを返す）
    department = relationship('Department', back_populates='employees', uselist=False)

    def __str__(self):
        return f"Employee(id={self.id}, name={self.name})"


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ---- データ登録（relationship.append で紐づけ）----
dept01 = Department(name='Development')
dept02 = Department(name='Sales')

emp01 = Employee(name='Tom')
emp02 = Employee(name='John')
emp03 = Employee(name='Alice')
emp04 = Employee(name='Mary')

dept01.employees.append(emp01)
dept01.employees.append(emp02)
dept02.employees.append(emp03)
dept02.employees.append(emp04)

session.add_all([dept01, dept02])
session.commit()

# ---- 参照：社員 → 部署 ----
print("=== 社員から部署を参照 ===")
emp = session.query(Employee).filter_by(id=1).first()
print(emp)
print(f"  所属部署: {emp.department}")

print()

# ---- 参照：部署 → 社員一覧 ----
print("=== 部署から社員一覧を参照 ===")
dept = session.query(Department).filter_by(id=1).first()
print(dept)
for e in dept.employees:
    print(f"  {e}")

session.close()
