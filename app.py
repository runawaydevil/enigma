from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import string

app = Flask(__name__)
CORS(app)

# Configurações dos rotores (substituições e notches históricos)
ROTORS = {
    'I': {'wiring': "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'notch': 'Q'},
    'II': {'wiring': "AJDKSIRUXBLHWTMCQGZNPYFVOE", 'notch': 'E'},
    'III': {'wiring': "BDFHJLCPRTXVZNYEIWGAKMUSQO", 'notch': 'V'}
}
REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

class EnigmaMachine:
    def __init__(self, rotor_types=['I', 'II', 'III']):
        self.rotor_wirings = [ROTORS[t]['wiring'] for t in rotor_types]
        self.reverse_wirings = []
        for wiring in self.rotor_wirings:
            rev = [0] * 26
            for i, char in enumerate(wiring):
                rev[ord(char) - ord('A')] = i
            self.reverse_wirings.append(rev)

        self.notches = [ROTORS[t]['notch'] for t in rotor_types]
        self.rotor_positions = [0, 0, 0]
        self.plugboard = {}
        self.reflector = REFLECTOR

    def set_rotor_positions(self, positions):
        self.rotor_positions = [pos % 26 for pos in positions]

    def set_plugboard(self, plugboard_pairs):
        self.plugboard = {}
        for pair in plugboard_pairs:
            if len(pair) == 2:
                self.plugboard[pair[0]] = pair[1]
                self.plugboard[pair[1]] = pair[0]

    def rotate_rotors(self):
        # Enigma stepping logic with double stepping
        # Rotors are indexed: 0 (Left), 1 (Middle), 2 (Right)
        # Right rotor (2) always steps
        # Middle rotor (1) steps if Right rotor hits its notch
        # Middle rotor (1) also steps (double stepping) and steps Left rotor (0) if Middle rotor hits its notch

        r_notch = ord(self.notches[2]) - ord('A')
        m_notch = ord(self.notches[1]) - ord('A')

        step_left = False
        step_mid = False

        if self.rotor_positions[1] == m_notch:
            step_left = True
            step_mid = True
        elif self.rotor_positions[2] == r_notch:
            step_mid = True

        self.rotor_positions[2] = (self.rotor_positions[2] + 1) % 26
        if step_mid:
            self.rotor_positions[1] = (self.rotor_positions[1] + 1) % 26
        if step_left:
            self.rotor_positions[0] = (self.rotor_positions[0] + 1) % 26

    def process_letter(self, letter):
        if not letter.isalpha():
            return letter

        letter = letter.upper()
        
        # Passa pelo plugboard
        if letter in self.plugboard:
            letter = self.plugboard[letter]

        char_idx = ord(letter) - ord('A')

        # Passa pelos rotores (ida: Direita -> Esquerda)
        # self.rotor_positions[2] é o da direita
        for i in range(2, -1, -1):
            shift = self.rotor_positions[i]
            char_idx = (ord(self.rotor_wirings[i][(char_idx + shift) % 26]) - ord('A') - shift) % 26

        # Passa pelo reflector
        char_idx = (ord(self.reflector[char_idx]) - ord('A')) % 26

        # Passa pelos rotores (volta: Esquerda -> Direita)
        for i in range(3):
            shift = self.rotor_positions[i]
            target_idx = (char_idx + shift) % 26
            char_idx = (self.reverse_wirings[i][target_idx] - shift) % 26

        letter = chr(char_idx + ord('A'))

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '')
    rotor_positions = data.get('rotorPositions', [0, 0, 0])
    plugboard_pairs = data.get('plugboardPairs', [])
    rotor_types = data.get('rotorTypes', ['I', 'II', 'III'])

    # Map indices to names if they come as strings or numbers (for compatibility)
    type_map = {
        '0': 'I', 0: 'I',
        '1': 'II', 1: 'II',
        '2': 'III', 2: 'III'
    }
    resolved_types = [type_map.get(t, t) for t in rotor_types]

    # Instantiate EnigmaMachine locally for thread safety
    enigma = EnigmaMachine(resolved_types)
    enigma.set_rotor_positions(rotor_positions)
    enigma.set_plugboard(plugboard_pairs)

    result = enigma.process_text(text)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True) 