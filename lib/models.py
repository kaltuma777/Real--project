from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from faker import Faker
import random
import pandas as pd

# Create engine and bind to the SQLite database
engine = create_engine('sqlite:///hr.db', echo=True)

Base = declarative_base()

# An instance for Faker
fake = Faker(locale='en_US')

# Define the Employee class
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    ssn = Column(String(11))
    first_name = Column(String(50))
    last_name = Column(String(50))
    job = Column(String(100))
    department = Column(String(50))
    role = Column(String(50))
    salary = Column(Integer)

# Create the table
Base.metadata.create_all(engine)

# Function for generating employees
def create_employees(num_employees):
    employee_list = []
    for i in range(num_employees):
        employee = Employee(
            ssn=fake.ssn(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            job=fake.job(),
            department=fake.random_element(elements=('IT', 'HR', 'Marketing', 'Finance')),
            role=fake.random_element(elements=('Manager', 'Analyst', 'Developer', 'Associate')),
            salary=fake.random_int(min=30000, max=150000, step=1000)
        )
        employee_list.append(employee)
    return employee_list

# Create employees and add them to the database
employees = create_employees(78)
with engine.connect() as connection:
    for employee in employees:
        connection.execute(Employee.__table__.insert(), vars(employee))

# Fetch all employees from the database and print them
with engine.connect() as connection:
    result = connection.execute(Employee.__table__.select())
    for row in result:
        print(row)
