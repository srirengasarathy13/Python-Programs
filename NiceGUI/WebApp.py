from nicegui import app,run,ui

@ui.page('/')
def home():
    ui.label("Home")
    ui.button("Click",on_click=lambda:ui.navigate.to("/a"))

@ui.page('/a')
def aPage():
    ui.label("A Page") 
    ui.button("Click",on_click=lambda:ui.navigate.to("/"))
    
    
ui.run(host="0.0.0.0",port=7000)