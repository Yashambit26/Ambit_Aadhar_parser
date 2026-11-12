import io

from PIL import Image, ImageOps

# Small photos leave regional-script text only a few pixels tall; upscaling gives the model larger glyphs to read.
MIN_LONG_SIDE = 1600


def image_bytes(path):
    with Image.open(path) as im:
        # Phone photos are often stored sideways with an EXIF rotation flag; the model reads them best upright.
        img = ImageOps.exif_transpose(im).convert("RGB")
    scale = MIN_LONG_SIDE / max(img.size)
    if scale > 1:
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    # PNG is lossless, so re-encoding adds no compression artifacts to small text.
    img.save(buf, "PNG")
    return buf.getvalue()
