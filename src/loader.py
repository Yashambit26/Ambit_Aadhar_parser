SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg"}


def load_files(input_dir):
    return sorted(p for p in input_dir.glob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)
