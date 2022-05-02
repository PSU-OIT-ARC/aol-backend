from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from model_mommy.random_gen import gen_file_field
from model_mommy.mommy import make

from .models import Document
