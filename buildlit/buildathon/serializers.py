from rest_framework import serializers
from .models import Buildathon, BuildathonParticipant, BuildathonTeam,BuildathonWinner,BuildathonQuestion,QuestionAttachment,BuildathonJudging,BuildathonSubmission
from profiles.models import Profile
from profiles.serializers import ProfileMiniSerializer

class BuildathonSerializer(serializers.ModelSerializer):
   class Meta:
       model = Buildathon
       fields='__all__'
       read_only_fields = ['created_at', 'updated_at']
    
class BuildathonWinnerSerializer(serializers.ModelSerializer):
    buildathon = serializers.PrimaryKeyRelatedField(queryset=Buildathon.objects.all())
    participant = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    team = serializers.PrimaryKeyRelatedField(queryset=BuildathonTeam.objects.all(), required=False, allow_null=True)

    class Meta:
        model = BuildathonWinner
        fields = ['id','buildathon','participant','team','score','won_at']
        read_only_fields = ['won_at']

class BuildathonTeamSerializer(serializers.ModelSerializer):
    buildathon = serializers.PrimaryKeyRelatedField(queryset=Buildathon.objects.all())
    team_members_detail = ProfileMiniSerializer(source='team_members', many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = BuildathonTeam
        fields = ['id', 'team_name', 'buildathon', 'team_members_detail', 'created_at']
        read_only_fields = ['created_at']
    
    def get_member_count(self, obj):
        return obj.team_members.count()
    
    def __str__(self):
     return f"{self.team_name} - {self.buildathon.title}"

class BuildathonParticipantSerializer(serializers.ModelSerializer):
    buildathon = serializers.PrimaryKeyRelatedField(queryset=Buildathon.objects.all())
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    profile_detail = ProfileMiniSerializer(source='profile', read_only=True)
    class Meta:
        model = BuildathonParticipant
        fields = ['id', 'profile','profile_detail','buildathon','joined_at']
        read_only_fields = ['joined_at']
    
    def __str__(self):
     return f"{self.profile.user.username} in {self.buildathon.title}"


class QuestionAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttachment
        fields = ['id',  'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class BuildathonQuestionSerializer(serializers.ModelSerializer):
    attachments = QuestionAttachmentSerializer(many=True, required=True)
    buildathon = serializers.PrimaryKeyRelatedField(queryset=Buildathon.objects.all())
    class Meta:
        model = BuildathonQuestion
        fields = ['id', 'buildathon', 'question_text', 'question_type', 'created_at','attachments']
        read_only_fields = ['created_at','buildathon']

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        question = BuildathonQuestion.objects.create(**validated_data)
        for attachment in attachments_data:
            QuestionAttachment.objects.create(question=question, **attachment)
        return question


class BuildathonJudgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildathonJudging
        fields = ['id', 'judge', 'submission','score', 'feedback', 'judged_at']
        read_only_fields = ['judged_at','judge']


class BuildathonSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildathonSubmission
        fields = '__all__'
        read_only_fields = ['participant', 'submitted_at']

    def validate(self, data):
        code_text = data.get('code_text')
        code_file = data.get('code_file')

        if not code_text and not code_file:
            raise serializers.ValidationError("Provide either code text or upload a file.")
        if code_text and code_file:
            raise serializers.ValidationError("Provide either code text or file, not both.")

        return data

