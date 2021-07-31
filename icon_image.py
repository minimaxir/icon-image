from icon_font_to_png.icon_font import IconFont
import os
from PIL import Image
from matplotlib.colors import to_rgb
import numpy as np
import fire


def gen_icon(
    icon_name: str = "fas fa-robot",
    size: int = 600,
    icon_dir: str = ".temp",
    pro_icon_path: str = None,
    pro_css_path: str = None,
):
    """
    Generates a Font Awesome icon mask from the given FA prefix + name.
    """

    # FA prefixes which map to a font file.
    font_files = {
        "fas": "fa-solid-900.ttf",
        "far": "fa-regular-400.ttf",
        "fab": "fa-brands-400.ttf",
    }

    icon_prefix = icon_name.split(" ")[0]
    icon_name_raw = icon_name.split(" ")[1]

    css_path = pro_css_path or "fontawesome.min.css"
    ttf_path = pro_icon_path or font_files[icon_prefix]

    icon = IconFont(css_file=css_path, ttf_file=ttf_path)

    # If a length and width are provided, make icon the smaller of the two
    if isinstance(size, tuple):
        size = min(size)

    icon.export_icon(
        icon=icon_name_raw[len(icon.common_prefix) :],
        size=size,
        filename="icon.png",
        export_dir=icon_dir,
    )


def color_to_rgb(color):
    """Converts a color to a RGB tuple from (0-255)."""
    if isinstance(color, tuple):
        # if a RGB tuple already
        return color
    else:
        # to_rgb() returns colors from (0-1)
        color = tuple(int(x * 255) for x in to_rgb(color))
        return color


def cli(**kwargs):
    """Entrypoint for the stylecloud CLI."""
    fire.Fire(gen_icon)


if __name__ == "__main__":
    cli()
