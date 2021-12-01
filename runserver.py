from waitress import serve
from closet.wsgi import application as app
import werkzeug.serving

@werkzeug.serving.run_with_reloader
def run_server():
    app.debug = True
    serve(app, port='8000')

if __name__ == '__main__':
    run_server()
