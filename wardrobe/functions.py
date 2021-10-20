import time
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
from ast import literal_eval

def search_item(link):

    SAVE_FOLDER = 'staticfiles/searched'

    response = requests.get(link)
    name = 'test'

    photo = SAVE_FOLDER + '/' + name + '.png'
    with open(photo, 'wb') as file:
        file.write(response.content)

    img = Image.open(photo)
    image_bytes = BytesIO()
    img.save(image_bytes, format='PNG')


    hope = InMemoryUploadedFile(
    image_bytes, None, name, 'image/png', None, None, None
    )

    return hope
