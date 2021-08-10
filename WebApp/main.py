from website import create_app
from flaskwebgui import FlaskUI

app = create_app()
ui = FlaskUI(app, width=1024, height=640, start_server='flask')

if __name__ == '__main__':
    #app.run(debug=True)
    ui.run()
    