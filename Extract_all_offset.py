import subprocess
import os
import sys

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error running command {command}: {e}")
        return None

def extract_offsets(file_path, log_file):
    """Extract section offsets using readelf."""
    print(f"\n[+] Extracting offsets from: {file_path}")
    output = run_command(['readelf', '-S', file_path])  # Get section headers
    if output:
        print(output)
        log_output(output, log_file)

def log_output(output, log_file):
    """Write the output to the log file."""
    with open(log_file, "a") as f:
        f.write(output + "\n")

def main(so_file_path):
    if not os.path.exists(so_file_path):
        print(f"[-] File {so_file_path} does not exist.")
        return

    log_file = "offsets_output.txt"  # Specify the log file name
    print(f"[+] Analyzing {so_file_path}")

    # Clear the log file at the beginning
    open(log_file, 'w').close()

    # Extract offsets
    extract_offsets(so_file_path, log_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python x.py <path_to_file.so>")
        sys.exit(1)
        
    so_file_path = sys.argv[1]  # Take the .so file path from the command-line argument
    main(so_file_path)
