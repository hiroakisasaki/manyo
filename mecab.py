import MeCab

class MeCabParser:
    def __init__(self, args):
        # Append the --unk-feature option to the argument list
        args.append('--unk-feature=unknown')
        self.tagger = MeCab.Tagger(" ".join(args))
    
    def parse_to_nodes(self, sentence):
        """
        Parse the given sentence into nodes using MeCab.parse and update the node dictionary.
        """
        result = []
        total_length = 0
        parsed_result = self.tagger.parse(sentence)
        lines = parsed_result.splitlines()
        
        for line in lines:
            if line == "EOS":
                break
            surface, feature = line.split("\t")
            if not feature.startswith("unknown"):
                total_length += len(surface)
            result.append((surface, feature))
        
        result.append(("EOS", "EOS"))
        return result, total_length
