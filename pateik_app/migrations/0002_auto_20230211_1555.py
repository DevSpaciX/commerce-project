from django.core.management import call_command
from django.db import migrations


def load_fixtures(state, schema_editor):
    call_command("loaddata", "fixture_file.json")


def reverse_load_fixtures(state, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('pateik_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixtures, reverse_load_fixtures)
    ]
