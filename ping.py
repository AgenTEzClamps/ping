import os
import time
from ping3 import ping

def check_ping(host):
    try:
        rtt = ping(host)
        return rtt
    except Exception as e:
        return f"Error: {e}"

def log_ping(filename, ping_result):
    try:
        with open(filename, 'a') as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - {ping_result * 1000:.2f} ms\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def log_error(filename, error_message):
    try:
        with open(filename, 'a') as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - ERROR: {error_message}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def create_readme():
    readme_content = """To create the standalone executable using PyInstaller, run the following command:\n\npyinstaller --onefile ping.py"""
    with open("README.txt", "w") as readme_file:
        readme_file.write(readme_content)

if __name__ == "__main__":
    # Replace 'roblox.com' with an external server you want to ping
    target_host = 'roblox.com'
    # Specify the full path for the log files
    log_filename = os.path.join(os.path.expanduser('~'), 'ping_log.txt')
    error_log_filename = os.path.join(os.path.expanduser('~'), 'ping_error_log.txt')

    ping_count = 0
    total_ping = 0
    average_ping_count = 5  # Change this to the desired number of pings for calculating the average

    create_readme()  # Create the README file

    while True:
        try:
            ping_result = check_ping(target_host)
            if not isinstance(ping_result, str):
                print(f"Current Ping to {target_host}: {ping_result * 1000:.2f} ms")
                log_ping(log_filename, ping_result)
                ping_count += 1
                total_ping += ping_result

                if ping_count >= average_ping_count:
                    average_ping = total_ping / ping_count
                    print(f"Average Ping over {average_ping_count} pings: {average_ping * 1000:.2f} ms")
                    ping_count = 0
                    total_ping = 0
            else:
                print(f"Error: {ping_result}")
                log_error(error_log_filename, ping_result)
        except Exception as e:
            error_message = f"Exception occurred: {e}"
            print(error_message)
            log_error(error_log_filename, error_message)

        # Adjust the time interval (in seconds) based on your preference
        time.sleep(5)

    # Add the following line to prevent the window from closing immediately
    input("Press Enter to exit...")
