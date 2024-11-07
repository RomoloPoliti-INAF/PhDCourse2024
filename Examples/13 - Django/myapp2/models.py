from django.db import models

# Create your models here.
class Lavoro(models.Model):
    lavoro= models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.lavoro

class Example(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    lavoro = models.ForeignKey(Lavoro, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"
