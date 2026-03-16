import unittest
from app import EnigmaMachine

class TestEnigmaMachine(unittest.TestCase):
    def test_reversibility(self):
        # Test that encrypting then decrypting with same settings returns original text
        machine1 = EnigmaMachine(['I', 'II', 'III'])
        machine1.set_rotor_positions([0, 0, 0])
        original_text = "HELLOENIGMA"
        encrypted = machine1.process_text(original_text)

        machine2 = EnigmaMachine(['I', 'II', 'III'])
        machine2.set_rotor_positions([0, 0, 0])
        decrypted = machine2.process_text(encrypted)

        self.assertEqual(original_text, decrypted)

    def test_different_rotors(self):
        machine1 = EnigmaMachine(['III', 'II', 'I'])
        machine1.set_rotor_positions([10, 5, 2])
        original_text = "TESTINGDYNAMICS"
        encrypted = machine1.process_text(original_text)

        machine2 = EnigmaMachine(['III', 'II', 'I'])
        machine2.set_rotor_positions([10, 5, 2])
        decrypted = machine2.process_text(encrypted)

        self.assertEqual(original_text, decrypted)

    def test_plugboard(self):
        machine = EnigmaMachine(['I', 'II', 'III'])
        machine.set_plugboard(['AB', 'CD'])
        # A should be swapped with B
        self.assertEqual(machine.plugboard['A'], 'B')
        self.assertEqual(machine.plugboard['B'], 'A')

        # Test encryption with plugboard
        machine1 = EnigmaMachine(['I', 'II', 'III'])
        machine1.set_plugboard(['AZ', 'BY'])
        machine1.set_rotor_positions([0, 0, 0])
        encrypted = machine1.process_text("AAAAA")

        machine2 = EnigmaMachine(['I', 'II', 'III'])
        machine2.set_plugboard(['AZ', 'BY'])
        machine2.set_rotor_positions([0, 0, 0])
        decrypted = machine2.process_text(encrypted)

        self.assertEqual("AAAAA", decrypted)

    def test_stepping(self):
        # Rotor III notch is V (21)
        machine = EnigmaMachine(['I', 'II', 'III'])
        # Set positions so next step hits notch V
        # Positions are Left, Mid, Right (0, 1, 2)
        machine.set_rotor_positions([0, 0, 21]) # 21 = V

        # Next step should rotate Right and Mid
        machine.process_text("A")
        self.assertEqual(machine.rotor_positions[2], 22) # W
        self.assertEqual(machine.rotor_positions[1], 1)   # B
        self.assertEqual(machine.rotor_positions[0], 0)   # A

    def test_double_stepping(self):
        # Rotor II notch is E (4)
        machine = EnigmaMachine(['I', 'II', 'III'])
        # Set positions so Mid is at its notch
        # When Mid is at notch, it steps itself and Left (double stepping)
        machine.set_rotor_positions([0, 4, 0]) # Mid at E

        machine.process_text("A")
        self.assertEqual(machine.rotor_positions[2], 1)
        self.assertEqual(machine.rotor_positions[1], 5)
        self.assertEqual(machine.rotor_positions[0], 1)

if __name__ == '__main__':
    unittest.main()
