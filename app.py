from flask import Flask, jsonify, request, render_template_string
import os
import psycopg2

app = Flask(__name__)

# Configuration PostgreSQL via les variables d'environnement
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "taskdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


# Template HTML intégré pour avoir une belle interface visuelle
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>TaskMaster DevSecOps</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; background: #f4f6f9; padding: 20px; }
        .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        form { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; }
        li { background: #ecf0f1; margin: 8px 0; padding: 10px; border-radius: 5px; list-style: none; }
        .badge { background: #3498db; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 TaskMaster <span class="badge">{{ env }}</span></h1>
        <form method="POST" action="/add">
            <input type="text" name="title" placeholder="Nouvelle tâche DevOps..." required>
            <button type="submit">Ajouter</button>
        </form>
        <ul>
            {% for task in tasks %}
                <li>✅ {{ task[1] }}</li>
            {% else %}
                <li>Aucune tâche pour le moment.</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    env_name = os.getenv("APP_ENV", "local")
    try:
        init_db()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title FROM tasks ORDER BY id DESC;")
        tasks = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        tasks = [(0, "⚠️ Base PostgreSQL non connectée")]
    return render_template_string(HTML_PAGE, tasks=tasks, env=env_name)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    if title:
        init_db()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s);", (title,))
        conn.commit()
        cur.close()
        conn.close()
    return index()


# Route de Monitoring (Healthcheck) pour Docker et le Cloud !
@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)