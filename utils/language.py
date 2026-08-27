import re


def apply_mapping(text, mapping):
    """Apply word/phrase substitutions in a single, non-cascading pass.

    Longer expressions are matched first, which allows mappings such as
    ``boa noite -> olá`` or ``com você -> comigo`` without the replacement
    being transformed again by another rule in the same mapping.
    """
    if not text or not mapping:
        return text

    keys = sorted(mapping.keys(), key=lambda item: (len(item.split()), len(item)), reverse=True)
    alternatives = []
    for key in keys:
        # Spaces in JSON expressions match one or more whitespace characters.
        pattern = re.escape(key).replace(r'\ ', r'\s+')
        alternatives.append(pattern)

    regex = re.compile(r'(?<!\w)(' + '|'.join(alternatives) + r')(?!\w)', re.IGNORECASE)

    def replace(match):
        normalized_key = re.sub(r'\s+', ' ', match.group(0).lower())
        return mapping.get(normalized_key, match.group(0))

    return regex.sub(replace, text)
