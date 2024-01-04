import os
from PIL import Image
from io import BytesIO

def compress_file(file: bytes) -> bytes:
    # Assuming 'file' contains the binary data of the image
    image = Image.open(BytesIO(file))

    # Compress the image with a specified quality (adjust as needed)
    compressed_image = BytesIO()
    image.save(
        compressed_image,
        format='JPEG',
        quality=int(os.getenv("IMAGE_COMPRESSION_QUALITY", 30))
    )

    # Get the compressed image content
    return compressed_image.getvalue()