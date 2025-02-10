from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, get_inventory, authenticate_user, create_user

app = Flask(__name__,
    static_folder='../frontend/static',
    template_folder='../frontend/templates')

app.secret_key = 'supersecretkey12345'

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Для доступа требуется авторизация', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
@login_required
def inventory():
    items = get_inventory()
    return render_template('inventory.html', inventory=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')
        
        user = authenticate_user(email, password, role)
        
        if user:
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            return redirect(url_for('inventory'))
        
        flash('Неверные учетные данные или роль', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('register'))
            
        if create_user(username, email, password):
            flash('Регистрация успешна! Войдите в систему', 'success')
            return redirect(url_for('login'))
        
        flash('Ошибка регистрации. Возможно email уже занят', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)