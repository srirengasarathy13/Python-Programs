from nicegui import ui
from mysql.connector import connect, Error
from datetime import date


# =========================================================
# DATABASE CONNECTION
# =========================================================

def connect_database():
    return connect(
        host='localhost',
        user='root',
        password='root',
        database='simple_hrms'
    )


# =========================================================
# GLOBAL VARIABLES
# =========================================================

current_employee = None


# =========================================================
# DATABASE HELPER
# =========================================================

def execute_query(query, values=None, fetch=False):
    connection = None
    cursor = None

    try:
        connection = connect_database()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, values or ())

        if fetch:
            result = cursor.fetchall()
            return result

        connection.commit()
        return True

    except Error as e:
        ui.notify(f"Database Error: {e}", type='negative')
        return None

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# COMMON STYLING
# =========================================================

def page_header(title, subtitle=None):
    with ui.row().classes(
        'w-full items-center justify-between mb-6'
    ):
        with ui.column().classes('gap-0'):
            ui.label(title).classes(
                'text-3xl font-bold text-gray-800'
            )

            if subtitle:
                ui.label(subtitle).classes(
                    'text-gray-500'
                )

        ui.button(
            'Logout',
            icon='logout',
            on_click=logout
        ).props('outline color=negative')


def menu_button(text, icon, page_function):
    ui.button(
        text,
        icon=icon,
        on_click=page_function
    ).props(
        'flat'
    ).classes(
        'w-full justify-start text-left'
    )


# =========================================================
# LOGIN PAGE
# =========================================================

@ui.page('/')
def login_page():

    ui.query('body').classes('bg-gray-100')

    with ui.column().classes(
        'w-full min-h-screen items-center justify-center'
    ):

        with ui.card().classes(
            'w-[400px] p-8 shadow-lg'
        ):

            ui.label('Simple HRMS').classes(
                'text-3xl font-bold text-center w-full'
            )

            ui.label(
                'Employee Management System'
            ).classes(
                'text-gray-500 text-center w-full mb-6'
            )

            email = ui.input(
                'Email',
                placeholder='Enter your email'
            ).classes('w-full')

            password = ui.input(
                'Password',
                password=True,
                password_toggle_button=True
            ).classes('w-full')

            ui.button(
                'Login',
                icon='login',
                on_click=lambda: login(email.value, password.value)
            ).classes('w-full mt-4')

            ui.separator().classes('my-4')

            ui.label(
                'Demo Login'
            ).classes('font-bold')

            ui.label(
                'Email: sri@gmail.com'
            ).classes('text-sm text-gray-600')

            ui.label(
                'Password: 1234'
            ).classes('text-sm text-gray-600')


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login(email, password):

    global current_employee

    if not email or not password:
        ui.notify(
            'Please enter email and password',
            type='warning'
        )
        return

    result = execute_query(
        """
        SELECT *
        FROM employees
        WHERE email = %s
        AND password = %s
        """,
        (email, password),
        fetch=True
    )

    if result:

        current_employee = result[0]

        ui.notify(
            'Login successful!',
            type='positive'
        )

        ui.navigate.to('/dashboard')

    else:

        ui.notify(
            'Invalid email or password',
            type='negative'
        )

        
# =========================================================
# DASHBOARD
# =========================================================

