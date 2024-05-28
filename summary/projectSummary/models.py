from django.db import models

# Create your models here.
class ConversionResult(models.Model):
    CONVERSION_TYPES = [
        ('OCR', 'OCR'),
        ('STT', 'STT'),
        ('GPT', 'GPT'),
    ]

    conversion_type = models.CharField(max_length=3, choices=CONVERSION_TYPES)
    input_data = models.TextField()  # 변환 전 데이터
    result_data = models.TextField()  # 변환 후 데이터
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversion_type} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"