from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=20)
    id = models.CharField(primary_key=True, max_length=2)

    def __str__(self):
        return self.name;
