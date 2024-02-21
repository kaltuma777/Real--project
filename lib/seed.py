from faker import Faker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Employee, Department  # Import your models

Base = declarative_base()

# Connect to the database
engine = create_engine('sqlite:///hr.db', echo=False)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# An instance for Faker
fake = Faker(locale='en_US')

# Function to create employees
def create_employees(num_employees):
    employees = []
    for _ in range(num_employees):
        employee = Employee(
            ssn=fake.ssn(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            job=fake.job(),
            role=fake.random_element(elements=('Manager', 'Analyst', 'Developer', 'Associate')),
            salary=fake.random_int(min=30000, max=150000, step=1000),
            department=Department(name=fake.random_element(elements=('IT', 'HR', 'Marketing', 'Finance')))
        )
        employees.append(employee)
    return employees


# Generate employees
num_employees = 100  # Specify the number of employees you want to generate
employees = create_employees(num_employees)

# Add employees to the database
session.bulk_save_objects(employees)
session.commit()

# Close the session
session.close()
