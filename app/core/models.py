from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
class Question(models.Model):
    label = models.CharField(_('Question label'), max_length=120)
    hint_text = models.CharField(_('Question hint text'), max_length=120)



# Choices 
class ChoiceField(models.Model):
    title = models.CharField(_('Title of this choice'), max_length=120)

class MediaChoiceField(ChoiceField):
    class Meta:
        abstract = True

    # what kind of field 

class IconChoiceField(MediaChoiceField):
    pass 

class ImageChoiceField(MediaChoiceField):
    pass

class TextChoiceField(ChoiceField):
    pass 

CHOICE_FIELD_TYPES = (
    (TextChoiceField, _('Text choices')),
    (ImageChoiceField, _('Icon choices')),
    (IconChoiceField, _('Images choices')),
)


class Typology(models.Model):
    class Meta:
        abstract = True


class MultipleChoiceTypology(Typology):
    class Meta(Typology.Meta):
        pass
    choices = models.ForeignKey(ChoiceField)
    choice_field_type = models.CharField(_('Choices type'), max_length=50, choices=CHOICE_FIELD_TYPES) 
