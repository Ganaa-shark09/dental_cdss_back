from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cdss", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cdssengine",
            name="department",
            field=models.CharField(
                choices=[
                    ("GENERAL", "General Dentistry"),
                    ("ENDODONTICS", "Endodontics"),
                    ("PERIODONTICS", "Periodontics"),
                    ("ORAL_SURGERY", "Oral Surgery"),
                    ("ORTHODONTICS", "Orthodontics"),
                    ("PROSTHODONTICS", "Prosthodontics"),
                    ("PEDIATRIC", "Pediatric Dentistry"),
                    ("PREVENTIVE", "Preventive Dentistry"),
                ],
                default="GENERAL",
                max_length=30,
            ),
        ),
    ]
