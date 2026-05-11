from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Создаем базу данных при запуске
def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form.get('name')
    phone = request.form.get('phone')
    
    if name and phone:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO leads (name, phone) VALUES (?, ?)', (name, phone))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400
@app.route('/admin')
def admin():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    # Получаем все заявки, самые свежие — сверху
    cursor.execute('SELECT name, phone, date FROM leads ORDER BY date DESC')
    all_leads = cursor.fetchall()
    conn.close()
    return render_template('admin.html', leads=all_leads)

if __name__ == '__main__':
    init_db()
    import os
    # Берем порт, который даст Render, или 10000 по умолчанию
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


