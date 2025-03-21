from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5004)
