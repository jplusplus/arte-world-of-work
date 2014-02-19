from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

class InheritedModelMixin(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        error_msg = "{klass} subclasses must implement model_mapping attribute".format(
            klass=self.__class__.__name__)
        assert getattr(self, 'model_mapping', None) != None, error_msg
        super(InheritedModelMixin, self).__init__(*args, **kwargs)

    def to_native(self, value):
        if not value:
            return None
        base_data  = super(InheritedModelMixin, self).to_native(value)
        serializer = self.get_final_serializer(value)
        if serializer:
            base_data.update(serializer(value).data)
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


class InheritedModelCreateMixin(mixins.CreateModelMixin):
    # took from rest_framework.mixins.CreateModelMixin.create() base method
    def create(self, request, *args, **kwargs):
        # only variation: we don't use directly self.get_serializer but we want
        # the final serializer: i.e. the appropriated serializer for the given 
        # request DATA. 
        serializer = self.get_final_serializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_final_serializer(self, data, files):
        base_serializer = self.get_serializer(data=data, files=files)
        assert isinstance(base_serializer, InheritedModelMixin) 
        return base_serializer.as_final_serializer(data=data, files=files)

class ContentTypeMixin(serializers.ModelSerializer):

    def get_ctype_serializer(self, value):
        ctype, cobject = self.get_generic(value)
        ctype_mapping = self.get_mapping()
        for model_klass in ctype_mapping.keys():
            if issubclass(ctype.model_class(), model_klass) or \
                isinstance(cobject, model_klass):
                return ctype_mapping[model_klass]

    def get_generic(self, value):
        ctype   = getattr(value, 'content_type',   None)
        obj_id  = getattr(value, 'object_id',      None)
        # first try to resolve content object 
        cobject = getattr(value, 'content_object', None) 
        assert ctype != None
        # if doesn't have a local content_object then we assign it here
        if cobject is None:
            cobject = ctype.model_class().objects.get(pk=obj_id or value.pk)
        return (ctype, cobject)

    def get_mapping(self):
        return self.ctype_mapping

    def to_native(self, value):
        ctype, cobject = self.get_generic(value)
        base_data = super(ContentTypeMixin, self).to_native(value)
        ctype_serializer = self.get_ctype_serializer(value)
        if ctype_serializer:
            base_data.update(ctype_serializer(cobject).data)
        return base_data
