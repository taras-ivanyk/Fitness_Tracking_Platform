# from django.http import HttpResponse
# from .models import Activity
#
# def home_page(request):
#     # 1. Get all activities from the database
#     all_activities = Activity.objects.all().order_by('-start_time')
#
#     # 2. Build an HTML string to display them
#     html = "<h1>Welcome to the Fitness Tracker</h1>"
#     html += "<h2>All Activities:</h2>"
#     html += "<ul>"
#
#     if not all_activities:
#         html += "<li>No activities found. Go create one in the admin!</li>"
#     else:
#         for act in all_activities:
#             # We use act.user.username to get the user's name
#             html += f"<li>{act.user.username} - {act.distance_m}m on {act.start_time.date()}</li>"
#
#     html += "</ul>"
#
#     # 3. Return the HTML as a web page
#     return HttpResponse(html)