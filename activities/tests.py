# from django.test import TestCase
# from django.contrib.auth.models import User
# from .models import Activity
# from datetime import datetime
#
# class ActivityModelTest(TestCase):
#
#     def test_create_activity(self):
#         # 1. Setup: Create a test user
#         user = User.objects.create_user(
#             username="test_user",
#             password="test_password"
#         )
#
#         # 2. Action: Create a new activity
#         Activity.objects.create(
#             user=user,
#             duration_sec=3600,
#             distance_m=10000,
#             elevation_gain_m=150,
#             height=200,
#             start_time=datetime.now(),
#             end_time=datetime.now()
#         )
#
#         # 3. Assert: Check if the activity exists in the database
#         self.assertEqual(Activity.objects.count(), 1)
#         self.assertEqual(Activity.objects.first().user.username, "test_user")
#         self.assertEqual(Activity.objects.first().distance_m, 10000)