from mysql.connector import pooling

connection = pooling.MySQLConnectionPool(pool_name = "myPool",pool_size = 1,host="127.0.0.1",user="root",password="root",database="company",use_pure=True)

print('connected')

cursor = connection.get_connection()


def display():
    cursor.execute("SELECT * FROM employee")
    result = cursor.fetchall()

    print("\nEmployee Details")
    for row in result:
        print(row)


def insert():
    # empId = int(input("Enter Employee ID : "))
    empName = input("Enter Employee Name : ")
    salary = int(input("Enter Salary : "))

    cursor.execute(
        "INSERT INTO employee (empName, salary) VALUES (%s, %s)",
        (empName, salary)
    )

    connection.commit()
    print("Employee Inserted Successfully")
    display()


def delete():
    display()

    empId = int(input("Enter Employee ID to Delete : "))

    cursor.execute(
        "DELETE FROM employee WHERE empId=%s",
        (empId,)
    )

    connection.commit()
    print("Employee Deleted Successfully")
    display()


def update():
    display()

    empId = int(input("Enter Employee ID : "))
    salary = int(input("Enter New Salary : "))

    cursor.execute(
        "UPDATE employee SET salary=%s WHERE empId=%s",
        (salary, empId)
    )

    connection.commit()
    print("Employee Updated Successfully")
    display()


while True:

    print("\n===== Employee Management =====")
    print("1. Display")
    print("2. Insert")
    print("3. Delete")
    print("4. Update")
    print("5. Exit")

    choice = int(input("Enter your choice : "))

    if choice == 1:
        display()

    elif choice == 2:
        insert()

    elif choice == 3:
        delete()

    elif choice == 4:
        update()

    elif choice == 5:
        print("Thank you...")
        break

    else:
        print("Invalid Choice")

cursor.close()
connection.close()