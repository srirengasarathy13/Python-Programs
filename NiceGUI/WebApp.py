from nicegui import ui


@ui.page('/Main')
def main():
    ui.label('Main Page')

    ui.button(
        'Back',
        on_click=lambda: ui.navigate.to('/'),
        icon='arrow_back'
    )


@ui.page('/')
def home():
    ui.label('Home Page')

    ui.button(
        'Next',
        on_click=lambda: ui.navigate.to('/Main'),
        color='green',
        icon='home'
    )
    with ui.card().classes('absolute-center w-[50%] items-center'):
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
                password=True
            )

            def login():
                print(userName.value)
                print(passWord.value)

            ui.button("Login",on_click=login)

    ui.button("Enable/Disable", on_click=enableDisableUsername)



ui.run(port=7000)