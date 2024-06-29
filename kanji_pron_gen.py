import itertools
import datetime
import sys
import os

class KanjiPronunciationGenerator:
    def __init__(self, kanji_strings, pronunciation_dict_file):
        self.kanji_strings = kanji_strings
        self.pronunciation_dict = self.load_pronunciation_dict(pronunciation_dict_file)
        self.output_file = self.generate_output_filename()
        self.error_log_file = 'error_log_kanji.txt'  

    def load_pronunciation_dict(self, file_path):
        """
        Load the pronunciation dictionary from a file.
        Each line in the file should contain a kanji character and its readings separated by a tab.
        Example line format: 漢\tカン\tハン
        """
        pronunciation_dict = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('\t')
                kanji = parts[0]
                readings = parts[1:]
                pronunciation_dict[kanji] = readings
        return pronunciation_dict

    def generate_output_filename(self):
        """
        Generate the output file name with the current datetime and ensure it is unique.
        """
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"kanji_{now}"
        output_filename = f"{base_filename}.txt"
        
        counter = 1
        while os.path.exists(output_filename):
            output_filename = f"{base_filename}_{counter}.txt"
            counter += 1
        
        return output_filename

    def generate_pronunciations(self):
        """
        Generate all possible pronunciations for the given kanji series.
        """
        pronunciation_options = []
        for kanji in self.kanji_strings:
            if kanji not in self.pronunciation_dict:
                # Log the error and skip this kanji
                with open(self.error_log_file, 'a', encoding='utf-8') as error_log:
                    error_log.write(f"Error: Kanji '{kanji}' not found in the pronunciation dictionary.\n")
                continue
            pronunciation_options.append(self.pronunciation_dict[kanji])
        
        try:
            all_combinations = list(itertools.product(*pronunciation_options))
        except Exception as e:
            with open(self.error_log_file, 'a', encoding='utf-8') as error_log:
                error_log.write(f"Error: An unexpected error occurred while generating pronunciations: {e}\n")
            return []
        
        return all_combinations

    def write_pronunciations_to_file(self, pronunciations):
        """
        Write all pronunciation combinations to the output file.
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                for pronunciation in pronunciations:
                    file.write(''.join(pronunciation) + '\n')   # hs 20240618 Join without spaces
        except IOError as e:
            with open(self.error_log_file, 'a', encoding='utf-8') as error_log:
                error_log.write(f"Error: An I/O error occurred while writing to the file: {e}\n")

    def process(self):
        """
        The main process to generate and write the pronunciations.
        """
        try:
            self.output_file = self.generate_output_filename()
            pronunciations = self.generate_pronunciations()
            if pronunciations:
                self.write_pronunciations_to_file(pronunciations)
                return self.output_file
            else:
                with open(self.error_log_file, 'a', encoding='utf-8') as error_log:
                    error_log.write("Error: No pronunciations generated.\n")
                return None
        except KeyError as e:
            with open(self.error_log_file, 'a', encoding='utf-8') as error_log:
                error_log.write(f"{e}\n")
            return None


