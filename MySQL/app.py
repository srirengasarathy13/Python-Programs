from mysql.connector import pooling

# Create Connection Pool
connection = pooling.MySQLConnectionPool(
    pool_name="myPool",
    pool_size=5,
    host="127.0.0.1",
    user="root",
    password="root",
    database="company",
    use_pure=True
)


def display():
    conn = connection.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employee")
    result = cursor.fetchall()

    print("\nEmployee Details")
    print("-" * 40)

    for row in result:
        print(row)

    cursor.close()
    conn.close()


def insert():
    conn = connection.get_connection()
    cursor = conn.cursor()

    empName = input("Enter Employee Name : ")
    salary = int(input("Enter Salary : "))

    cursor.execute(
        "INSERT INTO employee(empName, salary) VALUES (%s, %s)",
        (empName, salary)
    )

    conn.commit()

    print("Employee Inserted Successfully")

    cursor.close()
    conn.close()

    display()


def delete():
    display()

    conn = connection.get_connection()
    cursor = conn.cursor()

    empId = int(input("Enter Employee ID to Delete : "))

    cursor.execute(
        "DELETE FROM employee WHERE empId=%s",
        (empId,)
    )

    conn.commit()

    print("Employee Deleted Successfully")

    cursor.close()
    conn.close()

    display()


def update():
    display()

    conn = connection.get_connection()
    cursor = conn.cursor()

    empId = int(input("Enter Employee ID : "))
    salary = int(input("Enter New Salary : "))

    cursor.execute(
        "UPDATE employee SET salary=%s WHERE empId=%s",
        (salary, empId)
    )

    conn.commit()

    print("Employee Updated Successfully")

    cursor.close()
    conn.close()

    display()


while True:
    print("\n===== Employee Management =====")
    print("1. Display")
    print("2. Insert")
    print("3. Delete")
    print("4. Update")
    print("5. Exit")

    try:
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

    except ValueError:
        print("Please enter a valid number.")