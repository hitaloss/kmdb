from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ReviewChoices(models.TextChoices):
    MUST_WATCH = "Must Watch"
    SHOULD_WATCH = "Should Watch"
    AVOID_WATCH = "Avoid Watch"
    DEFAULT = "No Opinion"


class Review(models.Model):
    stars = models.PositiveIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    review = models.TextField()
    spoilers = models.BooleanField(null=True, default=False)
    recomendation = models.CharField(
        max_length=50, choices=ReviewChoices.choices, default=ReviewChoices.DEFAULT
    )

    critic = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )

    movie = models.ForeignKey(
        "movie.Movie", on_delete=models.CASCADE, related_name="reviews"
    )
