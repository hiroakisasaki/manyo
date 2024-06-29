import MeCab
from graphviz import Digraph
import datetime
import os
import uuid

class LatticeParser:
    def __init__(self, kanji_strings, pron_sentence):
        self.kanji_strings = kanji_strings
        self.pron_sentence = pron_sentence
        self.output_file = None
        self.counter = 1

    def generate_output_filename(self):
        """
        Generate the output file name with a UUID to ensure uniqueness.
        """
        unique_id = uuid.uuid4().hex
        return f"lattice_{unique_id}"

    def parse_sentence(self):
        """Parse the sentence using MeCab and return the lattice."""
        mecab = MeCab.Tagger()
        mecab.parse('')  # Initialize the parser
        return mecab.parse(self.pron_sentence)

    def create_graph(self, lattice):
        """Create a graph using Graphviz and save it as a PNG file."""
        dot = Digraph(comment='Lattice')
        dot.attr(label=f'{self.kanji_strings} / {self.pron_sentence}', labelloc='t', fontsize='20', fontname="Noto Sans CJK JP")

        nodes = []
        for line in lattice.split('\n'):
            if line == 'EOS' or line == '':
                break
            parts = line.split('\t')
            if len(parts) == 2:
                surface, feature = parts
                nodes.append((surface, feature))

        for i, (surface, feature) in enumerate(nodes):
            dot.node(f'node_{i}', f'{surface}\n{feature}', fontname="Noto Sans CJK JP")
            if i > 0:
                dot.edge(f'node_{i-1}', f'node_{i}')

        # Generate a unique filename
        self.output_file = self.generate_output_filename()
        if self.pron_sentence == "najoidaltitabodanaistahamudda":                   # hs 20240626
            self.output_file = "ground_truth_label"                                 # hs 20240626
        if self.kanji_strings != "莫器圓鄰之大相七兄爪湯氣":                            # hs 20240626    
            self.output_file = f"non#9_{self.counter}"                              # hs 20240626
            self.counter +=1                                                        # hs 20240626

        # Render and save the graph
        dot.render(filename=self.output_file, format='png', cleanup=True)

    def process(self):
        """Main process to parse the sentence and create a graph."""
        lattice = self.parse_sentence()
        self.create_graph(lattice)

