from django.db import models
from django.utils.translation import ugettext as _

from polymorphic import PolymorphicModel

# -----------------------------------------------------------------------------
# 
#     Choices field types
# 
# -----------------------------------------------------------------------------
class BaseChoiceField(PolymorphicModel):
    title = models.CharField(_('Title of this choice'), max_length=120)

class TextChoiceField(BaseChoiceField):
    pass

class MediaChoiceField(BaseChoiceField, PolymorphicModel):
    pass

class ImageChoiceField(MediaChoiceField):
    pass

class IconChoiceField(MediaChoiceField):
    pass

# -----------------------------------------------------------------------------
# 
#     Typologies
# 
# -----------------------------------------------------------------------------
class Typology(PolymorphicModel):
    pass

class BaseMultipleChoicesTypology(Typology, PolymorphicModel):
    choices = models.ManyToManyField('BaseChoiceField')

class SelectionTypology(BaseMultipleChoicesTypology):
    # multiple choices allowed
    value = models.ManyToManyField('BaseChoiceField')

class RadioTypology(BaseMultipleChoicesTypology, PolymorphicModel):
    # single value 
    value = models.ForeignKey(BaseChoiceField)

class BooleanTypology(RadioTypology):
    @classmethod
    def create(klass):
        choices  = (
            # default yes choice,
            BaseChoiceField(title=_('yes')),
            BaseChoiceField(title=_('no')),
            # default no choice
        )
        typology = klass()
        typology.choices += choices
        return typology


class Question(models.Model):
    label = models.CharField(_('Question label'), max_length=120)
    hint_text = models.CharField(_('Question hint text'), max_length=120)
    typology = models.ForeignKey(Typology)