import re

from utils.language import apply_mapping


def rank(sentences, script, substitutions):
    """Choose the sentence with the highest-ranked script keyword.

    Unlike the original eliza-py implementation, this version also supports
    multiword keywords (for example ``por que`` and ``o que``), which are
    important for idiomatic Brazilian Portuguese.
    """
    candidates = []

    for sentence_index, sentence in enumerate(sentences):
        # Keep Portuguese letters/accents; remove punctuation that should not
        # participate in matching. Apostrophes are preserved for forms like tô.
        normalized = re.sub(r'[#$%&()*+,\-./:;<=>?@[\]^_{|}~]', '', sentence)
        normalized = substitute(normalized, substitutions)
        normalized = ' '.join(normalized.split())

        if not normalized:
            continue

        matches = get_keyword_matches(normalized, script)
        max_rank = matches[0][0] if matches else 0
        candidates.append((max_rank, sentence_index, normalized, matches))

    if not candidates:
        return '', []

    # Highest rank wins; for ties, preserve the earliest sentence.
    best = max(candidates, key=lambda item: (item[0], -item[1]))
    _, _, sentence, matches = best

    # Matches are already sorted by rank desc and appearance order.
    sorted_keywords = [keyword for _, _, keyword in matches]
    return sentence, sorted_keywords


def get_keyword_matches(sentence, script):
    """Return matching script keywords as (rank, position, keyword) tuples."""
    matches = []
    lower_sentence = sentence.lower()

    for entry in script:
        keyword = entry['keyword']
        if keyword in {'$', '^'}:
            continue

        phrase_pattern = re.escape(keyword).replace(r'\ ', r'\s+')
        match = re.search(r'(?<!\w)' + phrase_pattern + r'(?!\w)', lower_sentence, re.IGNORECASE)
        if match:
            matches.append((entry['rank'], match.start(), keyword))

    matches.sort(key=lambda item: (-item[0], item[1]))
    return matches


def get_ranks(keywords, script):
    """Compatibility helper retained for users importing it directly."""
    ranks = []
    for keyword in keywords:
        for entry in script:
            if entry['keyword'] == keyword:
                ranks.append(entry['rank'])
                break
        else:
            ranks.append(0)
    return ranks


def substitute(in_str, substitutions):
    """Normalize words and phrases before keyword matching."""
    return apply_mapping(in_str, substitutions)
