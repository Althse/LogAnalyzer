from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3, os
from analyzer import DB_NAME, parse_logs, reset_database

app = Flask(__name__)

EXAMPLE_LOGS_DIR = "example_logs"

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    event_counts = {}
    cursor.execute("SELECT event_type, COUNT(*) FROM logs GROUP BY event_type")
    for row in cursor:
        event_type, count = row
        event_counts[event_type] = count

    failed_count = event_counts.get('FAILED_LOGIN', 0)
    accepted_count = event_counts.get('ACCEPTED_LOGIN', 0)

    top_ips = []
    cursor.execute(
        "SELECT ip_address, COUNT(*) FROM logs WHERE event_type='FAILED_LOGIN' "
        "GROUP BY ip_address ORDER BY COUNT(*) DESC LIMIT 5"
    )
    for row in cursor:
        ip, count = row
        top_ips.append({"ip": ip, "count": count})

    conn.close()
    return {"accepted_count": accepted_count, "failed_count": failed_count, "top_ips": top_ips}

# Home page
@app.route('/')
def index():
    stats = get_stats()
    return render_template('index.html', stats=stats)

# Upload page
@app.route('/upload_page', methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        # Upload from file
        if 'logfile' in request.files:
            file = request.files['logfile']
            if file.filename != '':
                content = file.read().decode('utf-8')
                parse_logs(log_content=content)
                return redirect(url_for('index'))
        # Upload from example log
        if 'example_file' in request.form:
            filename = request.form['example_file']
            path = os.path.join(EXAMPLE_LOGS_DIR, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    parse_logs(log_content=content)
                    return redirect(url_for('index'))

    # GET: show page
    if os.path.exists(EXAMPLE_LOGS_DIR):
        examples = os.listdir(EXAMPLE_LOGS_DIR)
    else:
        examples = []
    return render_template("upload.html", examples=examples)


# GET /reset_page – wyświetla stronę z przyciskiem
@app.route('/reset_page')
def reset_page():
    return render_template('reset.html')

# POST /reset – endpoint do resetu
@app.route('/reset', methods=['POST'])
def reset():
    reset_database()
    return jsonify({"message": "Database has been reset."})

if __name__ == "__main__":
    app.run(debug=True)