@ui.page('/dashboard')
def dashboard():

    if not check_login():
        return

    page_header(
        'Dashboard',
        f"Welcome, {current_employee['name']}"
    )

    with ui.row().classes('w-full gap-6'):

        # Employee Card
        with ui.card().classes(
            'w-[300px] p-5'
        ):
            ui.icon(
                'person',
                size='40px'
            )

            ui.label(
                current_employee['name']
            ).classes(
                'text-xl font-bold mt-2'
            )

            ui.label(
                current_employee['designation']
            ).classes(
                'text-gray-500'
            )

            ui.label(
                current_employee['department']
            ).classes(
                'text-gray-500'
            )

        # Attendance Card
        attendance_count = execute_query(
            """
            SELECT COUNT(*) AS total
            FROM attendance
            WHERE employee_id = %s
            AND status = 'Present'
            """,
            (current_employee['employee_id'],),
            fetch=True
        )

        present_count = (
            attendance_count[0]['total']
            if attendance_count
            else 0
        )

        with ui.card().classes(
            'w-[250px] p-5'
        ):
            ui.icon(
                'event_available',
                size='40px'
            )

            ui.label(
                'Present Days'
            ).classes(
                'text-gray-500'
            )

            ui.label(
                str(present_count)
            ).classes(
                'text-3xl font-bold'
            )

        # Leave Card
        leave_count = execute_query(
            """
            SELECT COUNT(*) AS total
            FROM leaves
            WHERE employee_id = %s
            AND status = 'Approved'
            """,
            (current_employee['employee_id'],),
            fetch=True
        )

        approved_leaves = (
            leave_count[0]['total']
            if leave_count
            else 0
        )

        with ui.card().classes(
            'w-[250px] p-5'
        ):
            ui.icon(
                'event_busy',
                size='40px'
            )

            ui.label(
                'Approved Leaves'
            ).classes(
                'text-gray-500'
            )

            ui.label(
                str(approved_leaves)
            ).classes(
                'text-3xl font-bold'
            )

        # Salary Card
        salary_result = execute_query(
            """
            SELECT net_salary
            FROM salary
            WHERE employee_id = %s
            ORDER BY salary_id DESC
            LIMIT 1
            """,
            (current_employee['employee_id'],),
            fetch=True
        )

        latest_salary = (
            salary_result[0]['net_salary']
            if salary_result
            else 0
        )

        with ui.card().classes(
            'w-[250px] p-5'
        ):
            ui.icon(
                'payments',
                size='40px'
            )

            ui.label(
                'Latest Salary'
            ).classes(
                'text-gray-500'
            )

            ui.label(
                f'₹ {latest_salary}'
            ).classes(
                'text-3xl font-bold'
            )

    # Quick Actions

    ui.label(
        'Quick Actions'
    ).classes(
        'text-2xl font-bold mt-10 mb-4'
    )

    with ui.row().classes('gap-4'):

        ui.button(
            'My Profile',
            icon='person',
            on_click=lambda: ui.navigate.to('/profile')
        ).props('outline')

        ui.button(
            'Attendance',
            icon='event',
            on_click=lambda: ui.navigate.to('/attendance')
        ).props('outline')

        ui.button(
            'Apply Leave',
            icon='event_busy',
            on_click=lambda: ui.navigate.to('/leave')
        ).props('outline')

        ui.button(
            'Salary',
            icon='payments',
            on_click=lambda: ui.navigate.to('/salary')
        ).props('outline')


# =========================================================
# PROFILE PAGE
# =========================================================

@ui.page('/profile')
def profile():

    if not check_login():
        return

    page_header(
        'My Profile',
        'View and update your employee information'
    )

    with ui.card().classes(
        'w-full max-w-2xl p-6'
    ):

        name = ui.input(
            'Name',
            value=current_employee['name']
        ).classes('w-full')

        email = ui.input(
            'Email',
            value=current_employee['email']
        ).classes('w-full')

        phone = ui.input(
            'Phone',
            value=current_employee['phone'] or ''
        ).classes('w-full')

        department = ui.input(
            'Department',
            value=current_employee['department'] or ''
        ).classes('w-full')

        designation = ui.input(
            'Designation',
            value=current_employee['designation'] or ''
        ).classes('w-full')

        ui.label(
            f"Employee ID: {current_employee['employee_code']}"
        ).classes(
            'text-gray-500 mt-2'
        )

        ui.label(
            f"Joining Date: {current_employee['joining_date']}"
        ).classes(
            'text-gray-500'
        )

        ui.button(
            'Update Profile',
            icon='save',
            on_click=lambda: update_profile(
                name.value,
                email.value,
                phone.value,
                department.value,
                designation.value
            )
        ).classes('mt-4')


# =========================================================
# UPDATE PROFILE
# =========================================================

def update_profile(
    name,
    email,
    phone,
    department,
    designation
):

    if not name or not email:
        ui.notify(
            'Name and email are required',
            type='warning'
        )
        return

    result = execute_query(
        """
        UPDATE employees
        SET
            name = %s,
            email = %s,
            phone = %s,
            department = %s,
            designation = %s
        WHERE employee_id = %s
        """,
        (
            name,
            email,
            phone,
            department,
            designation,
            current_employee['employee_id']
        )
    )

    if result:

        current_employee['name'] = name
        current_employee['email'] = email
        current_employee['phone'] = phone
        current_employee['department'] = department
        current_employee['designation'] = designation

        ui.notify(
            'Profile updated successfully',
            type='positive'
        )


# =========================================================
# ATTENDANCE PAGE
# =========================================================

