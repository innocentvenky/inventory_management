from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from . models import Items
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
# Create your tests here.
class Item_api_testing(APITestCase):
    def setUp(self):
        self.item_1=Items.objects.create(name="ABC",description="xyz")
        self.item_2=Items.objects.create(name="EFG",description="klm")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('retriveing', kwargs={'pk': self.item_1.id}) 
    def test_1(self):
        response=self.client.post('/items/',
            {
                "name":"XYZ",
                "description":"xyz"
            },
            format="json"
        )
        self.assertEqual(response.status_code ,status.HTTP_201_CREATED)
    def test_2(self):
        reponse=self.client.get(self.url)
        self.assertEqual(reponse.status_code,status.HTTP_200_OK)
    def test_3(self):
        reponse=self.client.put(self.url,
                                {
                                    'name':"EFH",
                                    "description":"xyz"

                                },
                                format='json'

        )
        self.assertEqual(reponse.status_code,status.HTTP_200_OK)
    def test_4(self):
        reponse=self.client.delete(self.url)
        self.assertEqual(reponse.status_code,status.HTTP_204_NO_CONTENT)


