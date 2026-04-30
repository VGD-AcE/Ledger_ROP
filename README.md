
# 📝 **Ledger_ROP**

## 🛠️ **Project Structure**

This project contains the following components:

- **libmodbus-2.9.3/**: Modbus protocol stack used as the target program for demonstrating control-flow hijacking attacks.
- **leger_generate.py**: The ledger generator script. It analyzes the target binary, encrypts its control-flow metadata using the PRESENT cipher, and generates the ledger file and parameter file used by the defense.
- **Ledger_cfi.py**: The main defense script implementing the Ledger-based Control-Flow Integrity (CFI) mechanism. It verifies return-path authenticity at runtime by comparing instruction tags against pre-generated ledger values.
- **baseline.py**: The baseline script with no defense mechanisms, used to run the target program without protection for comparison.
- **automated_run.py**: Automation script for launching experiments either with or without the Ledger defense.
- **exp.py**: Exploit script used to perform a control-flow hijacking attack against the target server.
- **README.md**: This file, containing the project documentation and instructions.

## 🖥️ **Requirements**

- **Operating System**: Ubuntu 20.04 (tested)
- **GDB**: GNU Debugger, to run the target program and inject defense logic
- **Python 3**: to run the automation and attack scripts
- **32-bit GCC toolchain**: to build the target program for 32-bit architecture

## ⚙️ **Environment Setup**

On a fresh Ubuntu 20.04 system, run the following commands in order to set up the environment:

### 1️⃣ **Clone the repository**:
```bash
git clone https://github.com/hailin-creat/Ledger_ROP.git
cd Ledger_ROP
```

### 2️⃣ **Update the system**:
```bash
sudo apt update
sudo apt upgrade
```

### 3️⃣ **Install build tools**:
```bash
sudo apt install autoconf automake libtool
```

### 4️⃣ **Install 32-bit build toolchain and debug libraries**:
```bash
sudo apt install gcc-multilib g++-multilib libc6-dev-i386 make libc6-dbg
```

### 5️⃣ **Install 32-bit libc debug symbols**:
```bash
sudo apt install libc6-dbg:i386
```

### 6️⃣ **Enable i386 architecture**:
```bash
sudo dpkg --add-architecture i386
```

### 7️⃣ **Install Python dependencies**:
```bash
pip3 install lief
pip3 install pwn
```

## 🔧 **Building the Target Program**

In the project directory, navigate to `libmodbus-2.9.3/` and build the server:
```bash
cd libmodbus-2.9.3
./autogen.sh
./configure --host=i686-linux-gnu --disable-dependency-tracking CFLAGS="-m32 -fno-stack-protector -no-pie -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0 -g -O0" LDFLAGS="-m32 -no-pie -z execstack -z norelro"
make
make install
```

> **Note**: Some error messages in the compilation will not affect the experiment.

## 🛡️ **Generating the Ledger Files**

Before running the defense, generate the ledger and parameter files from the target binary:
```bash
python3 leger_generate.py ./libmodbus-2.9.3/tests/.libs/unit-test-server
```

This will produce:
- `Ledger.txt` – Encrypted ledger entries used for runtime verification
- `parameter.txt` – Encryption key and counter seed used by `Ledger_cfi.py`

These files are required for the defense to work and must match the exact binary you are testing.

## 🚀 **Running the Experiment**

1. **Enable or disable Ledger defense**  
   Edit `automated_run.py`, and set:
   ```python
   ENABLE_LEDGER = True  # Enable Ledger CFI Defense
   ENABLE_LEDGER = False  # Run without defense (baseline)
   ```

2. **Run the target under GDB**  
   From the project root directory:
   ```bash
   python3 automated_run.py
   ```
   This will:
   - Start GDB with or without Ledger defense
   - Launch the Modbus server (`unit-test-server`)
   - Wait for the attack payload (`exp.py`) to be executed

3. **Launch the attack**  
   To successfully reproduce the attack (and execute the shellcode), you need to set the correct return address in `exp.py` that points to the shellcode in memory.

   In a separate terminal window, while the server is running under GDB (launched by `automated_run.py`), execute the attack script:
   ```bash
   python3 exp.py
   ```

### 🛡️ **What Happens**

- **With Ledger Defense**:  
  The attack should be detected, and the program terminates immediately when a control-flow mismatch is found.

- **Without Defense**:  
  If the payload is correct, the attack may execute the injected shellcode.

## 🐞 **Debugging to Find the Return Address**

If you want to reproduce the attack and set the correct return address in `exp.py`, you can use GDB to precisely locate the return address on the stack and compute the memory address of the injected shellcode.

1. Start GDB and set a breakpoint in `modbus_reply`
2. When the breakpoint hits, examine the stack frame and locate the saved return address for `modbus_reply`.
3. Identify where your shellcode is placed relative to the return address.
4. Update the `ret` variable in `exp.py` to point to this address:
   ```python
   ret = p32(0xYOUR_SHELLCODE_ADDRESS)
   ```
5. Run the attack again:
   ```bash
   python3 exp.py
   ```

## 🛑 **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
