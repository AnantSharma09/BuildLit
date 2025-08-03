from django.shortcuts import render,get_object_or_404
from .serializers import BuilderChallengeSerializer,ChallengeApplicantSerializer,ChallengeQuestionSerializer,ChallengeSubmissionSerializer,ChallengeTestCasesSerializer,ChallengeJudgingSerializer
from .models import BuilderChallenge,ChallengeApplicant,ChallengeQuestion,ChallengeSubmission,ChallengeTestCase,ChallengeJudging
from rest_framework.response import Response
from rest_framework import viewsets,generics
from rest_framework.permissions import BasePermission,IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError,PermissionDenied,NotFound
# Create your views here.

class IsBuilder(BasePermission):
      def has_permission(self,request,view):
           return hasattr(request.user,'role') and request.user.role == 'builder'
      
class BuilderChallengeViewSet(viewsets.ModelViewSet):
     queryset = BuilderChallenge.objects.all()
     serializer_class = BuilderChallengeSerializer
     permission_classes = [IsBuilder]
     
     def perform_create(self,serializer):
          serializer.save(created_by = self.request.user.profile)
          
     def get_queryset(self):
          return BuilderChallenge.objects.filter(created_by=self.request.user.profile)
     
     def perform_update(self,serializer):
          serializer.save(created_by=self.request.user.profile)
     


         
class ChallengeApplicantViewSet(viewsets.ModelViewSet):
        queryset = ChallengeApplicant.objects.all()
        serializer_class = ChallengeApplicantSerializer
        
        def get_queryset(self):
              return ChallengeApplicant.objects.filter(applicant=self.request.user.profile)
        def perform_create(self,serializer):
              serializer.save(applicant=self.request.user.profile)
         
        @action(detail=True,methods=['post'])
        def register(self,request,pk=None):
              applicant = request.user.profile
              challenge = get_object_or_404(BuilderChallenge, pk=pk)

              if applicant.role != 'joiner':
                    return Response({"detail":"Only joiners can register for challenges."})

              if ChallengeApplicant.objects.filter(applicant=applicant,challenge=challenge).exists():
                    return Response({"detail":"You have already registered for this challenge."},status=status.HTTP_400_BAD_REQUEST)
              
              if challenge.created_by == request.user.profile:
                  return Response({"detail": "You cannot register for your own challenge."}, status=400)

               
              ChallengeApplicant.objects.create(applicant=applicant, challenge=challenge)
              return Response({"detail":"Successfully registered for the challenge."},status=status.HTTP_201_CREATED)
        

class ChallengeQuestionViewSet(viewsets.ModelViewSet):
       queryset = ChallengeQuestion.objects.all()
       serializer_class = ChallengeQuestionSerializer
       permission_classes = [IsAuthenticated,IsBuilder]

class JoinerViewQuestionList(generics.ListAPIView):
      serializer_class = ChallengeQuestionSerializer
      permission_classes = [IsAuthenticated]
      def get_queryset(self):
            challenge_id = self.kwargs['challenge_id']
            return ChallengeQuestion.objects.filter(challenge_id=challenge_id)
      

class ChallengeSubmissionViewSet(viewsets.ModelViewSet):
      serializer_class = ChallengeSubmissionSerializer
      permission_classes = [IsAuthenticated]

      def perform_create(self, serializer):
        # Get the current user's application (ChallengeApplicant)
        try:
            application = ChallengeApplicant.objects.get(applicant=self.request.user.profile)
            serializer.save(application=application)
        except ChallengeApplicant.DoesNotExist:
            raise ValidationError("You are not registered for this challenge.")

      def get_queryset(self):
            # Only show the user's own submissions
          return ChallengeSubmission.objects.filter(application__applicant=self.request.user.profile)
      

class ChallengeTestCaseCreateView(generics.CreateAPIView):
     serializer_class = ChallengeTestCasesSerializer
     permission_classes = [IsAuthenticated]

     def perform_create(self,serializer):
          question_id = self.kwargs.get('question_id')
          try:
              question = ChallengeQuestion.objects.get(id=question_id)
              if question.challenge.created_by!=self.request.user:
                   raise PermissionDenied("You are not allowed to add test cases.")
              serializer.save(question=question)
          except ChallengeQuestion.DoesNotExist:
               raise NotFound("challenge question not found")
              
              
class ChallengeTestCaseListView(generics.ListAPIView):
     serializer_class=ChallengeTestCasesSerializer
     permission_classes=[IsAuthenticated]

     def get_queryset(self):
          question_id = self.kwargs['question_id']
          return ChallengeTestCase.objects.filter(question__id=question_id, is_public=True)
     

class ChallengeJudgingViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeJudgingSerializer
    permission_classes = [IsAuthenticated, IsBuilder]

    def get_queryset(self):
        return ChallengeJudging.objects.filter(judge=self.request.user.profile)

    def perform_create(self, serializer):
        submission = serializer.validated_data['submission']
        judge = self.request.user.profile

        # Prevent duplicate judging
        if ChallengeJudging.objects.filter(submission=submission, judge=judge).exists():
            raise ValidationError("You have already judged this submission.")

        # Get participant from the submission
        participant = submission.application.applicant
        serializer.save(judge=judge, participant=participant)


