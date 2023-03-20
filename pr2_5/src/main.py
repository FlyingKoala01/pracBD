"""
==================

This is the main module. It will interact with all of the other modules and
with the user. 

The functions are just an analogy of the options in the menu. This means
that executing any function is like clicking on that menu option.

==================
"""

from time import sleep

import input_manager
import queries
import database

def insert():
    """
    Option used to insert a new element (row) into a specific table.
    Once user selects the table, it will ask for the attributes of that given table and lastly run 
    a hard-coded SQL query to insert the element.

    """

    table = input_manager.get_tables()
    if table == "EMPLOYEE":
        id_employee = input_manager.get_attribute("employee", "id_employee")
        street = input_manager.get_attribute("employee", "street")
        city = input_manager.get_attribute("employee", "city")

        queries.insert_employee(id_employee, street, city)
    
    elif table == "JOB":
        id_employee = input_manager.get_attribute("jobs", "id_employee")
        id_company = input_manager.get_attribute("jobs", "id_company")
        salary = input_manager.get_attribute("jobs", "salary")

        queries.insert_job(id_employee, id_company, salary)
    
    elif table == "COMPANY":
        id_company = input_manager.get_attribute("company", "id_company")
        city = input_manager.get_attribute("company", "city")

        queries.insert_company(id_company, city)
    
    elif table == "MANAGER":
        id_employee = input_manager.get_attribute("manager", "id_employee")
        id_employee_coordinator = input_manager.get_attribute("manager", "id_employee_coordinator")

        queries.insert_manager(id_employee, id_employee_coordinator)

    print()

def delete():
    """
    Option used to delete an element (row) from a specific table.
    Once user selects the table, it will ask for the primary key of that given table and lastly run 
    a hard-coded SQL query to delete the row.

    """

    table = input_manager.get_tables()
    if table == "EMPLOYEE":
        id_employee = input_manager.get_attribute("employee", "id_employee")
        
        queries.delete_employee(id_employee)
    
    elif table == "JOB":
        id_employee = input_manager.get_attribute("jobs", "id_employee")

        queries.delete_job(id_employee)
    
    elif table == "COMPANY":
        id_company = input_manager.get_attribute("company", "id_company")
        
        queries.delete_company(id_company)
    
    elif table == "MANAGER":
        id_employee = input_manager.get_attribute("manager", "id_employee")
        id_employee_coordinator = input_manager.get_attribute("manager", "id_employee_coordinator")

        queries.delete_manager(id_employee, id_employee_coordinator)

    print()

def view():
    """
    Option used to view all the elements from a specific table.
    Once user selects the table, it will dump each row in the table.

    """
    table = input_manager.get_tables()

    if table == "EMPLOYEE":
        cursor = queries.view_employee()
        print("ID   ||  STREET  ||  CITY")
        print("="*30)
        for row in cursor:
            print(f"{row[0]}   ||  {row[1]}    ||  {row[2]}")
    
    elif table == "JOB":
        cursor = queries.view_job()
        print("ID EMPLOYEE  ||  ID COMPANY  ||  SALARY")
        print("="*40)
        for row in cursor:
            print(f"{row[0]}    ||  {row[1]}    ||  {row[2]}")
    
    elif table == "COMPANY":
        cursor = queries.view_company()
        print("ID COMPANY   ||   CITY")
        print("="*25)
        for row in cursor:
            print(f"{row[0]}    ||  {row[1]}")
    
    elif table == "MANAGER":
        cursor = queries.view_manager()
        print("ID EMPLOYEE   ||   ID MANAGER")
        print("="*25)
        for row in cursor:
            print(f"{row[0]}    ||  {row[1]}")

    print()

