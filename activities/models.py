from django.db import models
from django.contrib.auth.models import User
# Імпортуємо валідатори
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import F  # Потрібно для CheckConstraint


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)

    # --- ВАЛІДАЦІЯ ---
    weight_kg = models.FloatField(
        blank=True, null=True,
        validators=[MinValueValidator(0.0)]
    )
    height_cm = models.FloatField(
        blank=True, null=True,
        validators=[MinValueValidator(0.0)]
    )
    age = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(0)]
    )
    # ------------------

    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # --- ВАЛІДАЦІЯ НА РІВНІ БД ---
        constraints = [
            models.CheckConstraint(
                check=models.Q(weight_kg__gte=0),
                name='profile_weight_kg_positive'
            ),
            models.CheckConstraint(
                check=models.Q(height_cm__gte=0),
                name='profile_height_cm_positive'
            ),
            models.CheckConstraint(
                check=models.Q(age__gte=0),
                name='profile_age_positive'
            ),
        ]
        # ----------------------------

    def __str__(self):
        return self.user.username


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")

    # --- ВАЛІДАЦІЯ ---
    duration_sec = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )
    distance_m = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )
    elevation_gain_m = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    height = models.IntegerField(  # Я припускаю, що це теж не може бути від'ємним
        validators=[MinValueValidator(0)]
    )
    # ------------------

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- ВАЛІДАЦІЯ ДАТИ ---
    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time < self.start_time:
                raise ValidationError(
                    "Дата фінішу (end_time) не може бути раніше дати старту (start_time)."
                )

    # ----------------------

    def save(self, *args, **kwargs):
        self.clean()  # Викликаємо валідацію перед збереженням
        super().save(*args, **kwargs)

    class Meta:
        # --- ВАЛІДАЦІЯ НА РІВНІ БД ---
        constraints = [
            models.CheckConstraint(
                check=models.Q(duration_sec__gte=0),
                name='activity_duration_sec_positive'
            ),
            models.CheckConstraint(
                check=models.Q(distance_m__gte=0),
                name='activity_distance_m_positive'
            ),
            models.CheckConstraint(
                check=models.Q(elevation_gain_m__gte=0),
                name='activity_elevation_gain_m_positive'
            ),
            # Валідація дати на рівні БД
            models.CheckConstraint(
                check=models.Q(end_time__gte=F('start_time')),
                name='activity_end_time_gte_start_time'
            )
        ]
        # ----------------------------

    def __str__(self):
        return f"Activity by {self.user.username} on {self.start_time.date()}"


class ActivityPoint(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,
                                 related_name="points")  # ВИПРАВЛЕНО (було related_name="activity")

    lat = models.FloatField()
    lon = models.FloatField()
    recorded_at = models.DateTimeField(null=True, blank=True)

    # --- ВАЛІДАЦІЯ ---
    ele = models.FloatField(null=True, blank=True)  # Висота над рівнем моря може бути від'ємною
    speed = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0)]
    )
    cadence = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )

    # ------------------

    class Meta:
        # --- ВАЛІДАЦІЯ НА РІВНІ БД ---
        constraints = [
            models.CheckConstraint(
                check=models.Q(speed__gte=0),
                name='activitypoint_speed_positive'
            ),
            models.CheckConstraint(
                check=models.Q(cadence__gte=0),
                name='activitypoint_cadence_positive'
            ),
        ]
        # ----------------------------


class Comment(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,
                                 related_name="comments")  # ВИПРАВЛЕНО (було related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"  # ВИПРАВЛЕНО (було related_name="reply")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.activity.id}"


class Kudos(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="kudos")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kudos_given")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'user')


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')


class UserMonthlyStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="monthly_stats")
    year = models.IntegerField()
    month = models.IntegerField()

    # --- ВАЛІДАЦІЯ ---
    total_distance_m = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    total_duration_sec = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    # ------------------

    class Meta:
        unique_together = ('user', 'year', 'month')
        # --- ВАЛІДАЦІЯ НА РІВНІ БД ---
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_distance_m__gte=0),
                name='stats_distance_m_positive'
            ),
            models.CheckConstraint(
                check=models.Q(total_duration_sec__gte=0),
                name='stats_duration_sec_positive'
            ),
        ]
        # ----------------------------