from itertools import chain
from datetime import datetime

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
        if isinstance(data[f.name], datetime):
            data[f.name] = str(data[f.name])
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data