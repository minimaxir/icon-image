from icon_font_to_png.icon_font import IconFont
import os
from PIL import Image
import fire
import numpy as np


def gen_icon(
    icon_name: str = "fas fa-robot",
    icon_size: int = 500,
    icon_dir: str = ".temp",
    icon_color: str = "#7b7568",
    bg_noise: bool = True,
    bg_noise_opacity: float = 0.2,
    bg_color: tuple[int] = (255, 255, 255, 255),
    bg_width: int = 600,
    bg_height: int = 600,
    seed: int = 42,
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
    icon_bg = Image.new("RGBA", (bg_width, bg_height), bg_color)
    if bg_noise:
        if seed:
            np.random.seed(seed)
        noise = np.uint8(np.random.rand(bg_width, bg_height) * 255)
        noise_array = np.stack(
            [
                noise,
                noise,
                noise,
                np.uint8(np.full((bg_width, bg_height), 255 * bg_noise_opacity)),
            ],
            axis=2,
        )
        noise_img = Image.fromarray(
            noise_array,
            mode="RGBA",
        )
        icon_bg = Image.alpha_composite(icon_bg, noise_img)
    offset = ((bg_width - icon_size) // 2, (bg_height - icon_size) // 2)
    icon_bg.paste(icon_img, offset, icon_img)

    icon_bg.save("icon.png")


def cli(**kwargs):
    """Entrypoint for the stylecloud CLI."""
    fire.Fire(gen_icon)


if __name__ == "__main__":
    cli()
