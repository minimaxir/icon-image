from icon_font_to_png.icon_font import IconFont
import os
from PIL import Image
import fire
import numpy as np


def gen_icon(
    icon_name: str = "fas fa-robot",
    icon_size: int = 500,
    icon_width: int = None,
    icon_height: int = None,
    icon_dir: str = ".temp",
    icon_color: str = "#7b7568",
    icon_opacity: float = 1.0,
    sketch_path: str = None,
    bg_noise: bool = True,
    rainbow_noise: bool = False,
    bg_noise_opacity: float = 0.2,
    bg_color: str = "white",
    bg_width: int = 600,
    bg_height: int = 600,
    align: str = "center",
    seed: int = 42,
    pro_icon_path: str = None,
    pro_css_path: str = None,
):
    """
    Generates a Font Awesome icon mask from the given FA prefix + name.
    """

    assert align in ["center", "left", "right", "top", "bottom"], "Invalid align value."

    if sketch_path:
        icon_img = Image.open(sketch_path).convert("RGBA")
        icon_img = icon_img.resize((icon_size, icon_size), Image.ANTIALIAS)

        sketch_array = np.asarray(icon_img.convert("L")).T

        # https://stackoverflow.com/a/765829
        pixdata = icon_img.load()
        width, height = icon_img.size
        for y in range(height):
            for x in range(width):
                if sketch_array[x, y] >= 250:
                    pixdata[x, y] = (255, 255, 255, 0)
    else:
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

        icon_width = icon_width or icon_size
        icon_height = icon_height or icon_size
        if icon_width != icon_size or icon_height != icon_size:
            icon_img = icon_img.resize((icon_width, icon_height))

    if icon_opacity < 1.0:
        icon_img = Image.blend(
            Image.new("RGBA", (icon_width, icon_height), (0, 0, 0, 0)),
            icon_img,
            icon_opacity,
        )
    icon_bg = Image.new("RGBA", (bg_width, bg_height), bg_color)
    if bg_noise:
        if seed:
            np.random.seed(seed)
        if rainbow_noise:
            noise_array = np.stack(
                [
                    np.uint8(np.random.rand(bg_height, bg_width) * 255),
                    np.uint8(np.random.rand(bg_height, bg_width) * 255),
                    np.uint8(np.random.rand(bg_height, bg_width) * 255),
                    np.uint8(np.full((bg_height, bg_width), 255 * bg_noise_opacity)),
                ],
                axis=2,
            )
        else:
            noise = np.uint8(np.random.rand(bg_height, bg_width) * 255)
            noise_array = np.stack(
                [
                    noise,
                    noise,
                    noise,
                    np.uint8(np.full((bg_height, bg_width), 255 * bg_noise_opacity)),
                ],
                axis=2,
            )
        noise_img = Image.fromarray(
            noise_array,
            mode="RGBA",
        )
        icon_bg = Image.alpha_composite(icon_bg, noise_img)

    left_offset = (bg_width - icon_width) // 2
    if align == "left":
        left_offset = 0
    if align == "right":
        left_offset = bg_width - icon_width

    top_offset = (bg_height - icon_height) // 2
    if align == "top":
        top_offset = 0
    if align == "bottom":
        top_offset = bg_height - icon_height

    icon_bg.paste(icon_img, (left_offset, top_offset), icon_img)
    icon_bg.save("icon.png")


def cli(**kwargs):
    """Entrypoint for the stylecloud CLI."""
    fire.Fire(gen_icon)


if __name__ == "__main__":
    cli()
