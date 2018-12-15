from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe




class Subscription(models.Model):
    your_email = models.EmailField(blank=True)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    """
        We name the new field order, and we specify that the ordering is calculated with respect to the course by setting for_fields=['course']. This means that the order
        for a new module will be assigned adding 1 to the last module of the same Course object.
    """

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)




"""
    This is the Content model. A module contains multiple contents, so we define a ForeignKey field to the Module model. We also set up a generic relation to associate
    objects from different models that represent different types of content. Remember that we need three different fields to set up a generic relationship. In our Content model, these are:
    
    • content_type: A ForeignKey field to the ContentType model
    • object_id: This is PositiveIntegerField to store the primary key of the related object
    • item: A GenericForeignKey field to the related object by combining the two previous fields
    
    Only the content_type and object_id fields have a corresponding column in the database table of this model. The item field allows you to retrieve or set the related
    object directly, and its functionality is built on top of the other two fields. We are going to use a different model for each type of content. Our content models
    will have some common fields, but they will differ in the actual contents they can store.
"""

class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    """
        We add a limit_choices_to argument to limit the ContentType objects that canbe used for the generic relationship. 
        We use the model__in field lookup to filter the query to the ContentType objects with a model attribute that is 'text', 'video','image' or, 'file'.
    """
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in':('text','video','image','file')}, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


"""
    In this code, we define an abstract model named ItemBase. Therefore, we have set abstract=True in its Meta class. In this model, we define the owner, title,
    created, and updated fields. These common fields will be used for all types of content. The owner field allows us to store which user created the content. Since
    this field is defined in an abstract class, we need different related_name for each sub-model. Django allows us to specify a placeholder for the model class name in
    the related_name attribute as %(class)s. By doing so, related_name for each child model will be generated automatically. Since we use '%(class)s_related'
    as related_name, the reverse relation for child models will be text_related, file_related, image_related, and video_related respectively.
"""
class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})


"""
    Django allows us to specify a placeholder for the model class name in the related_name attribute as %(class)s. By doing so, related_name for each
    child model will be generated automatically. Since we use '%(class)s_related' as related_name, the reverse relation for child models will be text_related,
    file_related, image_related, and video_related respectively.
    We have defined four different content models, which inherit from the ItemBase
    abstract model. These are:
    • Text: To store text content.
    • File: To store files, such as PDF.
    • Image: To store image files.
    • Video: To store videos. We use an URLField field to provide a video URL in
    order to embed it.
    Each child model contains the fields defined in the ItemBase class in addition to its own fields. A database table will be created for the Text, File, Image, and Video
models respectively. There will be no database table associated to the ItemBase model since it is an abstract model. 

"""



class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()




#A brief Note on django model inheritance
"""
Django supports model inheritance. It works in a similar way to standard class inheritance in Python. Django offers the following three options to use model
inheritance:
• Abstract models: Useful when you want to put some common information into several models. No database table is created for the abstract model.
• Multi-table model inheritance: Applicable when each model in the hierarchy is considered a complete model by itself. A database table is created for each model.
• Proxy models: Useful when you need to change the behavior of a model, for example, including additional methods, changing the default manager, 
or using different meta options. No database table is created for proxy models.

Let's take a closer look at each of them.

Abstract models
An abstract model is a base class in which you define fields you want to include in all child models. Django doesn't create any database table for abstract models. A
database table is created for each child model, including the fields inherited from the abstract class and the ones defined in the child model.
To mark a model as abstract, you need to include abstract=True in its Meta class. Django will recognize that it is an abstract model and will not create a database
table for it. To create child models, you just need to subclass the abstract model.

The following is an example of an abstract Content model and a child Text model:
from django.db import models
class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
class Text(BaseContent):
    body = models.TextField()
    
In this case, Django would create a table for the Text model only, including the
title, created, and body fields.


Multi-table model inheritance
In multi-table inheritance, each model corresponds to a database table. Django creates a OneToOneField field for the relationship in the child's model to its parent.
To use multi-table inheritance, you have to subclass an existing model. Django will create a database table for both the original model and the sub-model. 
The following example shows multi-table inheritance:

from django.db import models

class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
class Text(BaseContent):
    body = models.TextField()

Django would include an automatically generated OneToOneField field in the Text
model and create a database table for each model.


Proxy models
Proxy models are used to change the behavior of a model, for example, including additional methods or different meta options. Both models operate on the database
table of the original model. To create a proxy model, add proxy=True to the Meta class of the model.

The following example illustrates how to create a proxy model:

from django.db import models
from django.utils import timezone

class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
class OrderedContent(BaseContent):
    class Meta:
        proxy = True
        ordering = ['created']
        
    def created_delta(self):
        return timezone.now() - self.created
        
Here, we define an OrderedContent model that is a proxy model for the Content model. This model provides a default ordering for QuerySets and an additional
created_delta() method. Both models, Content and OrderedContent, operate on the same database table, and objects are accessible via the ORM through either model.
"""

