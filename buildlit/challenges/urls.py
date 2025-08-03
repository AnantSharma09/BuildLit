from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BuilderChallengeViewSet,
    ChallengeApplicantViewSet,
    ChallengeQuestionViewSet,
    JoinerViewQuestionList,
    ChallengeSubmissionViewSet,
    ChallengeTestCaseCreateView,
    ChallengeTestCaseListView,
    ChallengeJudgingViewSet,
)

router = DefaultRouter()
router.register(r'challenges', BuilderChallengeViewSet, basename='builder-challenge')
router.register(r'applicants', ChallengeApplicantViewSet, basename='challenge-applicant')
router.register(r'questions', ChallengeQuestionViewSet, basename='challenge-question')
router.register(r'submissions', ChallengeSubmissionViewSet, basename='challenge-submission')
router.register(r'judgings', ChallengeJudgingViewSet, basename='challenge-judging')

urlpatterns = [
    path('', include(router.urls)),

    # Joiner view: list of questions for a specific challenge
    path('challenges/<int:challenge_id>/questions/', JoinerViewQuestionList.as_view(), name='joiner-question-list'),

    # Test cases
    path('questions/<int:question_id>/testcases/', ChallengeTestCaseCreateView.as_view(), name='create-test-case'),
    path('questions/<int:question_id>/testcases/public/', ChallengeTestCaseListView.as_view(), name='list-public-test-cases'),
]
