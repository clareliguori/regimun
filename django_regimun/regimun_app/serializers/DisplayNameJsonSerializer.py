from django.core.serializers.json import Serializer as JsonSerializer
from django.utils.encoding import is_protected_type

class Serializer(JsonSerializer):

    def handle_field(self, obj, field):
        value = field._get_val_from_obj(obj)

        #If the object has a get_field_display() method, use it.
        display_method = "get_%s_display" % field.name
        if hasattr(obj, display_method):
            self._current[field.name] = getattr(obj, display_method)()

        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        elif is_protected_type(value):
            self._current[field.name] = value
        else:
            self._current[field.name] = field.value_to_string(obj)

