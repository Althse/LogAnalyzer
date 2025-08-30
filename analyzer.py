import sys
import re


def analyze_log_file(log_file_path):
    """
    Analyzes a log file to count failed login attempts and
    identify top attacking IP addresses.
    """
    # Variables to store counts for different event types
    failed_attempts = 0
    accepted_connections = 0
    ip_addresses = {}

    # Define regex patterns for different event types
    failed_pattern = re.compile(r"Failed password.*from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    accepted_pattern = re.compile(r"Accepted password.*from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                # Check for failed login attempts
                match_failed = failed_pattern.search(line)
                if match_failed:
                    failed_attempts += 1
                    ip = match_failed.group(1)
                    ip_addresses[ip] = ip_addresses.get(ip, 0) + 1

                # Check for accepted connections
                match_accepted = accepted_pattern.search(line)
                if match_accepted:
                    accepted_connections += 1

    except FileNotFoundError:
        sys.exit(f"Error: File not found: {log_file_path}")

    return failed_attempts, accepted_connections, ip_addresses


def print_summary(failed_attempts, accepted_connections, ip_addresses):
    """
    Prints the analysis summary to the console.
    """
    print("\n" + "="*40)
    print("        LOG ANALYSIS SUMMARY")
    print("="*40)
    print(f"Total failed login attempts: {failed_attempts}")
    print(f"Total accepted connections: {accepted_connections}")

    # Sort IP addresses by their occurance
    print("\nTop attacking IP addresses:")
    sorted_ips = sorted(ip_addresses.items(), key=lambda item: item[1], reverse=True)
    for ip, count in sorted_ips[:5]:  # Show only 5 top
        print(f" - {ip}: {count} attempts")

    print("="*40 + "\n")


def main():
    # Sprawdź czy użytkownik podał ścieżkę do pliku z logami jako argument.
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 analyzer.py <log_file>")

    log_file_path = sys.argv[1]

    failed, accepted, ips = analyze_log_file(log_file_path)
    print_summary(failed, accepted, ips)


if __name__ == "__main__":
    main()
