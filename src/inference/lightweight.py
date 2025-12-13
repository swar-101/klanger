

def token_overlap_score(tokens, text):
    """

    :param tokens: list[str] from filename
    :param text: metadata fields : artist and title
    :return:
    """

    if not text:
        return 0.0, []

    text_tokens = [t.lower() for t in text.split()]
    overlap = set(tokens) & set(text_tokens)

    score = len(overlap) / len(text_tokens)
    return score, list(overlap)


tokens = ["daft", "punk", "harder", "better"]
artist = "Daft Punk"

score, overlap = token_overlap_score(tokens, artist)
print(score, overlap)
