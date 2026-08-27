import os

from utils.startup import setup
from utils.rules import reset_all_last_used_reassembly_rule
from utils.response import prepare_response, generate_response

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = os.path.join(PROJECT_DIR, 'scripts')
GENERAL_SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'general.json')
SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'doctor.json')


def main():
    memory_stack = []
    general_script, script, memory_inputs, exit_inputs = setup(GENERAL_SCRIPT_PATH, SCRIPT_PATH)
    substitutions = general_script.get('substitutions', {})
    reflections = general_script.get('reflections', {})

    in_str = input("Eliza: Olá. Conte-me o que está acontecendo.\nVocê: ")
    in_str_l = in_str.strip().lower()

    while in_str_l not in exit_inputs:
        # str.lower().islower() is a fast way to check whether the input
        # contains at least one alphabetic character (including accents).
        if not in_str_l.islower():
            response = prepare_response('Eliza: Por favor, escreva usando palavras para que eu possa acompanhar você.')
        elif in_str_l in {'reset', 'reiniciar', 'reinicie'}:
            reset_all_last_used_reassembly_rule(script)
            memory_stack.clear()
            response = prepare_response('Eliza: Conversa reiniciada.')
        else:
            response = generate_response(
                in_str,
                script,
                substitutions,
                reflections,
                memory_stack,
                memory_inputs,
            )

        in_str = input(response)
        in_str_l = in_str.strip().lower()

    print("Eliza: Até logo.\n")


if __name__ == "__main__":
    main()
