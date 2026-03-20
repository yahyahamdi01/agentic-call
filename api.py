from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "appointments.db"

def setup_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    connection.close()

setup_database()

@app.route('/end-of-call', methods=['POST'])
def save_call_data():
    data = request.json
    
    if not data or 'appointment_date' not in data:
        return jsonify({"error": "Missing appointment_date"}), 400
        
    date = data['appointment_date']
    
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO calls (appointment_date) VALUES (?)", (date,))
        connection.commit()
        connection.close()
        
        print(f"Appointment saved for: {date}")
        return jsonify({"status": "success"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)