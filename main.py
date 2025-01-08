import regex as re
import pandas
from Levenshtein import ratio


# List of issues
# - final -ent (that can be unstressed or stressed)
# - <ie> (diphtong, hiatus, …)

consonant = "[bcçdfghjklpqrstvwxzmn]"
nasal = "[mn]"
vowel = "[aeiouyâêîôûàèùéëïü]"
all = "[bcdfghjklpqrstvwxzmnaeiouyâêîôûàèùéëïü]"

with open("fro/of3c_atone.tsv", "r") as f:
    atone_words = [t.split('\t')[0] for t in f.readlines()]

# Function to syllabify a word
def syllabify(word):
    # Step 1: Mark consonant clusters (tr, pl, etc.) to prevent splitting
    word = re.sub(r'([tbgdpkfvc])([rl])', r'\1_\2', word)  # Temporarily replace "tr" or "pl" with "t_r", "p_l", etc.
    word = re.sub(r'(g)(n)', r'\1_\2', word)  # Temporarily replace "gn" "g_n"
    word = re.sub(r'(c)(h)', r'\1_\2', word)  # Temporarily replace "ch" "c_h"
    # mark qu sequence
    word = re.sub(r'(q)(u)', r'\1_\2_', word)  # Temporarily replace "gn" "g_n"
    ### Triphtongs
    word = re.sub(r'([ie])(a[ul])', r'\1_\2', word)  # Temporarily replace "iau"/"eau", "i_a_u"
    # Step 1b: preserve diphtongs
    word = re.sub(r'([aeou])(i)', r'\1_\2', word)  # Temporarily replace "oi" with "o_i"
    word = re.sub(r'([aeo])(u)', r'\1_\2', word)
    word = re.sub(r'(o)(e)(?=n)', r'\1_\2', word)
    word = re.sub(r'([u])(e)(?=[^n])', r'\1_\2', word) #except verbal terminaisons. Better, look for tonic syllable?
    word = re.sub(r'(i)([é])', r'\1_\2', word)  # Temporarily replace "ié" with "i_é"
    #word = re.sub(r'(?<!'+vowel+'_?)'+'(i)([e])', r'\1_\2', word)  # Temporarily replace "ie" with "i_e", if not already preceded by two wowels
    word = re.sub(r'(i)([e])(?=rs?$)', r'\1_\2', word) # suffix -ier
    word = re.sub(r'(?<=(ch|g|j))(i)([e])', r'\1_\2', word) # Bartsch law
    word = re.sub(r'(?<![_])(i)([e])(?=[nm](' + consonant + '|$))', r'\1_\2', word)  # nasal diphtong
    word = re.sub(r'(i)([e])(?=[rls]'+consonant+')', r'\1_\2', word) # North-Eastern diphtongue conditionnée par r/l/s


    # My regex:
    # first, split between consonnants
    word = re.sub("("+vowel+consonant+")"+"("+consonant+")", r'\1-\2', word)
    # then, split between vowel and vowel/consonnant that are not final
    word = re.sub("(" + vowel + ")" + "(" + consonant + ")(?=[^\-])", r'\1-\2', word)
    # then, split between vowels
    word = re.sub("(" + vowel + ")" + "(" + vowel + ")", r'\1-\2', word)

    # Step 6: Restore consonant clusters
    word = word.replace('_', '')

    # Final step, handle mute e
    word = re.sub(r'([ée])([e])', r'\1-\2', word)

    # Cleanup: Ensure there are no final syllables without vowels or empty syllables
    word = re.sub(r"\-("+consonant+"+)$", r'\1', word)
    syllables = word.split('-')
    return [s for s in syllables if s]

# Examples to test the function
# words = ["bielement", "maniere", "piece", "pieche", "iriez", "grieve", "liez", "mariage", "chastiaus", "poez", "demenoient", "boene",
#          "tierre",  "saluent", "mie", "escrie", "amie", "aie",
#          "peçoie", "salue", "battre", "batre", "mangier", "vëoir", "voit", "plaisir",
#          "avoir", "dame", "chevalier",
#          "mangees", "Champaigne", "cherchier", "vialt", "outree", "deïst", "quanque"]
#
# for word in words:
#     print(f"{word} -> {syllabify(word)}")


# Function to determine stress pattern for a word
def get_stress(word, next_word=None):
    syllables = syllabify(word)

    if len(syllables) == 1:  # Monosyllabic word
        if word in atone_words:
            return "w"
        else:
            return "S"

    else:
        # first, set all syllables as weak
        stress = ["w" for s in syllables]
        if re.match(".*es?$", syllables[-1]):
            if word not in atone_words:
                stress[-2] = 'S'
            if next_word is None:
                stress[-1] = "e" # elision at the end of the verse
            elif syllables[-1].endswith("e") and (next_word is None or re.match(r"^"+vowel, next_word)):
                stress[-1] = "e"
        else:
            if word not in atone_words:
                stress[-1] = "S"
        return "".join(stress)

