import sys
import re
import sqlite3
from datetime import datetime

DB_NAME = 'log_database.db'
RESET_LOG_FILE = 'reset_log.txt'


def parse_logs(log_file_path=None, log_content=None):
    """
    Parses SSH logs and stores relevant events in the database.
    Either provide log_file_path or log_content as a string.
    """
    if not log_file_path and not log_content:
        raise ValueError("Provide log_file_path or log_content.")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                user_account TEXT,
                ip_address TEXT,
                original_line TEXT
            )
        """)

        ip_pattern = r"(\d{1,3}(?:\.\d{1,3}){3}|[a-fA-F0-9:]+)"
        failed_pattern = re.compile(
            rf"Failed password for (?:invalid user\s+)?(\S+) from {ip_pattern}"
        )
        accepted_pattern = re.compile(
            rf"Accepted password for (\S+) from {ip_pattern}"
        )

        if log_content:
            lines = str(log_content).splitlines()
        else:
            assert log_file_path is not None
            with open(log_file_path) as f:
                lines = f.readlines()

        for line in lines:
            match = failed_pattern.search(line)
            if match:
                user, ip = match.groups()
                cursor.execute(
                    "INSERT INTO logs (event_type, user_account, ip_address, original_line) "
                    "VALUES (?, ?, ?, ?)",
                    ("FAILED_LOGIN", user, ip, line.strip())
                )
                continue

            match = accepted_pattern.search(line)
            if match:
                user, ip = match.groups()
                cursor.execute(
                    "INSERT INTO logs (event_type, user_account, ip_address, original_line) "
                    "VALUES (?, ?, ?, ?)",
                    ("ACCEPTED_LOGIN", user, ip, line.strip())
                )

    return f"Data from logs added into database '{DB_NAME}'."


def generate_report():
    """
    Generates a report from the logs stored in the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Count successful and failed logins
    event_counts = {}
    cursor.execute("SELECT event_type, COUNT(*) FROM logs GROUP BY event_type")
    for row in cursor:
        event_type, count = row
        event_counts[event_type] = count

    failed_count = event_counts.get('FAILED_LOGIN', 0)
    accepted_count = event_counts.get('ACCEPTED_LOGIN', 0)

    # Top 5 attacking IPs
    top_ips = []
    cursor.execute(
        "SELECT ip_address, COUNT(*) FROM logs WHERE event_type = 'FAILED_LOGIN' "
        "GROUP BY ip_address ORDER BY COUNT(*) DESC LIMIT 5"
    )
    for row in cursor:
        ip, count = row
        top_ips.append((ip, count))

    conn.close()

    report = "\n" + "=" * 40
    report += "\n        LOG ANALYSIS REPORT\n"
    report += "=" * 40 + "\n"
    report += f"Number of successful logins: {accepted_count}\n"
    report += f"Number of failed login attempts: {failed_count}\n\n"
    report += "Top 5 attacking IP addresses:\n"

    if top_ips:
        for ip, count in top_ips:
            word = "attempt" if count == 1 else "attempts"
            report += f" - {ip}: {count} {word}\n"
    else:
        report += " - No failed login attempts recorded.\n"

    report += "=" * 40 + "\n"
    return report


def reset_database():
    """
    Clears all logs from the database and records the reset in a separate file.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()

    # Write reset info to separate file
    with open(RESET_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Database reset\n")

    return f"Database has been reset. Reset logged in '{RESET_LOG_FILE}'."


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 analyzer.py <log_file> [--reset]")

    if '--reset' in sys.argv:
        print(reset_database())
    else:
        log_file_path = sys.argv[1]
        print(parse_logs(log_file_path))
        print(generate_report())


if __name__ == "__main__":
    main()
