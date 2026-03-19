from django.db import models


class AdminReport(models.Model):
    report_type = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)
    report_data = models.JSONField()

    def __str__(self):
        return f'{self.report_type} ({self.generated_at:%Y-%m-%d})'
