from django.utils.translation import ugettext as _


class ChoicesZero(object):
    """
        ChoicesZero class to simplify field choices creation.
        Choices starts from zero i.e. index of the item
    """

    def __init__(self, *args):
        self._choices = []
        for index, arg in enumerate(args):
            setattr(self, arg[0], index)
            self._choices.append((index, arg[1]))

    def __iter__(self):
        return iter(self._choices)


class ChoicesOne(object):
    """
        ChoicesOne class to simplify field choices creation.
        Choices starts from One i.e. (index + 1) of the item
    """

    def __init__(self, *args):
        self._choices = []
        for index, arg in enumerate(args):
            setattr(self, arg[0], index + 1)
            self._choices.append(((index + 1), arg[1]))

    def __iter__(self):
        return iter(self._choices)

    def field_display(self, arg):
        for key in self._choices:
            if key[0] == arg:
                return key[1]
        return None


USER = {

    'WINNER_MONTH': ChoicesOne(
        ('january', _('January')),
        ('February', _('February')),
        ('March', _('March')),
        ('April', _('April')),
        ('May', _('May')),
        ('June', _('June')),
        ('July', _('July')),
        ('August', _('August')),
        ('September', _('September')),
        ('October', _('October')),
        ('November', _('November')),
        ('December', _('December')),
    ),

}


IMAGE_NAME_CHOICES = {
    'TYPE': ChoicesOne(
        ('Award1', _('Award1')),
        ('Award2', _('Award2')),
        ('Award3', _('Award3')),
        ('Award4', _('Award4')),
        ('Award5', _('Award5')),
        ('Award6', _('Award6')),
        ('Award7', _('Award7')),
        ('Award8', _('Award8')),
        ('Footer1', _('Footer1')),
        ('Footer2', _('Footer2')),
        ('Footer3', _('Footer3')),
        ('Footer4', _('Footer4')),
        ('Coverimage', _('Coverimage')),
        ('Profileimage', _('Profileimage')),
        ('landingpageimage', _('landingpageimage')),
    )
}