# Function to process a line of verse
def process_line(line):
    # remove punctuation
    line = re.sub(r"\p{P}", "", line).lower()
    words = line.split()
    result = []
    for i, word in enumerate(words):
        next_word = words[i + 1] if i + 1 < len(words) else None
        stress = get_stress(word, next_word=next_word)
        result.append(stress)
    #return f"{line} " + ".".join(result)
    return ".".join(result)

# Test function for syllabification

def syllabify_line(line):
    #remove punctuation
    line = re.sub(r"\p{P}", "", line).lower()
    words = line.split()
    result = []
    for i, word in enumerate(words):
        result.append("-".join(syllabify(word)))
    return ".".join(result)

#
# # Input lines (example)
# lines = [
#     "Puis que ma dame de Chanpaigne",
#     "Vialt que romans a feire anpraigne",
#     "Je l'anprendrai mout volentiers",
#     "Come cil qui est suens antiers",
#     "De quanqu'il puet el monde feire",
#     "Sanz rien de losange avant treire",
#     "Mes tex s'an poïst antremetre",
#     "Qui li volsist losenge metre",
#     "Si deïst, et jel tesmoignasse",
#     "Que ce est la dame qui passe"
# ]
#
# # Process each line
# for line in lines:
#     print(syllabify_line(line))
#
# # Process each line
# for line in lines:
#     print(process_line(line))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--eval_path', action='store', help="Path to evaluation file", type=str, default='')
    parser.add_argument('--detailed_eval', action='store_true', help="Detailed evaluation results")
    parser.add_argument('--compare', action='store_true', help="Compare with alternative annotators")
    parser.add_argument('--unseen_paths', action='store', help="Paths to unseen files for prediction",
                        nargs='+',default='')
    args = parser.parse_args()

    if args.eval_path != '':
        gt = pandas.read_csv(args.eval_path, sep="\t")

        print(".... Evaluating on: " + args.eval_path + ' ....')

        lines = list(gt.Verse)
        preds = []
        for line in lines:
            preds.append(process_line(line))

        print(".... Evaluation scores ....")
        # EVAL scores
        evals = [ratio(row["Annotation"], preds[index]) for index, row in gt.iterrows()]

        print(pandas.DataFrame(evals).describe())

        if args.detailed_eval:
            # print lines where syllable counts differ
            print("... Printing lines where syllable count differ ...")
            for index, row in gt.iterrows():
                if evals[index] < 1:
                    if len(row["Annotation"]) != len(preds[index]):
                        print(
                            str(index) + row["Verse"] + " --" + row["Annotation"] + " --" + preds[index] + " -- Score: " + str(
                                evals[index]))

            print("... Printing lines with accentuation errors ...")
            # print lines with errors but same syllable count
            for index, row in gt.iterrows():
                if evals[index] < 1 and len(row["Annotation"]) == len(preds[index]):
                    print(str(index) + row["Verse"] + " --" + row["Annotation"] + " --" + preds[index] + " -- Score: " + str(evals[index]))

        if args.compare:
            print("... Comparing with other tools ...")
            cols = [col for col in gt.columns if col not in ["File", "LineNo", "Verse", "Annotation"]]

            for col in cols:
                print("... Comparing with " + col + "...")
                evals = [ratio(row["Annotation"], row[col]) for index, row in gt.iterrows()]
                print(pandas.DataFrame(evals).describe())

                if args.detailed_eval:
                    # print lines where syllable counts differ
                    print("... Printing lines where syllable count differ ...")
                    for index, row in gt.iterrows():
                        if evals[index] < 1:
                            if len(row["Annotation"]) != len(row[col]):
                                print(
                                    str(index) + row["Verse"] + " --" + row["Annotation"] + " --" + row[col] + " -- Score: " + str(
                                        evals[index]))

                    print("... Printing lines with accentuation errors ...")
                    # print lines with errors but same syllable count
                    for index, row in gt.iterrows():
                        if evals[index] < 1 and len(row["Annotation"]) == len(row[col]):
                            print(str(index) + row["Verse"] + " --" + row["Annotation"] + " --" + row[col] + " -- Score: " + str(evals[index]))

    if args.unseen_paths != '':
        for path in args.unseen_paths:
        ### Annotate unseen sample
            with open(path, 'r') as f:
                lines = f.readlines()
                lines = [line.rstrip() for line in lines if line != '']

            with open(path.split("/")[-1].split(".")[0]+'_pros.txt', 'w') as out:
                for line in lines:
                    out.write(process_line(line) + '|\n')






