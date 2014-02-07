from django.contrib.contenttypes.models import ContentType
from django.db.models import Max
from django.db.models.signals import post_save, pre_save

from app.utils import receiver_subclasses
from app.core.models import BaseQuestion
from app.core.models import BaseFeedback
from app.core.models import ThematicElement
from app.core.models import TextChoiceField
from app.core.models import BooleanQuestion
from app.core.models import UserProfile
from app.core.models import UserChoiceField
from app.core.models import UserGenderQuestion
# -----------------------------------------------------------------------------
# 
#   Post save callback definitions and binding with django signals framework
# 
# -----------------------------------------------------------------------------
def set_element_position(sender, **kwargs):
    # on every ThematicElement.save() we will try to set the appropriate position
    if kwargs.get('instance' , False) and not kwargs.get('raw'):
        element  = kwargs['instance']
        thematic = element.thematic
        if thematic != None and not element.position:
            sub_elements = thematic.thematicelement_set.all()
            # we get the max position set, if none set it will result as 
            # position = 0
            max_pos_dict = sub_elements.aggregate(Max('position'))
            position = max_pos_dict['position__max']
            if position == None:
                position = 0
            else:
                position += 1
            element.position = position

@receiver_subclasses(post_save, BaseQuestion, "basequestion_post_save")
@receiver_subclasses(post_save, BaseFeedback, "basefeedback_post_save")
def create_generic_element(sender, **kwargs):
    # create a generic element appropriated 
    if kwargs.get('created', False) and not kwargs.get('raw'):
        instance = kwargs.get('instance', None)
        ctype = ContentType.objects.get_for_model(instance)
        element  = ThematicElement.objects.get_or_create(content_type=ctype, object_id=instance.pk)[0]
        element.save()

def delete_generic_element(sender, **kwargs):
    instance = kwargs.get('instance', None)
    ctype = ContentType.objects.get_for_model(instance)
    element = ThematicElement.objects.get(content_type=ctype, object_id=instance.id)
    element.delete()

def create_boolean_choices(sender, **kwargs):
    # will create default choice fields for boolean questions ("yes" and "no")
    # I must reckon that's clever.
    if kwargs.get('created', False) and not kwargs.get('raw'):
        instance = kwargs['instance']
        yes = TextChoiceField(title='yes', question=instance)
        no  = TextChoiceField(title='no', question=instance)
        yes.save()
        no.save()


def create_user_choice_fieds(sender, **kwargs):
    # will create user gender choice 
    if kwargs.get('created', False) and not kwargs.get('raw'):
        question = kwargs['instance']
        field = UserProfile._meta.get_field(question.__class__.profile_attribute)
        # import pdb; pdb.set_trace()
        for c in field.choices: 
            field = UserChoiceField(value=c[0], title= c[1], question=question)
            field.save()


def bind():
    pre_save.connect(set_element_position, sender=ThematicElement)
    # will trigger `create_boolean` after every boolean question creation
    post_save.connect(create_boolean_choices, sender=BooleanQuestion)
    post_save.connect(create_user_choice_fieds, sender=UserGenderQuestion)


#EOF
