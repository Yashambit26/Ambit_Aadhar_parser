import io

from PIL import Image, ImageOps


def image_bytes(path):
    with Image.open(path) as im:
        # Phone photos are often stored sideways with an EXIF rotation flag; the model reads them best upright.
        img = ImageOps.exif_transpose(im).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "JPEG")
    return buf.getvalue()
