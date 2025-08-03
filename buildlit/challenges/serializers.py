from rest_framework import serializers
from .models import (
    BuilderChallenge,
    ChallengeApplicant,
    ChallengeQuestion,
    ChallengeSubmission,
    ChallengeTestCase,
    ChallengeJudging
)
from buildathon.models import BuildathonWinner
from profiles.models import Profile
from .models import BuilderChallenge


class BuilderChallengeSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=True, allow_null=False)
    is_eligible = serializers.SerializerMethodField()
    class Meta:
        model = BuilderChallenge
        fields = ['id','title','description','min_buildathon_score','created_by','required_skills']
        read_only_fields = ['created_by']
    
    def get_is_eligible(self, obj):
        # Get the current user from context (typically request.user)
        request = self.context.get('request')
        if not request or not hasattr(request.user, 'profile'):
            return False
        
        profile = request.user.profile
        return profile in obj.eligible_applicants()
    

class ChallengeApplicantSerializer(serializers.ModelSerializer):
    challenge = serializers.PrimaryKeyRelatedField(queryset=BuilderChallenge.objects.all())
    buildathon_credentials = serializers.PrimaryKeyRelatedField(
        many=True , queryset=BuildathonWinner.objects.all()
    )
    applicant = serializers.ReadOnlyField(source='applicant.id')

    class Meta:
        model = ChallengeApplicant
        fields = '__all__'
        read_only_fields = ['created_at']
        

class ChallengeQuestionSerializer(serializers.ModelSerializer):
    challenge = serializers.PrimaryKeyRelatedField(queryset = BuilderChallenge.objects.all())

    class Meta:
        model = ChallengeQuestion
        fields = '__all__'

class ChallengeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeSubmission
        fields = '__all__'
        read_only_fields = ['submitted_at']

class ChallengeTestCasesSerializer(serializers.ModelSerializer):
    question_title = serializers.ReadOnlyField(source='question.title')
    class Meta:
        model = ChallengeTestCase
        fields = '__all__'




class ChallengeJudgingSerializer(serializers.ModelSerializer):
    submission_title = serializers.ReadOnlyField(source='submission.question.title')
    participant_username = serializers.ReadOnlyField(source='participant.user.username')
    judge_username = serializers.ReadOnlyField(source='judge.user.username')

    class Meta:
        model = ChallengeJudging
        fields = [
            'id',
            'submission',
            'participant',
            'judge',
            'score',
            'created_at',
            'updated_at',
            'submission_title',
            'participant_username',
            'judge_username'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Optional: Prevent judge judging their own participant (if logic applies)
        if data['participant'] == data['judge']:
            raise serializers.ValidationError("Judge cannot evaluate their own submission.")
        return data