def modify():
    """
    Option used to modify a value of a specific column of a specific row from a table.

    """
    table = input_manager.get_tables()
    if table == "EMPLOYEE":
        id_employee = input_manager.get_attribute("employee", "id_employee")
        col = input_manager.get_attributes(table)
        value = input("New value: ")
        queries.modify_employee(id_employee, col, value)
    
    elif table == "JOB":
        id_employee = input_manager.get_attribute("jobs", "id_employee")
        col = input_manager.get_attributes(table)
        value = input("New value: ")
        queries.modify_job(id_employee, col, value )
    
    elif table == "COMPANY":
        id_company = input_manager.get_attribute("company", "id_company")
        col = input_manager.get_attributes(table)
        value = input("New value: ")
        queries.modify_company(id_company, col, value)
    
    elif table == "MANAGER":
        id_employee = input_manager.get_attribute("manager", "id_employee")
        col = input_manager.get_attributes(table)
        value = input("New value: ")
        queries.modify_manager(id_employee, col, value)

    print()

def most_employees():
    cursor = queries.company_with_most_employees()
    print("ID COMPANY  ||  COUNT ")
    print("="*20)
    for row in cursor:
        print(f"{row[0]}   ||  {row[1]}")

def update_salary_managers():
    new_salary = int(input("By what factor (%) would you like to increase Managers' salary?"))

    queries.update_managers_salary(new_salary)

def employees_same_city():
    cursor = queries.employees_same_city()
    print("ID EMPLOYEE")
    print("="*15)
    for row in cursor:
        print(f"{row[0]}")

def employees_same_city_manager():
    cursor = queries.employees_same_city_as_manager()
    print("ID EMPLOYEE")
    print("="*15)
    for row in cursor:
        print(f"{row[0]}")

def employees_by_city():
    city = input("What city would you like to check?")

    cursor = queries.employees_in_city(city)

    print("ID EMPLOYEE")
    print("="*15)
    for row in cursor:
        print(f"{row[0]}")

def employees_by_salary():
    order = input("What order would you like to order by the employees salary? [ASC/DESC]")

    cursor = queries.employees_by_salary(order)

    print("ID EMPLOYEE")
    print("="*15)
    for row in cursor:
        print(f"{row[0]}")

MENU_OPTIONS_TEXT = [
    "Insert",
    "Delete",
    "View",
    "Modify",
    "Export CSV",
    "Import CSV",
    "Company with most Employees",
    "Update Managers Salary",
    "Employees in the same city",
    "Employees in the same city as their manager",
    "Employees in a specific city",
    "Employees by salary",
    "Exit"
]

MENU_OPTIONS_CALLBACKS = [
    insert,
    delete,
    view,
    modify,
    database.dump_db,
    database.load_db,
    most_employees,
    update_salary_managers,
    employees_same_city,
    employees_same_city_manager,
    employees_by_city,
    employees_by_salary
]

def print_menu():
    """
    Prints the user menu. In order to make this program easy-to-scale,
    the options are defined in a list in this module.

    This is the only function of this module that doesn't gather user input,
    so we can introduce a doctest.

    >>> print_menu()
    ====================
    EMPLOYER MANAGER MENU
    ====================
    <BLANKLINE>
    Opcions:
     1: Insert
     2: Delete
     3: View
     4: Modify
     5: Export CSV
     6: Import CSV
     7: Company with most Employees
     8: Update Managers Salary
     9: Employees in the same city
     10: Employees in the same city as their manager
     11: Employees in a specific city
     12: Employees by salary
     13: Exit
    <BLANKLINE>
    """
    print("="*20)
    print("EMPLOYER MANAGER MENU")
    print("="*20 + "\n")
    print("Opcions:")
    for i in range(len(MENU_OPTIONS_TEXT)):
        print(f" {i+1}: {MENU_OPTIONS_TEXT[i]}")
    print()

if __name__=="__main__":

    database.check_db()    

    while True:
        print_menu()
        option = input_manager.get_menu_option(len(MENU_OPTIONS_TEXT))

        if option == len(MENU_OPTIONS_TEXT): # User wants to exit
            print("Thanks for using this application!")
            break

        print()
        MENU_OPTIONS_CALLBACKS[option-1]()
        # We wait 1 sec in order to let the user read the result.
        sleep(2)
        print()
