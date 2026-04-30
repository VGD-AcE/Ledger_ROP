#!/usr/bin/env python3
import os
import subprocess
import sys

# === Configuration ===
ENABLE_LEDGER = True  # True to enable Ledger defense; False to run without defense

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBMODBUS_DIR = os.path.join(SCRIPT_DIR, "libmodbus-2.9.3")
LIBMODBUS_LIB_DIR = os.path.join(LIBMODBUS_DIR, "src", ".libs")
SERVER_EXEC = os.path.join(LIBMODBUS_DIR, "tests", ".libs", "unit-test-server")

# GDB script & command
if ENABLE_LEDGER:
    GDB_SCRIPT = os.path.join(SCRIPT_DIR, "Ledger_cfi.py")  # Ledger mechanism script
    GDB_COMMAND = "ledgercfi"  # Command registered in GDB for Ledger
else:
    GDB_SCRIPT = os.path.join(SCRIPT_DIR, "baseline.py")
    GDB_COMMAND = "baseline"


def check_file_exists(path, description="file"):
    """Check if a file exists (skip executable permission check for scripts)."""
    if not os.path.isfile(path):
        print(f"❌ Error: {description} '{path}' does not exist.")
        sys.exit(1)


def launch_gdb_server():
    """Launch the target server under GDB with proper environment variables."""
    print("🚀 Launching GDB with Ledger CFI..." if ENABLE_LEDGER else "🚀 Launching GDB without defense...")

    # Check necessary files
    check_file_exists(SERVER_EXEC, "Server executable")
    check_file_exists(GDB_SCRIPT, "GDB script")

    # Prepare environment
    env = os.environ.copy()
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"{LIBMODBUS_LIB_DIR}:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = LIBMODBUS_LIB_DIR

    print(f"🌐 LD_LIBRARY_PATH set to: {env['LD_LIBRARY_PATH']}")
    print(f"🔗 Running: {SERVER_EXEC}")

    # GDB command
    gdb_cmd = [
        "gdb", "-q", SERVER_EXEC,
        "-ex", f"source {GDB_SCRIPT}",
        "-ex", GDB_COMMAND
    ]

    # Run GDB
    return subprocess.Popen(gdb_cmd, env=env)


def main():
    gdb_proc = launch_gdb_server()
    gdb_proc.wait()
    print("✅ Experiment completed.")


if __name__ == "__main__":
    main()
