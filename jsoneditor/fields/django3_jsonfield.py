from django.db.models import JSONField as _JSONField
from django.forms import JSONField as _JSONFormField
from jsoneditor.forms import JSONEditor


class JSONFormField(_JSONFormField):
    widget = JSONEditor
    def __init__(self,*av,**kw):
        kw['widget'] = self.widget(
            schema=kw.pop("schema"), 
            schema_refs=kw.pop("schema_refs")
        ) # force avoiding widget override
        super(JSONFormField,self).__init__(*av,**kw)

class JSONField(_JSONField):
    def __init__(self,schema=None,schema_refs=None,*av,**kw):
        self.schema = schema
        self.schema_refs = schema_refs
        super(JSONField,self).__init__(*av,**kw)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': kwargs.get('form_class', JSONFormField),
            'schema': self.schema,
            'schema_refs': self.schema_refs
        }
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)
