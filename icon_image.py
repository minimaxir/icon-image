from icon_font_to_png.icon_font import IconFont
import os
from PIL import Image
import numpy as np
import fire


def gen_icon(
    icon_name: str = "fas fa-robot",
    icon_size: int = 500,
    icon_dir: str = ".temp",
    icon_color: str = "gray",
    bg_color: tuple[int] = (255, 255, 255, 255),
    bg_width: int = 600,
    bg_height: int = 600,
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

    icon.export_icon(
        icon=icon_name_raw[len(icon.common_prefix) :],
        size=icon_size,
        color=icon_color,
        filename="icon.temp.png",
        export_dir=icon_dir,
    )

    icon_img = Image.open(os.path.join(icon_dir, "icon.temp.png"))
    icon_mask = Image.new("RGBA", (bg_width, bg_height), bg_color)
    offset = ((bg_width - icon_size) // 2, (bg_height - icon_size) // 2)
    icon_mask.paste(icon_img, offset, icon_img)

    icon_mask.save("icon.png")


def cli(**kwargs):
    """Entrypoint for the stylecloud CLI."""
    fire.Fire(gen_icon)


if __name__ == "__main__":
    cli()
