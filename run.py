from webapp import app

if __name__ == "__main__":
    if app.config['ENV'] == "development":
        app.run(debug=True)
    elif app.config['ENV'] == "production":
        app.run(debug=True)