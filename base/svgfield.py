from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_svg_file(value):
    if not value.name.endswith('.svg'):
        raise ValidationError(_('Недопустимый формат файла: разрешены только файлы SVG.'))


class SVGField(models.FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validate_svg_file)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('validators', None)
        return name, path, args, kwargs
