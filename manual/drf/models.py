from django.db import models


class DataPoint(models.Model):
    label = models.CharField(max_length=50)
    x_coordinate = models.SmallIntegerField()
    y_coordinate = models.SmallIntegerField()


class Post(models.Model):
    body = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.body[:10]


class Task(models.Model):
    title = models.CharField(max_length=4)
    body = models.TextField()
    # image = models.ImageField(upload_to='img')
    created_at = models.DateTimeField(auto_now_add=True)


class Subtask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.PROTECT)
    content = models.CharField(max_length=128)



# Модеиль для примера сериализаторов
class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


# Модеиль для примера сериализаторов
class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    
    class Meta:
        unique_together = ['album', 'order']
        ordering = ('order',)
    
    def __str__(self) -> str:
        return f'{self.order} {self.title}'
