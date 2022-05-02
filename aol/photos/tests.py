import posixpath
import os

from django.utils.timezone import now
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

from model_mommy.random_gen import gen_image_field
from model_mommy.mommy import make

from .models import Photo
