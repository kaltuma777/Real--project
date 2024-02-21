import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee, Department

# Database connection
DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@click.group()
def cli():
    """CLI for managing employees and departments."""


@cli.command()
@click.argument('employee_id', type=int)
def get_employee(employee_id):
    """Get details of a specific employee."""
    session = Session()
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        click.echo(f"Employee ID: {employee.id}")
        click.echo(f"First Name: {employee.first_name}")
        click.echo(f"Last Name: {employee.last_name}")
        click.echo(f"Job: {employee.job}")
        click.echo(f"Role: {employee.role}")
        click.echo(f"Salary: {employee.salary}")
        click.echo(f"Department: {employee.department.name}")
    else:
        click.echo("Employee not found.")
    session.close()


@cli.command()
@click.argument('department_name')
def count_employees(department_name):
    """Count the number of employees in a department."""
    session = Session()
    department = session.query(Department).filter_by(name=department_name).first()
    if department:
        employee_count = len(department.employees)
        click.echo(f"Number of Employees in {department_name}: {employee_count}")
    else:
        click.echo("Department not found.")
    session.close()


@cli.command()
@click.option('--ssn', prompt='Enter SSN', help='Employee Social Security Number')
@click.option('--first_name', prompt='Enter First Name', help='Employee First Name')
@click.option('--last_name', prompt='Enter Last Name', help='Employee Last Name')
@click.option('--job', prompt='Enter Job', help='Employee Job')
@click.option('--role', prompt='Enter Role', help='Employee Role')
@click.option('--salary', prompt='Enter Salary', help='Employee Salary')
@click.option('--department_id', prompt='Enter Department ID', help='Department ID to assign')
def add_employee(ssn, first_name, last_name, job, role, salary, department_id):
    """Add a new employee."""
    session = Session()
    employee = Employee(
        ssn=ssn,
        first_name=first_name,
        last_name=last_name,
        job=job,
        role=role,
        salary=salary,
        department_id=department_id
    )
    session.add(employee)
    session.commit()
    click.echo("Employee added successfully.")
    session.close()


@cli.command()
@click.argument('employee_id', type=int)
def delete_employee(employee_id):
    """Delete an employee."""
    session = Session()
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()
        click.echo("Employee deleted successfully.")
    else:
        click.echo("Employee not found.")
    session.close()


if __name__ == '__main__':
    cli()
