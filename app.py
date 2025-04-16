from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import string

app = Flask(__name__)
CORS(app)

# Configurações dos rotores (substituições)
ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

class EnigmaMachine:
    def __init__(self):
        self.rotors = [ROTOR_I, ROTOR_II, ROTOR_III]
        self.rotor_positions = [0, 0, 0]
        self.plugboard = {}
        self.reflector = REFLECTOR

    def set_rotor_positions(self, positions):
        self.rotor_positions = positions

    def set_plugboard(self, plugboard_pairs):
        self.plugboard = {}
        for pair in plugboard_pairs:
            if len(pair) == 2:
                self.plugboard[pair[0]] = pair[1]
                self.plugboard[pair[1]] = pair[0]

    def rotate_rotors(self):
        self.rotor_positions[0] = (self.rotor_positions[0] + 1) % 26
        if self.rotor_positions[0] == 0:
            self.rotor_positions[1] = (self.rotor_positions[1] + 1) % 26
            if self.rotor_positions[1] == 0:
                self.rotor_positions[2] = (self.rotor_positions[2] + 1) % 26

    def process_letter(self, letter):
        if not letter.isalpha():
            return letter

        letter = letter.upper()
        
        # Passa pelo plugboard
        if letter in self.plugboard:
            letter = self.plugboard[letter]

        # Passa pelos rotores (ida)
        for i in range(3):
            pos = (ord(letter) - ord('A') + self.rotor_positions[i]) % 26
            letter = self.rotors[i][pos]

        # Passa pelo reflector
        letter = self.reflector[ord(letter) - ord('A')]

        # Passa pelos rotores (volta)
        for i in range(2, -1, -1):
            pos = self.rotors[i].index(letter)
            letter = chr((pos - self.rotor_positions[i]) % 26 + ord('A'))

        # Passa pelo plugboard novamente
        if letter in self.plugboard:
            letter = self.plugboard[letter]

        return letter

    def process_text(self, text):
        result = ""
        for char in text:
            if char.isalpha():
                self.rotate_rotors()
            result += self.process_letter(char)
        return result

enigma = EnigmaMachine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '')
    rotor_positions = data.get('rotorPositions', [0, 0, 0])
    plugboard_pairs = data.get('plugboardPairs', [])

    enigma.set_rotor_positions(rotor_positions)
    enigma.set_plugboard(plugboard_pairs)

    result = enigma.process_text(text)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True) 