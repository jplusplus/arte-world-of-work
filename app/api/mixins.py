from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType

from app.core.mixins import AsFinalMixin

class SerializerNotFoundError(Exception):
    pass

class PatchGenericAPIViewMixin(object):
    # Monkey patching of `rest_framework.generics.GenericAPIView.get_serializer`
    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        serializer = super(PatchGenericAPIViewMixin, self).get_serializer(instance=instance, 
            data=data, files=files, many=many, partial=partial)
        assert isinstance(serializer, InheritedModelMixin) 
        return serializer.as_final_serializer(data=data, files=files)

class UpdateInheritedModelMixin(PatchGenericAPIViewMixin, mixins.UpdateModelMixin):
    # Monkey patching for CreateModelMixin which provides a `create` method that
    # will use the `get_serializer` method inherited from PatchGenericAPIViewMixin 
    pass

class CreateInheritedModelMixin(PatchGenericAPIViewMixin, mixins.CreateModelMixin):
    # Monkey patching for CreateModelMixin which provides a `create` method that
    # will use the `get_serializer` method inherited from PatchGenericAPIViewMixin 
    pass

class InheritedModelMixin(serializers.ModelSerializer):
        
    def __init__(self, *args, **kwargs):
        self.check_class()
        super(InheritedModelMixin, self).__init__(*args, **kwargs)

    def check_class(self):
        klass_name = self.__class__.__name__
        error_msg  = "{klass} subclasses must implement model_mapping attribute"
        assert getattr(self, 'model_mapping', None) != None, error_msg.format(
            klass=klass_name)

    def check_value(self, value):
        error_msg  =  "%s must inherit from app.core.mixins.AsFinalMixin" 
        assert isinstance( value, AsFinalMixin), error_msg % value

    def to_native(self, value):
        if not value:
            return None
        self.check_value(value)
        final_value = value.as_final()
        base_data   = super(InheritedModelMixin, self).to_native(value)
        serializer  = self.get_final_serializer(final_value)
        if serializer:
            base_data.update(serializer(final_value, context=self.context).data)
        return base_data

    def get_final_serializer(self, value):
        for model_klass in self.model_mapping.keys():
            match = isinstance(value, model_klass) or \
                    issubclass(value.__class__, model_klass)

            if not match:
                try: 
                    match = issubclass(value, model_klass)
                except:
                    match = False
            if match:
                return self.model_mapping[model_klass]
        if not match:
            msg = 'Cound not find the final serializer for {value} '
            raise SerializerNotFoundError(msg.format(value=value))

    def as_final_serializer(self, data, files):
        klass = self.__class__.__name__
        raise NotImplementedError('%s must implement as_final_serializer method' % klass_name)

class GenericModelMixin(serializers.ModelSerializer):
    
    def get_ctype_serializer(self, value):
        ctype, cobject = self.get_generic(value)
        ctype_mapping = self.get_mapping()
        for model_klass in ctype_mapping.keys():
            if issubclass(ctype.model_class(), model_klass) or \
                isinstance(cobject, model_klass):
                return ctype_mapping[model_klass]

    def get_generic(self, value):
        ctype   = getattr(value, 'content_type',   None)
        if not ctype:
            ctype = ContentType.objects.get_for_model(value)

        obj_id  = getattr(value, 'object_id',      None)
        # first try to resolve content object 
        cobject = getattr(value, 'content_object', None) 
        # if doesn't have a local content_object then we assign it here
        if cobject is None:
            cobject = ctype.model_class().objects.get(pk=obj_id or value.pk)
        return (ctype, cobject)

    def get_mapping(self):
        return self.ctype_mapping

    def to_native(self, value):
        ctype, cobject = self.get_generic(value)
        base_data = super(GenericModelMixin, self).to_native(value)
        ctype_serializer = self.get_ctype_serializer(value)
        if ctype_serializer:
            base_data.update(ctype_serializer(cobject, context=self.context).data)
        return base_data


