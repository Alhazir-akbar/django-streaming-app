import os
import django
from django.apps import apps
from django.db import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

def get_model_structure():
    model_structure = []

    for model in apps.get_models():
        model_info = f"Model: {model.__name__}\n"
        model_info += "Fields:\n"

        for field in model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                field_info = f"  - {field.name} (ForeignKey to {field.related_model.__name__})"
            elif isinstance(field, models.ManyToManyField):
                field_info = f"  - {field.name} (ManyToManyField with {field.related_model.__name__})"
            elif isinstance(field, models.OneToOneField):
                field_info = f"  - {field.name} (OneToOneField with {field.related_model.__name__})"
            else:
                field_info = f"  - {field.name} ({field.get_internal_type()})"
            model_info += f"{field_info}\n"

        model_structure.append(model_info)

    return "\n".join(model_structure)

if __name__ == "__main__":
    structure = get_model_structure()
    with open('models_structure.txt', 'w') as file:
        file.write(structure)
    print("Model structure has been written to models_structure.txt")
