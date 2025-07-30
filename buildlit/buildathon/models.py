from django.db import models
from profiles.models import Profile
from django.utils import timezone 
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os
from django.contrib.auth.models import get_user_model
# Create your models here.
User = get_user_model()
class Buildathon(models.Model):
    name = models.CharField(max_length=275)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_buildathons')
    is_team_based = models.BooleanField(default=False)
    max_team_size = models.IntegerField(default=4, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    registered_participants = models.ManyToManyField(User, blank=True, related_name='registered_buildathons')
    banner = models.ImageField(upload_to='buildathon_banners/', null=True, blank=True)
    category = models.CharField(max_length=100)
    @property
    def has_ended(self):
        return timezone.now()> self.end_date
    def __str__(self):
        return self.name
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class BuildathonParticipant(models.Model):
    name = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='buildathon_participants')
    buildathon = models.ForeignKey(Buildathon, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name.user.username} - {self.buildathon.name}"


from django.db import models
from django.core.exceptions import ValidationError

class BuildathonTeam(models.Model):
    buildathon = models.ForeignKey('Buildathon', on_delete=models.CASCADE, related_name='teams')
    team_name = models.CharField(max_length=100)
    team_members = models.ManyToManyField(Profile, related_name='buildathon_teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.buildathon.is_team_based:
            raise ValidationError("Teams can only be created for team-based buildathons.")
        if not self.team_name:
            raise ValidationError("Team name is required.")

    @property
    def team_size(self):
        return self.team_members.count()

    def __str__(self):
        return f"{self.team_name} - {self.buildathon.name} ({self.team_size})"

class BuildathonQuestion(models.Model):
    buildathon = models.ForeignKey(Buildathon, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    tag = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Question for {self.buildathon.name}: {self.question_text[:50]}..."



class QuestionAttachment(models.Model):
    question = models.ForeignKey(BuildathonQuestion, on_delete=models.CASCADE, related_name='attachments')
    
    file = models.FileField(
        upload_to='question_attachments/',
        validators=[FileExtensionValidator(['pdf', 'zip', 'txt'])]
    )
    image = models.ImageField(
        upload_to='question_images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Attachment for {self.question.question_text[:50]}..."
    

class BuildathonSubmission(models.Model):

    def validate_code_file(value):
        valid_extensions = ['.py', '.cpp', '.java', '.js', '.txt', '.c', '.cs', '.go', '.rb']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError(
                f"Unsupported file extension '{ext}'. Allowed types: {', '.join(valid_extensions)}."
            )

    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('js', 'JavaScript'),
        ('c', 'C'),
        ('cs', 'C#'),
        ('go', 'Go'),
        ('rb', 'Ruby'),
        ('other', 'Other'),
    ]

    participant = models.ForeignKey(
    'profiles.Profile',
    on_delete=models.CASCADE,
    related_name='buildathon_submissions'
    )

    buildathon = models.ForeignKey(
        'Buildathon',
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    question = models.ForeignKey(
        'BuildathonQuestion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submissions'
    )

    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='python'
    )

    code_text = models.TextField(
        blank=True,
        null=True,
        help_text="Paste your code here if not uploading a file."
    )

    code_file = models.FileField(
        upload_to='buildathon_submissions/code/',
        validators=[validate_code_file],
        blank=True,
        null=True,
        help_text="Upload your code file (.py, .cpp, .java, etc.)"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Make sure at least one source of code is provided
        if not self.code_text and not self.code_file:
            raise ValidationError("You must provide either code text or upload a code file.")
        
        # Make sure both are not provided at the same time
        if self.code_text and self.code_file:
            raise ValidationError("Please provide either code text or code file, not both.")

    def __str__(self):
        return f"Submission by {self.participant.user.username} | {self.buildathon.name} | {self.language}"

from django.db import models
from django.core.exceptions import ValidationError

class BuildathonJudging(models.Model):
    submission = models.ForeignKey(
        BuildathonSubmission,
        on_delete=models.CASCADE,
        related_name='judgings'
    )
    judge = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='judged_submissions'
    )
    score = models.FloatField(
        default=0,
        help_text="Score given to the submission by the judge"
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        help_text="Optional feedback from the judge"
    )
    judged_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('submission', 'judge')  # Prevent duplicate judgings from same judge

    def clean(self):
        # Optional: Validate that the judge is allowed to judge this submission
        if not self.submission.buildathon.judges.filter(id=self.judge.id).exists():
            raise ValidationError("This user is not a judge for the related buildathon.")

    def __str__(self):
        return f"Judge: {self.judge.user.username} | Submission: {self.submission.id} | Score: {self.score}"


class BuildathonWinner(models.Model):
    buildathon = models.ForeignKey(
        Buildathon,
        on_delete=models.CASCADE,
        related_name='winners'
    )
    participant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='buildathon_wins',
        help_text="Profile of the winner (individual or team member)"
    )
    team = models.ForeignKey(
        BuildathonTeam,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wins',
        help_text="Team the participant was part of, if applicable"
    )
    score = models.FloatField(
        default=0,
        help_text="Final score achieved by this winner"
    )
    won_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Time when the winner was recorded"
    )

    class Meta:
        unique_together = ('buildathon', 'participant')  # Avoid duplicate win entries for same person

    def __str__(self):
        return f"{self.participant.user.username} - Winner of {self.buildathon.name}"
