


def infer_from_filename(filename):
    """
    Positional heuristics based on common human filename patterns.
    Returns artist and title candidates with medium confidence.
    :param filename:
    :return:
    """

    name = filename.lower()

    if "." in name:
        name = name.rsplit(".", 1)[0]

    artist_candidate = None
    title_candidate = None

    if "-" in name:
        left, right = name.split("-", 1)

        artist_candidate = left.strip()

        if "(" in right:
            right = right.split("(", 1)[0]

        title_candidate = right.strip()

    return {
        "artist": {
            "value": artist_candidate,
            "confidence": 0.5,
            "source": "filename_position"
        } if artist_candidate else None,

        "title": {
            "value": title_candidate,
            "confidence": 0.5,
            "source": "filename_position"
        } if title_candidate else None
    }


input = "Daft Punk - Harder Better Faster Stronger (Live Edit).mp3"
print(infer_from_filename(input))

""" 
Moving forward.. 
We can infer more candidates like something occurs inside parenthesis so 'live edit' becomes another relevant 
chunk of information, for now, we keep it simple.
"""