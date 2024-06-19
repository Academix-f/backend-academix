from django.db import models
from pgvector.django import VectorField
from AI import main

class Department(models.Model):
    head = models.OneToOneField('UserApp.MyUser', default=None, null=True, on_delete=models.SET_NULL, related_name='department_head')
    name = models.CharField(max_length = 50)
    overview = models.TextField()
    embedding = VectorField(dimensions= 768 , null = True , blank = True)

    def set_embedding(self):
        text = f"Department name: {self.name}, overview: {self.overview}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embedding()
        super().save(*args, **kwargs)

class Course(models.Model):
    name = models.CharField(max_length = 50)
    department = models.ManyToManyField(Department)
    academic_year = models.IntegerField(null=True)
    semester = models.IntegerField()
    credit_hour = models.IntegerField()
    lecture_hour = models.IntegerField()
    overview = models.TextField()
    embedding = VectorField(dimensions= 768 , null = True , blank = True)

    def set_embedding(self):
        text = f"Course name: {self.name}, overview: {self.overview}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embedding()
        super().save(*args, **kwargs)

class Building(models.Model):
    name = models.CharField()
    block_number = models.IntegerField()
    type = models.CharField(max_length = 50)
    description = models.TextField()
    embedding = VectorField(dimensions= 768 , null = True , blank = True)
    
    def set_embedding(self):
        text = f"Building name: {self.name}, Description: {self.description} , block number: {self.block_number} , type: {self.type}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embedding()
        super().save(*args, **kwargs)
    




