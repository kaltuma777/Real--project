import click
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base, Employee, Department

Base = declarative_base()

# Connect to the database
DATABASE_URL = 'sqlite:///hr.db'
engine = create_engine(DATABASE_URL)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

@click.group()
def cli():
    """CLI for managing employees and departments."""

@cli.command()
@click.argument('num_employees', type=int)
def populate_employees(num_employees):
    """Populate the database with random employees."""
    session = Session()
    create_employees(session, num_employees)
    session.close()

@cli.command()
@click.argument('first_name')
@click.argument('last_name')
@click.argument('role')
@click.argument('salary', type=int)
def add_employee(first_name, last_name, role, salary):
    """Add an employee to the database."""
    session = Session()
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        role=role,
        salary=salary,
    )
    session.add(employee)
    session.commit()
    click.echo("Employee added successfully.")
    session.close()

@cli.command()
@click.argument('employee_id', type=int)
def delete_employee(employee_id):
    """Delete an employee from the database."""
    session = Session()
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()
        click.echo("Employee deleted successfully.")
    else:
        click.echo("Employee not found.")
    session.close()

def create_employees(session, num_employees):
    fake = Faker(locale='en_US')
    employees = []
    for _ in range(num_employees):
        employee = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=fake.random_element(elements=('Manager', 'Analyst', 'Developer', 'Associate')),
            salary=fake.random_int(min=30000, max=150000, step=1000),
        )
        employees.append(employee)
    session.bulk_save_objects(employees)
    session.commit()

if __name__ == "__main__":
    cli()
