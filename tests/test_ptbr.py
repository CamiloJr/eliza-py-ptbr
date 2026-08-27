import unittest

from utils.startup import setup
from utils.response import generate_response
from utils.rank import rank


class ElizaPTBRTests(unittest.TestCase):
    def setUp(self):
        self.general, self.script, self.memory_inputs, _ = setup(
            'scripts/general.json', 'scripts/doctor.json'
        )
        self.memory = []

    def respond(self, text):
        return generate_response(
            text,
            self.script,
            self.general['substitutions'],
            self.general['reflections'],
            self.memory,
            self.memory_inputs,
        )

    def test_colloquial_normalization(self):
        response = self.respond('vc ta me ouvindo')
        self.assertIn('Eliza:', response)
        self.assertIn('eu estou te ouvindo', response.lower())

    def test_sadness(self):
        response = self.respond('Eu estou triste')
        self.assertIn('triste', response.lower())
        self.assertIn('você', response.lower())

    def test_belief_reflects_possessive_without_breaking_third_person_verb(self):
        response = self.respond('Eu acho que minha mãe não gosta de mim')
        self.assertIn('sua mãe não gosta de você', response.lower())
        self.assertNotIn('não gosto de você', response.lower())

    def test_multiword_keyword(self):
        sentence, keywords = rank(
            ['Por que você não me entende?'], self.script, self.general['substitutions']
        )
        self.assertEqual(keywords[0], 'por que')
        self.assertIn('por que', sentence.lower())

    def test_help_question(self):
        response = self.respond('Você pode me ajudar?')
        self.assertTrue(
            'ajuda' in response.lower() or 'útil' in response.lower(), response
        )

    def test_possessive_noun_is_not_conjugated(self):
        response = self.respond('Meu trabalho anda difícil')
        self.assertIn('trabalho', response.lower())
        self.assertNotIn('seu trabalha', response.lower())

    def test_memory_stack(self):
        self.respond('Minha mãe me critica muito')
        self.assertTrue(self.memory)
        response = self.respond('Ontem aconteceu uma coisa estranha')
        self.assertIn('família', response.lower())

    def test_greeting_phrase(self):
        response = self.respond('boa noite')
        self.assertIn('olá', response.lower())


if __name__ == '__main__':
    unittest.main()
