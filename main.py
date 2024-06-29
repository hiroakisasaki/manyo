import datetime
import os
import sys
from kanji_pron_gen import KanjiPronunciationGenerator as KPG
from mecab import MeCabParser as MP
from lattice import LatticeParser  

class KanjiPronunciationGenerator:
    def __init__(self, kanji_strings):
        self.kanji_strings = kanji_strings

    def generate_pronunciations(self):
        """
        Generate pronunciations for the given kanji strings using kanji_pron_gen.py.
        """
        try:
            generator = KPG(self.kanji_strings, "kanji_pron_dict.tsv")
            output_file = generator.process()
            return output_file
        except KeyError as e:
            print(f"Error: {e}")
            return None

class ManyoProcessor:
    def __init__(self, script_file):
        self.script_file = script_file
        self.mecab_parser = MP([])

    def process_script(self):
        """
        Process each line of the given script file.
        """
        with open(self.script_file, 'r', encoding='utf-8') as file:
            for line in file:
                kanji_strings = line.strip()
                if not kanji_strings:
                    continue

                # Generate kanji pronunciations
                kanji_gen = KanjiPronunciationGenerator(kanji_strings)
                kanji_pron_file = kanji_gen.generate_pronunciations()
                if not kanji_pron_file:
                    continue

                # Read the generated kanji pronunciation file
                all_nodes = []
                with open(kanji_pron_file, 'r', encoding='utf-8') as pron_file:
                    for pron_line in pron_file:
                        pron_sentence = pron_line.strip()
                        if not pron_sentence:
                            continue

                        # Parse the sentence using MeCab
                        nodes, total_length = self.mecab_parser.parse_to_nodes(pron_sentence)
                        if not nodes:
                            continue

                        # Check if lengths match
                        if len(pron_sentence) == total_length:

                            parser = LatticeParser(kanji_strings, pron_sentence)
                            parser.process()

                        # Add nodes to the overall list for this kanji pronunciation file
                        all_nodes.extend(nodes)

                # Write all nodes for this kanji pronunciation file to a unique output file
                output_filename = self._generate_unique_filename()
                with open(output_filename, "w", encoding="utf-8") as output_file:
                    for surface, feature in all_nodes:
                        output_file.write(f"{surface}\t{feature}\n")

    def _generate_unique_filename(self):
        """
        Generate a unique filename based on the current datetime.
        """
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"nodes_{current_time}"
        output_filename = f"{base_filename}.txt"
        
        counter = 1
        while os.path.exists(output_filename):
            output_filename = f"{base_filename}_{counter}.txt"
            counter += 1
        
        return output_filename

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <script_file>")
        sys.exit(1)

    script_file = sys.argv[1]
    processor = ManyoProcessor(script_file)
    processor.process_script()
