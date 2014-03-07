from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

MEDIA_TYPES = (
    ('icon', _('Icon (small)')),
    ('image', _('Image (big)')),
)

GENDER_TYPES = (
    ('male',    _('Male'  )),
    ('female',  _('Female')),
)


class CHART_TYPES:
    HISTOGRAMME = 'histogramme'
    PIE = 'pie'
    HORIZONTAL_BAR = 'horizontal_bar'
    VERTICAL_BAR = 'veritical_bar'
