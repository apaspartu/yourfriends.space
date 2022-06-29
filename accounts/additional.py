from .models import Profile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.conf import settings
import cloudinary
import cloudinary.uploader


def get_profile_photo(user):
    profile = Profile.objects.get(user=user.id)
    if profile.photo:
        profile_photo = profile.photo
    else:
        profile_photo = '/media/profile_pictures/blankprofile.png'

    return profile_photo


def save_photo(photo, profile):
    img = Image.open(photo)
    imf = img.format
    width, height = img.size
    if width > height:
        img = img.crop((0, 0, height, height))
    if height > width:
        img = img.crop((0, 0, width, width))

    buffer = BytesIO()
    img.save(fp=buffer, format=imf)
    cf = ContentFile(buffer.getvalue())

    image_field = profile.photo
    image_name = profile.user.username + f'.{imf}'

    image_field(cloudinary.uploader.upload_image(InMemoryUploadedFile(cf, None, image_name,  f'image/{imf.lower()}', cf.tell, None)))
