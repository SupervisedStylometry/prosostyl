import regex as re

consonant = "[bcdfghjklpqrstvwxzmn]"
nasal = "[mn]"
vowel = "[aeiouyâêîôûàèùéëïü]"
all = "[bcdfghjklpqrstvwxzmnaeiouyâêîôûàèùéëïü]"

# Function to syllabify a word
def syllabify(word):
    # Step 1: Mark consonant clusters (tr, pl, etc.) to prevent splitting
    word = re.sub(r'([tbgdpkfvc])([rl])', r'\1_\2', word)  # Temporarily replace "tr" or "pl" with "t_r", "p_l", etc.
    word = re.sub(r'(g)(n)', r'\1_\2', word)  # Temporarily replace "gn" "g_n"
    # mark qu sequence
    word = re.sub(r'(q)(u)', r'\1_\2_', word)  # Temporarily replace "gn" "g_n"
    # Step 1b: preserve diphtongs
    word = re.sub(r'([aeou])(i)', r'\1_\2', word)  # Temporarily replace "oi" with "o_i"
    word = re.sub(r'([eo])(u)', r'\1_\2', word)
    word = re.sub(r'([u])(e)', r'\1_\2', word)
    word = re.sub(r'(i)([eéau])', r'\1_\2', word)  # Temporarily replace "oi" with "o_i"

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
words = ["battre", "batre", "mangier", "vëoir", "voit", "plaisir", "avoir", "dame", "chevalier",
         "mangees", "Champaigne", "cherchier", "vialt", "outree", "deïst", "quanque"]

for word in words:
    print(f"{word} -> {syllabify(word)}")


# Function to determine stress pattern for a word
def get_stress(word, next_word=None):
    syllables = syllabify(word)
    if len(syllables) == 1:  # Monosyllabic word
        return "S" if word not in ["que", "de", "le", "la", "et", "si"] else "w"
    else:
        # first, set all syllables as weak
        stress = ["w" for s in syllables]
        if syllables[-1].endswith("e"):
            stress[-2] = 'S'
            if next_word is None or re.match(r"^"+vowel, next_word):
                stress[-1] = "e"
        else:
            stress[-1] = "S"
    return "".join(stress)

# Function to process a line of verse
def process_line(verse_num, line):
    # remove punctuation
    line = re.sub(r"\p{P}", "", line)
    words = line.split()
    result = []
    for i, word in enumerate(words):
        next_word = words[i + 1] if i + 1 < len(words) else None
        stress = get_stress(word, next_word=next_word)
        result.append(stress)
    return f"{line} " + ";".join(result)

# Test function for syllabification

def syllabify_line(verse_num, line):
    #remove punctuation
    line = re.sub(r"\p{P}", "", line)
    words = line.split()
    result = []
    for i, word in enumerate(words):
        result.append("-".join(syllabify(word)))
    return ".".join(result)


# Input lines (example)
lines = [
    "Puis que ma dame de Chanpaigne",
    "Vialt que romans a feire anpraigne",
    "Je l'anprendrai mout volentiers",
    "Come cil qui est suens antiers",
    "De quanqu'il puet el monde feire",
    "Sanz rien de losange avant treire",
    "Mes tex s'an poïst antremetre",
    "Qui li volsist losenge metre",
    "Si deïst, et jel tesmoignasse",
    "Que ce est la dame qui passe"
]

# Process each line
for i, line in enumerate(lines, 1):
    print(syllabify_line(i, line))

# Process each line
for i, line in enumerate(lines, 1):
    print(process_line(i, line))