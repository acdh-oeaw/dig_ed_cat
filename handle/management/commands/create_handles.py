from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType

from handle import utils
from handle.models import Pid


class Command(BaseCommand):

    """Creates handle-id for all objects of the passed in class"""

    help = 'Creates handle-id for all objects of the passed in class'

    def add_arguments(self, parser):
        parser.add_argument(
            'class', type=str, help="Lowercase name of the class you want to process"
        )
        parser.add_argument(
            '--pid',
            dest='pid',
            help="The name of the GenericRelation field you added to your class\
            to store the handle-pid. Default is 'pid'."
        )

    def handle(self, *args, **options):
        model_name = options['class']
        if options['pid']:
            filters = {options['pid']: None}
        else:
            filters = {'pid': None}
        try:
            ct = ContentType.objects.get(model=model_name).model_class()
        except ObjectDoesNotExist:
            ct = None
        if ct:
            qs = ct.objects.filter(**filters)
            for x in qs:
                new_hdl = Pid(content_object=x)
                new_hdl.save()
                self.stdout.write(self.style.SUCCESS(new_hdl.handle))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    """
                    Something went wrong.
                    Please make sure that the class: "{}" you chose actually exists
                    """.format(model_name)
                )
            )
