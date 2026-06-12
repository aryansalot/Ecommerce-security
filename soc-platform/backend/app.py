from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    if app is None:
        raise RuntimeError("create_app() returned None")
    print("Flask app initialized successfully")
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='127.0.0.1', port=5000)
