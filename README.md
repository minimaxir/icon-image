# icon-image

Python script to quickly generate an icon imposed on a background, mostly intended to be used to steer the usage of a VQGAN + CLIP model generation.

## Installation

You can the dependences via:

```sh
pip3 install Pillow numpy fire icon_font_to_png
```

## Usage

The main usage is a `icon_image.py` script, which can be used to generate an icon image.

For example,

- icon_name: The Font Awesome icon name, including the `fa-` prefix. (e.g. `fab fa-apple`)
- bg_color: Background color, in text or hex.
- icon_color: Icon color, in text or hex.
- bg_noise: Whether to add uniform noise to the background. (default: `True`)
- bg_noise_opacity: The strength of the noise, in range [0, 1]. (default: `0.2`)
- bg_width: Width of the final image (default: `600`)
- bg_height: Height of the final image (default: `600`)
- icon_size: Size of the icon within the final image, which should be slightly smaller than the background. (default: `500`)

## Helpful Notes

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

_Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and [GitHub Sponsors](https://github.com/sponsors/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use._

## License

MIT

Font Awesome icon font files included per the terms in its [SIL OFL 1.1 License](https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL).