@ui.page('/attendance')
def attendance_page():

    if not check_login():
        return

    page_header(
        'Attendance',
        'Mark and view your attendance'
    )

    today = date.today()

    today_record = execute_query(
        """
        SELECT *
        FROM attendance
        WHERE employee_id = %s
        AND attendance_date = %s
        """,
        (
            current_employee['employee_id'],
            today
        ),
        fetch=True
    )

    with ui.card().classes(
        'w-full max-w-xl p-6 mb-6'
    ):

        ui.label(
            f"Today's Date: {today}"
        ).classes(
            'text-lg font-bold'
        )

        if today_record:

            ui.label(
                f"Today's Status: {today_record[0]['status']}"
            ).classes(
                'text-lg mt-2'
            )

        else:

            ui.label(
                'Attendance not marked'
            ).classes(
                'text-gray-500 mt-2'
            )

            with ui.row().classes('gap-3 mt-4'):

                ui.button(
                    'Present',
                    icon='check',
                    on_click=lambda: mark_attendance('Present')
                )

                ui.button(
                    'Absent',
                    icon='close',
                    on_click=lambda: mark_attendance('Absent')
                ).props('outline color=negative')

    ui.label(
        'Attendance History'
    ).classes(
        'text-2xl font-bold mb-3'
    )

    records = execute_query(
        """
        SELECT
            attendance_date,
            status
        FROM attendance
        WHERE employee_id = %s
        ORDER BY attendance_date DESC
        """,
        (current_employee['employee_id'],),
        fetch=True
    )

    if records:

        columns = [
            {
                'name': 'attendance_date',
                'label': 'Date',
                'field': 'attendance_date'
            },
            {
                'name': 'status',
                'label': 'Status',
                'field': 'status'
            }
        ]

        rows = []

        for record in records:
            rows.append({
                'attendance_date': str(
                    record['attendance_date']
                ),
                'status': record['status']
            })

        ui.table(
            columns=columns,
            rows=rows,
            row_key='attendance_date'
        ).classes('w-full max-w-2xl')

    else:

        ui.label(
            'No attendance records found.'
        ).classes(
            'text-gray-500'
        )


# =========================================================
# MARK ATTENDANCE
# =========================================================

def mark_attendance(status):

    today = date.today()

    existing = execute_query(
        """
        SELECT *
        FROM attendance
        WHERE employee_id = %s
        AND attendance_date = %s
        """,
        (
            current_employee['employee_id'],
            today
        ),
        fetch=True
    )

    if existing:

        ui.notify(
            "Today's attendance is already marked.",
            type='warning'
        )

        return

    result = execute_query(
        """
        INSERT INTO attendance
        (
            employee_id,
            attendance_date,
            status
        )
        VALUES (%s, %s, %s)
        """,
        (
            current_employee['employee_id'],
            today,
            status
        )
    )

    if result:

        ui.notify(
            f'Attendance marked as {status}',
            type='positive'
        )

        ui.navigate.to('/attendance')


# =========================================================
# LEAVE APPLICATION PAGE
# =========================================================

@ui.page('/leave')
def leave_page():

    if not check_login():
        return

    page_header(
        'Leave Management',
        'Apply for leave and view your requests'
    )

    with ui.card().classes(
        'w-full max-w-2xl p-6 mb-8'
    ):

        ui.label(
            'Apply for Leave'
        ).classes(
            'text-2xl font-bold mb-4'
        )

        leave_type = ui.select(
            ['Casual Leave', 'Sick Leave', 'Earned Leave'],
            label='Leave Type'
        ).classes('w-full')

        from_date = ui.date(
            label='From Date'
        ).classes('w-full')

        to_date = ui.date(
            label='To Date'
        ).classes('w-full')

        reason = ui.textarea(
            'Reason'
        ).classes('w-full')

        ui.button(
            'Submit Leave Request',
            icon='send',
            on_click=lambda: apply_leave(
                leave_type.value,
                from_date.value,
                to_date.value,
                reason.value
            )
        ).classes('mt-4')

    ui.label(
        'Leave History'
    ).classes(
        'text-2xl font-bold mb-3'
    )

    records = execute_query(
        """
        SELECT
            leave_id,
            leave_type,
            from_date,
            to_date,
            reason,
            status
        FROM leaves
        WHERE employee_id = %s
        ORDER BY leave_id DESC
        """,
        (current_employee['employee_id'],),
        fetch=True
    )

    if records:

        columns = [
            {
                'name': 'leave_type',
                'label': 'Type',
                'field': 'leave_type'
            },
            {
                'name': 'from_date',
                'label': 'From',
                'field': 'from_date'
            },
            {
                'name': 'to_date',
                'label': 'To',
                'field': 'to_date'
            },
            {
                'name': 'reason',
                'label': 'Reason',
                'field': 'reason'
            },
            {
                'name': 'status',
                'label': 'Status',
                'field': 'status'
            }
        ]

        rows = []

        for record in records:

            rows.append({
                'leave_type': record['leave_type'],
                'from_date': str(record['from_date']),
                'to_date': str(record['to_date']),
                'reason': record['reason'],
                'status': record['status']
            })

        ui.table(
            columns=columns,
            rows=rows,
            row_key='leave_type'
        ).classes('w-full')

    else:

        ui.label(
            'No leave requests found.'
        ).classes(
            'text-gray-500'
        )


