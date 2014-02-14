from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Max
from django.db.models.signals import post_save, pre_save
from rest_framework.authtoken.models import Token

from app.utils import receiver_subclasses
# all used models for signals
from app.core.models import Thematic
from app.core.models import BaseAnswer
from app.core.models import BaseChoiceField
from app.core.models import BaseFeedback
from app.core.models import BaseQuestion
from app.core.models import BooleanQuestion
from app.core.models import TextChoiceField
from app.core.models import ThematicElement
from app.core.models import UserChoiceField
from app.core.models import UserGenderQuestion
from app.core.models import UserPosition
from app.core.models import UserProfile
# -----------------------------------------------------------------------------
# 
#   Post save callback definitions and binding with django signals framework
# 
# -----------------------------------------------------------------------------
def set_max_position(obj, queryset):
    # we get the max position set, if none set it will result as 
    # position = 0
    max_pos_dict = queryset.aggregate(Max('position'))
    position = max_pos_dict['position__max']
    if position == None:
        position = 1
    else:
        position += 1
    obj.position = position

def set_element_position(sender, **kwargs):
    # on every ThematicElement.save() we will try to set the appropriate position
    if kwargs.get('instance' , False) and not kwargs.get('raw'):
        element  = kwargs['instance']
        thematic = element.thematic
        if thematic != None and not element.position:
            set_max_position(element, thematic.thematicelement_set.all())

def set_thematic_position(sender, **kwargs):
    if kwargs.get('instance' , False) and not kwargs.get('raw'):
        thematic  = kwargs['instance']
        set_max_position(thematic, Thematic.objects.all())


@receiver_subclasses(post_save, BaseQuestion, "basequestion_post_save")
@receiver_subclasses(post_save, BaseFeedback, "basefeedback_post_save")
def create_generic_element(sender, **kwargs):
    # create a generic element appropriated for feedbacks and questions 
    if kwargs.get('created', False) and not kwargs.get('raw'):
        instance = kwargs.get('instance', None)
        ctype = ContentType.objects.get_for_model(instance)
        element  = ThematicElement.objects.get_or_create(content_type=ctype, object_id=instance.pk)[0]
        element.save()


@receiver_subclasses(pre_save, BaseFeedback, "basefeedback_pre_save")
@receiver_subclasses(pre_save, BaseChoiceField, "basechoicefield_pre_save")
@receiver_subclasses(pre_save, BaseQuestion, "basequestion_pre_save")
@receiver_subclasses(pre_save, BaseAnswer,   "baseanswer_pre_save")
def assign_content_object(sender, **kwargs):
    # pre save creation of instance.content_object. Designed to ease downcasting
    # for questions, answers and feedbacks
    # import pdb; pdb.set_trace()
    instance = kwargs.get('instance', None)
    instance.content_type =  ContentType.objects.get_for_model(instance)
    


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
        for c in field.choices: 
            field = UserChoiceField(value=c[0], title= c[1], question=question)
            field.save()

def create_user_informations(sender, **kwargs):
    # will create a profile & a token for evey newly created user
    if kwargs.get('created', False) and not kwargs.get('raw'): 
        user = kwargs.get('instance')
        profile = UserProfile.objects.create(user=user)
        position = UserPosition.objects.create(user=user)
        token = Token.objects.create(user=user)
        profile.save()
        position.save()
        token.save()

def bind():
    pre_save.connect(set_element_position, sender=ThematicElement)
    pre_save.connect(set_thematic_position, sender=Thematic)
    
    # will trigger `create_boolean` after every boolean question creation
    post_save.connect(create_boolean_choices, sender=BooleanQuestion)
    post_save.connect(create_user_choice_fieds, sender=UserGenderQuestion)

    # create user information on user created
    post_save.connect(create_user_informations, sender=get_user_model())

#EOF
