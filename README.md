# Enigma Machine Simulator

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/yourusername/enigma-simulator)

A web-based interactive simulator of the legendary Enigma machine, developed in Python with Flask for the backend and HTML/CSS/JS for the frontend.

## Historical Context

The Enigma machine was a cipher device developed and used in the early to mid-20th century to protect commercial, diplomatic, and military communication. It was most famously used by Nazi Germany during World War II. The machine's complex encryption system, which included rotors, a plugboard, and a reflector, was considered unbreakable until a team of brilliant mathematicians and cryptanalysts at Bletchley Park, including Alan Turing, successfully cracked the code. This breakthrough is considered one of the most significant achievements in the history of cryptography and played a crucial role in the Allied victory.

## Features

- Complete simulation of the Enigma machine with rotors, plugboard, and reflector
- Responsive and intuitive interface
- Customizable rotor order and initial positions
- Configurable plugboard
- Real-time text processing
- Historical accuracy in encryption/decryption

## Requirements

- Python 3.7+
- Flask
- Flask-CORS
- python-dotenv

## Installation

1. Clone the repository:
```bash
git clone [REPOSITORY_URL]
cd enigma-simulator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Project

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## How to Use

1. Configure the rotors:
   - Select the rotor order
   - Set initial positions for each rotor

2. Configure the plugboard:
   - Enter letter pairs (e.g., AB)
   - Click "Add" to include the pair
   - Click "×" to remove a pair

3. Enter the text you want to encrypt/decrypt in the input field
4. Click "Process" to see the result

## Technical Notes

- The simulator maintains fidelity to the original Enigma machine's operation
- The same configuration used to encrypt a message must be used to decrypt it
- Non-alphabetic characters remain unchanged
- The encryption process follows the historical implementation:
  - Plugboard substitution
  - Rotor encryption (forward)
  - Reflector
  - Rotor encryption (backward)
  - Plugboard substitution

## Development

This project was developed as an educational tool to demonstrate the principles of cryptography and the historical significance of the Enigma machine. It serves both as a learning resource and a tribute to the cryptanalysts who broke the Enigma code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The original Enigma machine designers and operators
- The Bletchley Park codebreakers
- The cryptographic community for preserving this important piece of history

## Developed by

Pablo Murad - 2025 