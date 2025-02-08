# Generated by Django 2.1 on 2021-01-06 06:11

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boundary',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('WARNING', 'Warning'), ('ERROR', 'Error'), ('COMPLETE', 'Complete')], default='PENDING', max_length=10)),
                ('label', models.CharField(max_length=128, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('color', models.CharField(default='blue', max_length=64)),
                ('display_field', models.CharField(blank=True, max_length=10, null=True)),
                ('data_fields', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('errors', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('source_file', models.FileField(upload_to='boundaries/%Y/%m/%d')),
            ],
            options={
                'verbose_name': 'Boundary',
                'verbose_name_plural': 'Boundaries',
            },
        ),
        migrations.CreateModel(
            name='BoundaryPolygon',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('boundary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polygons', to='grout.Boundary')),
            ],
            options={
                'verbose_name': 'Boundary Polygon',
                'verbose_name_plural': 'Boundary Polygons',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True)),
                ('archived', models.BooleanField(default=False)),
                ('occurred_from', models.DateTimeField(blank=True, null=True)),
                ('occurred_to', models.DateTimeField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('location_text', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='RecordSchema',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('version', models.PositiveIntegerField()),
                ('schema', django.contrib.postgres.fields.jsonb.JSONField()),
                ('next_version', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_version', to='grout.RecordSchema')),
            ],
        ),
        migrations.CreateModel(
            name='RecordType',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=64)),
                ('plural_label', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('geometry_type', models.CharField(choices=[('point', 'Point'), ('polygon', 'Polygon'), ('multipolygon', 'MultiPolygon'), ('linestring', 'LineString'), ('none', 'None')], default='point', max_length=12)),
                ('temporal', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recordschema',
            name='record_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schemas', to='grout.RecordType'),
        ),
        migrations.AddField(
            model_name='record',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grout.RecordSchema'),
        ),
        migrations.AlterUniqueTogether(
            name='recordschema',
            unique_together={('record_type', 'version')},
        ),
    ]
