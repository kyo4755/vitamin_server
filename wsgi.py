from ServerStart import app

if __name__ == '__main__':
    from Database.database import init_db
    init_db()
    app.run(debug=True)