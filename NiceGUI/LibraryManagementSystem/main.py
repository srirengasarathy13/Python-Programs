import mysql.connector
from nicegui import ui

def get_connection():
    return mysql.connector.connect(host="localhost",user="root",password="root",database="library_management")

def register_user(email,password,name,age,gender,location):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (email,password,name,age,gender,location) VALUES (%s.%s,%s,%s,%s,%s)"
    cursor.execute(query,(email,password,name,age,gender,location))
    connection.commit()
    cursor.close()
    connection.close()

def login_user(email,password):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM  users WHERE email = %s AND password = %s AND is_approved = TRUE"
    cursor.execute(query,(email,password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

@ui.page('/')
def login_page():
    with ui.column().classes('absolute-center w-96'):
        ui.label('Library Management System').classes(
            'text-2xl font-bold'
        )

        email = ui.input('Email').classes('w-full')

        password = ui.input(
            'Password',
            password=True
        ).classes('w-full')

        message = ui.label()

        def login():
            try:
                user = login_user(email.value, password.value)

                if user:
                    ui.navigate.to('/dashboard')
                else:
                    message.text = 'Invalid credentials or account not approved'
                    message.classes('text-red-500')

            except Exception as e:
                message.text = str(e)

        ui.button('Login', on_click=login).classes('w-full')

        ui.link(
            'Create Account',
            '/register'
        )


@ui.page('/register')
def register_page():
    with ui.column().classes('absolute-center w-96'):
        ui.label('Create Account').classes(
            'text-2xl font-bold'
        )

        name = ui.input('Name').classes('w-full')

        email = ui.input('Email').classes('w-full')

        password = ui.input(
            'Password',
            password=True
        ).classes('w-full')

        age = ui.number('Age').classes('w-full')

        gender = ui.select(
            ['Male', 'Female', 'Other'],
            label='Gender'
        ).classes('w-full')

        location = ui.input('Location').classes('w-full')

        message = ui.label()

        def register():
            try:
                register_user(
                    email.value,
                    password.value,
                    name.value,
                    age.value,
                    gender.value,
                    location.value
                )

                message.text = (
                    'Registration successful! '
                    'Wait for admin approval.'
                )
                message.classes('text-green-500')

            except Exception as e:
                message.text = str(e)
                message.classes('text-red-500')

        ui.button(
            'Register',
            on_click=register
        ).classes('w-full')

        ui.link(
            'Back to Login',
            '/'
        )


@ui.page('/dashboard')
def dashboard_page():
    with ui.column().classes('absolute-center items-center'):
        ui.label('📚 Library Dashboard').classes(
            'text-3xl font-bold'
        )

        ui.label('Welcome to the Library!').classes(
            'text-xl'
        )

        ui.label('This is your dummy dashboard.')

        ui.button(
            'Logout',
            on_click=lambda: ui.navigate.to('/')
        )


ui.run()