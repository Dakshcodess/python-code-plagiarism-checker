import re
import io
import tokenize
import keyword
import difflib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def clean_code(code):
    code = re.sub(r'#.*', '', code)
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    return "\n".join(lines)


def extract_identifiers(code):
    names = []
    try:
        token_stream = tokenize.generate_tokens(io.StringIO(code).readline)

        for toknum, tokval, _, _, _ in token_stream:
            if tokval.isidentifier() and not keyword.iskeyword(tokval):
                names.append(tokval)

    except:
        pass

    return names


def normalize_tokens(code):
    tokens = []

    try:
        token_stream = tokenize.generate_tokens(io.StringIO(code).readline)

        for toknum, tokval, _, _, _ in token_stream:

            if tokval.isidentifier() and not keyword.iskeyword(tokval):
                tokens.append("IDENTIFIER")

            elif tokval.isdigit():
                tokens.append("NUMBER")

            elif tokval.startswith(("'", '"')):
                tokens.append("STRING")

            else:
                tokens.append(tokval)

    except:
        return code

    return " ".join(tokens)


def token_similarity(code1, code2):
    docs = [code1, code2]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(docs)
    return cosine_similarity(matrix[0:1], matrix[1:2])[0][0]


def line_similarity(code1, code2):
    lines1 = code1.splitlines()
    lines2 = code2.splitlines()
    return difflib.SequenceMatcher(None, lines1, lines2).ratio()


def identifier_penalty(ids1, ids2):
    if not ids1 or not ids2:
        return 1.0

    common = len(set(ids1).intersection(set(ids2)))
    total = max(len(set(ids1).union(set(ids2))), 1)

    return common / total


def compare_python_files(file1, file2):
    raw1 = read_file(file1)
    raw2 = read_file(file2)

    code1 = clean_code(raw1)
    code2 = clean_code(raw2)

    ids1 = extract_identifiers(raw1)
    ids2 = extract_identifiers(raw2)

    norm1 = normalize_tokens(code1)
    norm2 = normalize_tokens(code2)

    score_token = token_similarity(norm1, norm2)
    score_line = line_similarity(code1, code2)
    score_ids = identifier_penalty(ids1, ids2)

    final_score = (
        score_token * 0.60 +
        score_line * 0.25 +
        score_ids * 0.15
    )

    final_score = round(final_score * 100, 2)

    return final_score


def get_risk_level(score):
    if score < 30:
        return "Low Risk"
    elif score < 70:
        return "Medium Risk"
    else:
        return "High Risk"
    import difflib


def get_matched_lines(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1:
        lines1 = f1.readlines()

    with open(file2, "r", encoding="utf-8") as f2:
        lines2 = f2.readlines()

    matcher = difflib.SequenceMatcher(None, lines1, lines2)

    matched = []

    for block in matcher.get_matching_blocks():
        a = block.a
        b = block.b
        size = block.size

        if size > 0:
            for i in range(size):
                line1 = lines1[a + i].strip()
                line2 = lines2[b + i].strip()

                if line1 and line2:
                    matched.append((line1, line2))

    return matched