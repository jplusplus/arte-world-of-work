from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Max
from django.db.models.signals import post_save, pre_save
from rest_framework.authtoken.models import Token

from app.utils import receiver_subclasses, clean_string
# all used models for signals
from app.core.models import Thematic
from app.core.models import StaticFeedback
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


# @receiver_subclasses(post_save, BaseQuestion, "basequestion_post_save")
# @receiver_subclasses(post_save, BaseFeedback, "basefeedback_post_save")
def create_generic_element(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if not kwargs.get('raw', False):
        ctype = ContentType.objects.get_for_model(instance)
        try:
            element = ThematicElement.objects.get(content_type=ctype, object_id=instance.pk)
        except ThematicElement.DoesNotExist:
            element = ThematicElement(content_object=instance)

        element.content_type = instance.content_type
        element.save()


# @receiver_subclasses(post_save, ThematicElement, "thematicelement_post_save")
def create_thematic_element(sender, **kwargs):
    instance = kwargs.get('instance', None)
    try:
        filters  = dict(content_type=instance.content_type, object_id=instance.object_id)
        excludes = dict(id=instance.id)

        te       = ThematicElement.objects.filter(**filters).exclude(**excludes)

        # Remove this instance if the thematic element is already        
        if len(te):
            prev_el = te[0]
            if prev_el.thematic and not instance.thematic:
                instance.delete()
            else:
                prev_el.delete()
    except ThematicElement.DoesNotExist:
        pass


@receiver_subclasses(pre_save, BaseFeedback,    "basefeedback_pre_save")
@receiver_subclasses(pre_save, BaseChoiceField, "basechoicefield_pre_save")
@receiver_subclasses(pre_save, BaseQuestion,    "basequestion_pre_save")
@receiver_subclasses(pre_save, BaseAnswer,      "baseanswer_pre_save")
def assign_content_object(sender, **kwargs):
    # pre save creation of instance.content_object. Designed to ease downcasting
    # for questions, answers and feedbacks
    instance = kwargs.get('instance', None)
    if not kwargs.get('raw', False):
        instance.content_type =  ContentType.objects.get_for_model(instance)

def create_boolean_choices(sender, **kwargs):
    # will create default choice fields for boolean questions ("yes" and "no")
    # I must reckon that's clever.
    if kwargs.get('created', False) and not kwargs.get('raw'):
        instance = kwargs['instance']
        yes = TextChoiceField(title='yes', question=instance, position=1)
        no  = TextChoiceField(title='no',  question=instance, position=2)
        yes.save()
        no.save()


def create_user_choice_fields(sender, **kwargs):
    # will create user gender choice 
    if kwargs.get('created', False) and not kwargs.get('raw'):
        question = kwargs['instance']
        field = UserProfile._meta.get_field(question.__class__.profile_attribute)
        position = 1
        for c in field.choices:
            field = UserChoiceField(value=c[0], title=c[1], question=question, position=position)
            field.save()
            position += 1

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


def clean_thematic(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.intro_description = clean_string(instance.intro_description)
    instance.outro_description = clean_string(instance.outro_description)


def clean_feedback(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.html_sentence = clean_string(instance.html_sentence)




def bind():
    pre_save.connect(set_element_position, sender=ThematicElement)    
    # pre_save.connect(set_thematic_position, sender=Thematic)
    
    # will trigger `create_boolean` after every boolean question creation
    # post_save.connect(create_boolean_choices, sender=BooleanQuestion)
    # post_save.connect(create_user_choice_fieds, sender=UserGenderQuestion)

    # create user information on user created
    post_save.connect(create_user_informations, sender=get_user_model())


    pre_save.connect(clean_thematic, sender=Thematic)
    pre_save.connect(clean_feedback, sender=StaticFeedback)

#EOF
