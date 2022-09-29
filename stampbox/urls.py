from django.urls import re_path
from stampbox.views import ClassificationView


urlpatterns = [
    re_path(r'^suggestion/classification', ClassificationView.as_view()),
    # re_path(r'^compare/images', MatchImages.as_view())
]
