from django.core.management.base import BaseCommand

from faker import Faker


from django.contrib.auth import get_user_model
from todo.models import Task


User = get_user_model()


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', nargs='?', type=int, default=5,
                            help='The number of users that will be generated')

    def handle(self, *args, **options):
        N = options['number']
        if not N or N <= 0:
            N = 5

        profile = self.fake.simple_profile()
        user, _ = User.objects.get_or_create(
            username=profile['username']+str(self.fake.pyint()),
            email=profile['mail'],
            password="Test@123456"
        )

        for _ in range(N):

            Task.objects.create(
                user=user,
                title=self.fake.text(max_nb_chars=20),
                complete=self.fake.boolean(chance_of_getting_true=25)
            )

        print(f'[{N}] tasks generated successfully!')