# =========================================================
# APPLY LEAVE
# =========================================================

def apply_leave(
    leave_type,
    from_date,
    to_date,
    reason
):

    if not leave_type:
        ui.notify(
            'Please select leave type',
            type='warning'
        )
        return

    if not from_date or not to_date:
        ui.notify(
            'Please select both dates',
            type='warning'
        )
        return

    if from_date > to_date:
        ui.notify(
            'From date cannot be after To date',
            type='negative'
        )
        return

    result = execute_query(
        """
        INSERT INTO leaves
        (
            employee_id,
            leave_type,
            from_date,
            to_date,
            reason,
            status
        )
        VALUES (%s, %s, %s, %s, %s, 'Pending')
        """,
        (
            current_employee['employee_id'],
            leave_type,
            from_date,
            to_date,
            reason
        )
    )

    if result:

        ui.notify(
            'Leave request submitted successfully',
            type='positive'
        )

        ui.navigate.to('/leave')


# =========================================================
# SALARY PAGE
# =========================================================

@ui.page('/salary')
def salary_page():

    if not check_login():
        return

    page_header(
        'Salary',
        'View your salary details'
    )

    records = execute_query(
        """
        SELECT
            salary_month,
            basic_salary,
            allowance,
            deduction,
            net_salary
        FROM salary
        WHERE employee_id = %s
        ORDER BY salary_id DESC
        """,
        (current_employee['employee_id'],),
        fetch=True
    )

    if records:

        # Latest salary card

        latest = records[0]

        with ui.card().classes(
            'w-full max-w-2xl p-6 mb-8'
        ):

            ui.label(
                'Latest Salary'
            ).classes(
                'text-xl font-bold'
            )

            ui.label(
                latest['salary_month']
            ).classes(
                'text-gray-500'
            )

            ui.label(
                f"₹ {latest['net_salary']}"
            ).classes(
                'text-4xl font-bold mt-2'
            )

        # Salary table

        ui.label(
            'Salary History'
        ).classes(
            'text-2xl font-bold mb-3'
        )

        columns = [
            {
                'name': 'salary_month',
                'label': 'Month',
                'field': 'salary_month'
            },
            {
                'name': 'basic_salary',
                'label': 'Basic',
                'field': 'basic_salary'
            },
            {
                'name': 'allowance',
                'label': 'Allowance',
                'field': 'allowance'
            },
            {
                'name': 'deduction',
                'label': 'Deduction',
                'field': 'deduction'
            },
            {
                'name': 'net_salary',
                'label': 'Net Salary',
                'field': 'net_salary'
            }
        ]

        rows = []

        for record in records:

            rows.append({
                'salary_month': record['salary_month'],
                'basic_salary': f"₹ {record['basic_salary']}",
                'allowance': f"₹ {record['allowance']}",
                'deduction': f"₹ {record['deduction']}",
                'net_salary': f"₹ {record['net_salary']}"
            })

        ui.table(
            columns=columns,
            rows=rows,
            row_key='salary_month'
        ).classes('w-full max-w-4xl')

    else:

        ui.label(
            'No salary records found.'
        ).classes(
            'text-gray-500'
        )


# =========================================================
# LOGIN CHECK
# =========================================================

def check_login():

    if current_employee is None:

        ui.notify(
            'Please login first',
            type='warning'
        )

        ui.navigate.to('/')

        return False

    return True


# =========================================================
# LOGOUT
# =========================================================

def logout():

    global current_employee

    current_employee = None

    ui.notify(
        'Logged out successfully',
        type='positive'
    )

    ui.navigate.to('/')


# =========================================================
# RUN APPLICATION
# =========================================================

ui.run(
    host='0.0.0.0',
    port=5000,
    title='Simple HRMS'
)