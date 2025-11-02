from flask import Flask
from config.database import engine, Base
from routes.web import web
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Buat tabel otomatis (kalau belum ada di DB)
Base.metadata.create_all(bind=engine)

# Daftarkan route
app.register_blueprint(web)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)