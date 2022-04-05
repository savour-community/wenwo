#encoding=utf-8

from django.db import models


class BaseModelManager(models.Manager):
    def all_to_dict(self):
        queryset = self.get_queryset()
        return [obj.to_dict() for obj in queryset.all()]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class Banner(BaseModel):
    text_info = models.CharField(max_length=50, default='')
    img = models.ImageField(upload_to='banner/')
    link_url = models.URLField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.text_info

    class Meta:
        pass


class Link(BaseModel):
    name = models.CharField(max_length=20)
    linkurl = models.URLField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        pass