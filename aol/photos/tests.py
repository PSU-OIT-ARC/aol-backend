import posixpath
import os

from django.utils.timezone import now
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings

from model_mommy.random_gen import gen_image_field
from model_mommy.mommy import make

from aol.lakes.tests import make_lake
from aol.lakes.models import NHDLake as Lake
from aol.users.tests.test_views import LoginMixin

from .models import Photo


class ModelTest(TestCase):
    def test_url(self):
        # make sure the URL path is valid
        photo = make(Photo, pk=1, file=gen_image_field())
        self.assertEqual(photo.url, "/media/photos/%s" % os.path.basename(photo.file.name))

    def test_thumbnail_url(self):
        photo = make(Photo, pk=1, file=gen_image_field())

        name = 'thumbnail-{name}'.format(name=os.path.basename(photo.file.name))
        path = os.path.join(settings.MEDIA_ROOT, 'photos', name)
        url = posixpath.join(settings.MEDIA_URL, 'photos', name)

        if os.path.exists(path):
            os.remove(path)

        self.assertEqual(photo.thumbnail_url, url)
        self.assertTrue(os.path.exists(path))

        # Now we want to make sure subsequent calls to the thumbnail_url
        # do not recreate the image (since that would be expensive).

        flag_text = 'this should not be overwritten!'
        with open(path, 'w') as f:
            f.write(flag_text)

        self.assertEqual(photo.thumbnail_url, url)
        with open(path) as f:
            self.assertEqual(f.read(), flag_text)

        os.remove(path)


class ViewTest(LoginMixin):
    def test_add_photo(self):
        (lake, geom) = make_lake(lake_kwargs={'title': "Matt Lake"})
        response = self.client.get(reverse('admin-add-photo', args=(lake.pk,)))
        self.assertEqual(response.status_code, 200)

        # test posting to the form
        data = {
            'caption': 'foo',
            'author': 'bar',
            'file': SimpleUploadedFile('image.jpg', b'fake content', content_type='image/jpeg'),
            'taken_on': '2012-12-12',
        }
        pre_count = Photo.objects.filter(lake=lake).count()
        response = self.client.post(reverse('admin-add-photo', args=(lake.pk,)), data)
        # the response should be valid, so a redirect should happen
        self.assertEqual(response.status_code, 302)
        # make sure the photo got added to the lake
        self.assertEqual(Photo.objects.filter(lake=lake).count(), pre_count + 1)

        # delete a required field to make the form invalid
        del data['caption']
        response = self.client.post(reverse('admin-add-photo', args=(lake.pk,)), data)
        self.assertFalse(response.context['form'].is_valid())

    def test_edit_photo(self):
        photo = make(Photo, pk=1, file=gen_image_field(), taken_on=now())

        response = self.client.get(reverse('admin-edit-photo', args=(photo.pk,)))
        self.assertEqual(response.status_code, 200)

        # edit the photo
        data = response.context['form'].initial
        data['caption'] = "whatever"
        response = self.client.post(reverse('admin-edit-photo', args=(photo.pk,)), data)
        # the response should be valid, so a redirect should happen
        self.assertEqual(response.status_code, 302)

        # make sure the caption got updated
        photo = Photo.objects.get(pk=1)
        self.assertEqual(photo.caption, data['caption'])
