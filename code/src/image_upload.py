from flask import send_from_directory, jsonify
import os
import re
import base64
import uuid

UPLOAD_FOLDER = "images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def upload_image(base64str: str):
    match = re.match(r'data:image/(?P<extension>[a-z]+);base64,(?P<data>.+)', base64str)
    if not match:
        return {'error': 'Invalid image data format'}

    extension = match.group('extension')
    base64_data = match.group('data')

    try:
        image_bytes = base64.b64decode(base64_data)
    except ValueError:
        return {'error': 'Invalid base64 data'}

    # Generate a unique random ID
    random_id = str(uuid.uuid4())
    filename = f"{random_id}.{extension}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save the image to the local images directory
    with open(filepath, 'wb') as f:
        f.write(image_bytes)

    # Construct the URL to access the saved image
    image_url = f"/uploads/images/{filename}"

    # Return the URL in a JSON response
    return {'url': image_url}