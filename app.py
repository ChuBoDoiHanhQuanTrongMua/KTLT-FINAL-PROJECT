from flask import Flask, render_template
from login import login_bp
from register import register_bp

app = Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
