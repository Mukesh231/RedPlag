from django.db import models

# class FILE(models.Model):
#     file=models.FileField(blank=False, null=False)
#     def __str__(self):
#         return self.file.name

    # def save(self, *args, **kwargs):
    #     name=kwargs.pop('name',None)
    #     content=kwargs.pop('content',None)
    #     self.fields['file'].save(name, content, save=True)