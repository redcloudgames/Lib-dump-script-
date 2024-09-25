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

def extract_symbols(file_path, log_file):
    """Extract symbols and their offsets using nm."""
    print(f"[+] Extracting symbols from: {file_path}")
    output = run_command(['nm', '-D', file_path])
    if output:
        log_output(output, log_file)

def log_output(output, log_file):
    """Write the output to the log file."""
    with open(log_file, "a") as f:
        f.write(output + "\n")

def dump_offsets(file_path, log_file):
    """Dump function offsets and addresses."""
    print(f"[+] Dumping offsets from: {file_path}")
    output = run_command(['readelf', '-s', file_path])  # Get symbol table
    if output:
        log_output(output, log_file)

def main(lib_file_path):
    if not os.path.exists(lib_file_path):
        print(f"[-] File {lib_file_path} does not exist.")
        return

    log_file = "ue4_dump_output.txt"  # Specify the log file name
    print(f"[+] Analyzing {lib_file_path}")

    # Clear the log file at the beginning
    open(log_file, 'w').close()

    # Step 1: Extract symbols
    extract_symbols(lib_file_path, log_file)

    # Step 2: Dump offsets
    dump_offsets(lib_file_path, log_file)

    print(f"[+] Dump complete. Output saved to {log_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ue4_dumper.py <path_to_lib.so>")
        sys.exit(1)
        
    lib_file_path = sys.argv[1]  # Take the .so file path from the command-line argument
    main(lib_file_path)