SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg"}


def load_cards(input_dir):
    """Each subfolder is one card (e.g. separate front and back files); each loose file is a card on its own."""
    cards = []
    for path in sorted(input_dir.iterdir()):
        if path.is_dir():
            files = sorted(p for p in path.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)
            if files:
                cards.append((path.name, files))
        elif path.suffix.lower() in SUPPORTED_EXTENSIONS:
            cards.append((path.name, [path]))
    return cards
