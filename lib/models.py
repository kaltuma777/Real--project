from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    #Define the relationship with employees
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    ssn = Column(String(11))
    first_name = Column(String(50))
    last_name = Column(String(50))
    job = Column(String(100))
    role = Column(String(50))
    salary = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))  # Add this line
    
     #Define the relationship with departments
    department = relationship("Department", back_populates="employees")
