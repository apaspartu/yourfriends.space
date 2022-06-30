from .models import Profile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from cloudinary import CloudinaryImage
import cloudinary
import cloudinary.api
import cloudinary.uploader
from django.core.files.images import get_image_dimensions


def get_profile_photo(user):
    profile = Profile.objects.get(user=user.id)
    if profile.photo:
        profile_photo = profile.photo
    else:
        profile_photo = 'https://res.cloudinary.com/hchmalldq/image/upload/v1656533368/blankprofile_pgklet.png'

    return profile_photo


def save_photo(photo, profile):
    # img = Image.open(photo)
    # imf = img.format
    # width, height = img.size
    # if width > height:
    #     img = img.crop((0, 0, height, height))
    # if height > width:
    #     img = img.crop((0, 0, width, width))
    #
    # buffer = BytesIO()
    # img.save(fp=buffer, format=imf)
    # cf = ContentFile(buffer.getvalue())
    # image_name = profile.user.username + f'.{imf}'
    # im = cloudinary.uploader.upload(InMemoryUploadedFile(cf, None, image_name, f'image/{imf.lower()}', cf.tell, None))

    w, h = get_image_dimensions(photo)
    min_value = min(w, h)
    im = cloudinary.uploader.upload(photo, eager=f'c_crop,w_{min_value},h_{min_value}/w_200,h_200,c_scale,g_north')
    profile.photo = im['url']
    profile.save()
