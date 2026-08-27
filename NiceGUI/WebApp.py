from nicegui import ui,app

@ui.page('/')
def home():
    ui.add_css('''
    body {background-image: url("/static/aesthetic_moon.jpg");background-size: cover;background-position:top center;background-attachment: fixed;}

    ''')
    with ui.card().classes('absolute-center w-[50%] items-center').style('background-color: rgba(1, 1, 1, 0.6); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            userName = ui.input(
                label='UserName',
                placeholder='Enter your UserName',
                value="Sri"
            )

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
            )

            def login():
                print(userName.value)
                print(passWord.value)

            ui.button("Login",on_click=login)

    ui.button("Enable/Disable", on_click=enableDisableUsername)


app.add_static_files('/static','NiceGUI\static')
ui.run(port=7000)