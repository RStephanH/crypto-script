# crypto-script
A script for performing encryption operations using the OpenSSL command.

## For Linux

To run this program, you need to install all dependencies:

### Debian-based Systems

1. Install Python and pip:
   ```bash
   sudo apt install python3 python3-pip
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

4. Install the required module from PyPI:
   ```bash
   pip install simple-term-menu
   ```

5. Install additional utilities for better output:
   ```bash
   sudo apt install cowsay figlet
   ```

### Arch-based Systems

1. Install Python and pip:
   ```bash
   sudo pacman -S python python-pip
   ```

2. Install the required module using `yay`:
   ```bash
   yay -S python-simple-term-menu
   ```

3. Install additional utilities for better output:
   ```bash
   sudo pacman -S cowsay figlet
   ```

## Usage

1. Clone the repository:
   ```bash
   git clone https://www.github.com/RStephanH/crypto-script.git
   cd crypto-script
   ```

2. Run the script:
   ```bash
   python3 main.py
   ```

