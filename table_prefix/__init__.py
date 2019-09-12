from django.db.models.signals import class_prepared
from table_prefix.utils import get_table_name, models_is_prefixed


def prefix_table(sender, *args, **kwargs):
    if models_is_prefixed(sender):
        sender._meta.db_table = get_table_name(sender._meta.db_table)

    for f in sender._meta.local_many_to_many:
        if not isinstance(f.remote_field.model, str):
            if models_is_prefixed(f.remote_field.model):
                f.remote_field.model._meta.db_table = get_table_name(f.remote_field.model._meta.db_table)

        if not isinstance(f.remote_field.through, str):
            if models_is_prefixed(f.remote_field.through):
                f.remote_field.through._meta.db_table = get_table_name(f.remote_field.through._meta.db_table)

class_prepared.connect(prefix_table)
