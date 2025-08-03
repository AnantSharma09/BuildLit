from django.db import models
from buildathon.models import BuildathonWinner
from profiles.models import Profile, Skills

class BuilderChallenge(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_challenges')
    title = models.CharField(max_length=255)
    description = models.TextField()
    min_buildathon_score = models.FloatField(
        default=0.0,
        help_text="Minimum score required to apply for this challenge"
    )
    required_skills = models.ManyToManyField(
        Skills,
        blank=True,
        related_name='builder_challenges',
        help_text="Skills required for this challenge"
    )

    def eligible_applicants(self):
        return Profile.objects.filter(
            buildathon_wins__score__gte=self.min_buildathon_score
        ).distinct()

    def __str__(self):
        return self.title


class ChallengeApplicant(models.Model):
    challenge = models.ForeignKey(BuilderChallenge, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    buildathon_credentials = models.ManyToManyField(BuildathonWinner, help_text="Buildathon wins that qualify this application")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.user.username} -> {self.challenge.title}"


class ChallengeQuestion(models.Model):
    challenge = models.ForeignKey(BuilderChallenge, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Problem description")
    input_format = models.TextField(blank=True, null=True)
    output_format = models.TextField(blank=True, null=True)
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=50, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium')

    def __str__(self):
        return f"{self.challenge.title} - {self.title}"
    

class ChallengeSubmission(models.Model):
    application = models.ForeignKey(ChallengeApplicant, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey(ChallengeQuestion, on_delete=models.CASCADE)
    submitted_code = models.TextField()
    language = models.CharField(max_length=50, help_text="Programming language used")
    score = models.FloatField(default=0.0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.applicant.user.username} - {self.question.title} Submission"
    
class ChallengeTestCase(models.Model):
    question = models.ForeignKey(ChallengeQuestion, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_public = models.BooleanField(default=False, help_text="Show this test case to user (like sample test)")

    def __str__(self):
        return f"TestCase for {self.question.title}"

class ChallengeJudging(models.Model):
    submission = models.ForeignKey(ChallengeSubmission, on_delete=models.CASCADE, related_name='judgings')
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='challenge_judged_submissions')
    judge = models.ForeignKey(Profile, limit_choices_to={'role': 'builder'}, on_delete=models.CASCADE, related_name='challenge_judged_by')
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_finalized = models.BooleanField(default=False)

    class Meta:
        unique_together = ('submission', 'judge')

    def save(self, *args, **kwargs):
        if not self.participant:
            self.participant = self.submission.application.applicant
        super().save(*args, **kwargs)

    def __str__(self):
        participant_name = getattr(self.participant.user, 'username', 'Unknown')
        question_title = getattr(self.submission.question, 'title', 'No Question')
        judge_name = getattr(self.judge.user, 'username', 'Unknown')
        return f"{participant_name} - {question_title} judged by {judge_name}"
