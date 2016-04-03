import os
import random
import string
from django.core.exceptions import ImproperlyConfigured
from filebrowser.utils import convert_filename
from awards import settings


def generate_user_id(prefix="USR"):
    """
    """

    from useraccount.models import UserProfile
    user_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    user_id = "%s%s" % (prefix, user_id)

    if UserProfile.objects.filter(user_id=user_id).count() > 0:
        generate_user_id(prefix=prefix)
    else:
        return user_id



def generate_unique_file_name(directory, file_name, ext):
    """
    Generates a unique file name inside a given directory using provided file_name
    :param directory: directory
    :param file_name: name of file (with ext)
    :param ext: the file extension
    :return: new file name + ext
    """
    count = 0

    while os.path.exists(os.path.join(directory, file_name + ext)):
        count += 1
        a = file_name[file_name.rfind("(") + 1:file_name.rfind(")")]
        if a.isdigit():
            file_name = file_name.rsplit('(' + a + ')', 1)[0]
        file_name = file_name + '(' + str(count) + ')'
    return file_name + ext



def normalize_file_name(name):
    """
    Normalize a given file name.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return convert_filename(''.join(c for c in name if c in valid_chars))



def get_user_model():
    # from django.db.models import get_model
    from django.apps import apps

    try:
        app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the"
                                   " form 'app_label.model_name'")
    user_model = apps.get_model(app_label, model_name)
    if user_model is None:
        raise ImproperlyConfigured("AUTH_USER_MODEL refers to model"
                                   " '%s' that has not been installed"
                                   % settings.AUTH_USER_MODEL)
    return user_model



