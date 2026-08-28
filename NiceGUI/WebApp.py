
from nicegui import ui, app


@ui.page('/')
def home():

    ui.add_css('''
        body {
            background-image: url("/static/aesthetic_moon.jpg");
            background-size: cover;
            background-position: top center;
            background-attachment: fixed;
        }

        .white-input .q-field__label {
            color: white !important;
        }

        .white-input .q-field__native {
            color: white !important;
        }

        .white-input .q-field__control:before {
            border-bottom: 1px solid white !important;
        }

        .white-input .q-field__control:after {
            border-bottom: 2px solid white !important;
        }

        .white-input .q-field__append .q-icon {
            color: white !important;
        }

        .white-input .q-field__append .q-icon:hover {
            color: grey !important;
        }
    ''')

    with ui.card().classes(
        'absolute-center w-[50%] items-center'
    ).style(
        'background-color: rgba(1, 1, 1, 0.4); '
        'backdrop-filter: blur(1px); '
        'border-radius: 10px; '
        'box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'
    ):

        userName = ui.input(
            label='UserName',
            placeholder='Enter your UserName',
            value='Sri'
        ).classes('white-input w-full')

        def enableDisableUsername():
            if userName.enabled:
                userName.disable()
            else:
                userName.enable()

        passWord = ui.input(
            label='Password',
            placeholder='Enter your Password',
            password=True,
            password_toggle_button=True
        ).classes('white-input w-full')

        def login():
            print("Username:", userName.value)
            print("Password:", passWord.value)

        ui.button(
            "Login",
            on_click=login
        )

    ui.button(
        "Enable/Disable",
        on_click=enableDisableUsername
    )


@ui.page('/practise')
def practise():
    ui.textarea()


app.add_static_files(
    '/static',
    'NiceGUI/static'
)


ui.run(port=7000)
