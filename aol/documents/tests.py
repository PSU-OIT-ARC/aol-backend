from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

from model_mommy.random_gen import gen_file_field
from model_mommy.mommy import make

from aol.lakes.tests import make_lake
from aol.lakes.models import NHDLake as Lake
from aol.users.tests.test_views import LoginMixin

from .models import Document


class ViewTest(LoginMixin):
    def test_add_document(self):
        (lake, geom) = make_lake(lake_kwargs={'title': "Matt Lake"})
        response = self.client.get(reverse('admin-add-document', args=(lake.pk,)))
        self.assertEqual(response.status_code, 200)

        # test posting to the form
        data = {
            'name': 'foo',
            'rank': '1',
            'file': SimpleUploadedFile('doc.pdf', b'fake content', content_type='application/pdf'),
            'type': Document.OTHER,
        }
        pre_count = Document.objects.filter(lake=lake).count()
        response = self.client.post(reverse('admin-add-document', args=(lake.pk,)), data)
        # the response should be valid, so a redirect should happen
        self.assertEqual(response.status_code, 302)
        # make sure the document got added to the lake
        self.assertEqual(Document.objects.filter(lake=lake).count(), pre_count + 1)

        # delete a required field to make the form invalid
        del data['name']
        response = self.client.post(reverse('admin-add-document', args=(lake.pk,)), data)
        self.assertFalse(response.context['form'].is_valid())

    def test_edit_document(self):
        document = make(Document, file=gen_file_field())
        response = self.client.get(reverse('admin-edit-document', args=(document.pk,)))
        self.assertEqual(response.status_code, 200)

        # edit the document
        data = response.context['form'].initial
        data['name'] = "whatever"
        response = self.client.post(reverse('admin-edit-document', args=(document.pk,)), data)
        # the response should be valid, so a redirect should happen
        self.assertEqual(response.status_code, 302)

        # make sure the caption got updated
        document = Document.objects.get(pk=document.pk)
        self.assertEqual(document.name, data['name'])
