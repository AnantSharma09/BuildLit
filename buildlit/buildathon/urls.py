from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BuildathonViewSet,
    BuildathonQuestionViewSet,
    BuildathonSubmissionViewSet,
    BuildathonJudgingViewSet,
    BuildathonWinnerView,
)

router = DefaultRouter()
router.register(r'', BuildathonViewSet, basename='buildathon')
router.register(r'questions', BuildathonQuestionViewSet, basename='buildathon-questions')
router.register(r'submissions', BuildathonSubmissionViewSet, basename='buildathon-submission')
router.register(r'judging', BuildathonJudgingViewSet, basename='buildathon-judging')

urlpatterns = [
    path('', include(router.urls)),
    path('declare-winners/<int:buildathon_id>/', BuildathonWinnerView.as_view({'post': 'create'}), name='declare-winners'),
]