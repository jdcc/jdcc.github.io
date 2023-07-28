from functools import partial
import re
import logging
from pathlib import Path

### This is crappy, quick templating that doesn't involve
# installing anything (like Jinja2 or whatever).
logging.basicConfig(level=logging.INFO)


TEMPLATE_PATH = Path(__file__).parent.resolve() / "templates"


def get_partials():
    """Grab all the HTML partials (fragments)

    Returns:
        dict[str, str]: name to HTML map
    """
    partials = {}
    for filename in TEMPLATE_PATH.glob("*.partial"):
        f = Path(filename)
        partials[f.stem] = f.read_text()
    return partials


def lookup_partial_from_match(match, partials):
    return partials[match.group(1)]


def fill_in_template(template, partials):
    """Fill in HTML templates with all the partial HTML

    Args:
        template (str): HTML with spaces for partials like "{{header}}".
        partials (dict[str, str]): All the HTML fragments
    """
    replace = partial(lookup_partial_from_match, partials=partials)
    return re.sub(r"{{([a-z]+)}}", replace, template)


def render():
    partials = get_partials()
    for filename in TEMPLATE_PATH.glob("**/*.html"):
        logging.info(f"Rendering {filename}")
        filled = fill_in_template(Path(filename).read_text(), partials)
        out_path = Path(filename).relative_to(TEMPLATE_PATH)
        with open(out_path, "w") as f:
            logging.info(f"Written to {out_path}")
            f.write(filled)


if __name__ == "__main__":
    render()
