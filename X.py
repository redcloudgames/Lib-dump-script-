import subprocess
import os
import sys

def run_command(command):
    """Run a shell command and return the output"""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error running command {command}: {e}")
        return None

def log_output(output, log_file):
    """Write the output to the log file"""
    with open(log_file, "a") as f:
        f.write(output + "\n")

def check_dependencies(file_path, log_file):
    """Check the shared library dependencies"""
    print(f"\n[+] Checking dependencies for: {file_path}")
    output = run_command(['ldd', file_path])
    if output:
        print(output)
        log_output(output, log_file)

def extract_symbols(file_path, log_file):
    """Extract symbols using nm"""
    print(f"\n[+] Extracting symbols from: {file_path}")
    output = run_command(['nm', '-D', file_path])
    if output:
        print(output)
        log_output(output, log_file)

def extract_dynamic_section(file_path, log_file):
    """Extract dynamic section using readelf"""
    print(f"\n[+] Extracting dynamic section of: {file_path}")
    output = run_command(['readelf', '-d', file_path])
    if output:
        print(output)
        log_output(output, log_file)

def disassemble(file_path, log_file):
    """Disassemble the .so file using objdump"""
    print(f"\n[+] Disassembling {file_path}")
    output = run_command(['objdump', '-d', '-S', file_path])  # -S for source interleaving
    if output:
        print(output)
        log_output(output, log_file)

def dump_sections(file_path, log_file):
    """Dump sections of the .so file using readelf"""
    print(f"\n[+] Dumping sections of: {file_path}")
    output = run_command(['readelf', '-S', file_path])
    if output:
        print(output)
        log_output(output, log_file)

def main(so_file_path):
    if not os.path.exists(so_file_path):
        print(f"[-] File {so_file_path} does not exist.")
        return

    log_file = "output.txt"  # Specify the log file name
    print(f"[+] Analyzing {so_file_path}")

    # Clear the log file at the beginning
    open(log_file, 'w').close()

    # Step 1: Check the dependencies
    check_dependencies(so_file_path, log_file)

    # Step 2: Extract symbols
    extract_symbols(so_file_path, log_file)

    # Step 3: Extract dynamic section
    extract_dynamic_section(so_file_path, log_file)

    # Step 4: Disassemble the file (for deeper analysis)
    disassemble(so_file_path, log_file)

    # Step 5: Dump sections
    dump_sections(so_file_path, log_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python x.py <path_to_file.so>")
        sys.exit(1)
        
    so_file_path = sys.argv[1]  # Take the .so file path from the command-line argument
    main(so_file_path)
