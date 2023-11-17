# Generated by Django 4.2.7 on 2023-11-15 12:51

import uuid

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("evaluations", "0002_populate_departments"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationDesignType",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "code",
                    models.SlugField(
                        help_text="unique identifier, containing only letters, numbers, underscores or hyphens",
                        max_length=128,
                        unique=True,
                    ),
                ),
                ("display", models.CharField(help_text="display name", max_length=512)),
                (
                    "collect_description",
                    models.BooleanField(default=False, help_text="Use for 'other' types to prompt further information"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="evaluations.evaluationdesigntype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="is_economic_type",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="is_impact_type",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="is_other_type",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="is_process_type",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="other_evaluation_type_description",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="published_evaluation_link",
        ),
        migrations.AddField(
            model_name="evaluation",
            name="other_reasons_unpublished_description",
            field=models.TextField(
                blank=True, help_text="description of other issues preventing publication", null=True
            ),
        ),
        migrations.AddField(
            model_name="evaluation",
            name="quality_reasons_unpublished_description",
            field=models.TextField(
                blank=True, help_text="description of quality issues preventing publication", null=True
            ),
        ),
        migrations.AddField(
            model_name="evaluation",
            name="reasons_unpublished",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("signoff", "Sign-off delays"),
                        ("procurement", "Procurement delays"),
                        ("resource", "Resource constraints"),
                        ("quality", "Quality issues (please specify)"),
                        ("changes", "Changes in the policy/programme being evaluated"),
                        ("other", "Other (please specify)"),
                    ],
                    max_length=256,
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="evaluation",
            name="rsm_evaluation_id",
            field=models.SmallIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="evaluation",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("planned", "A planned evaluation"),
                    ("ongoing", "An ongoing evaluation"),
                    ("complete", "A complete evaluation report"),
                ],
                max_length=512,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(blank=True, max_length=1024, null=True)),
                ("link", models.URLField(blank=True, max_length=1024, null=True)),
                ("rsm_report_id", models.SmallIntegerField(blank=True, null=True)),
                (
                    "evaluation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="evaluations.evaluation"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EvaluationDesignTypeDetail",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(blank=True, max_length=1024, null=True)),
                (
                    "design_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="evaluations.evaluationdesigntype"
                    ),
                ),
                (
                    "evaluation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="evaluations.evaluation"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="evaluation",
            name="evaluation_design_types",
            field=models.ManyToManyField(
                help_text="add more text for 'Other' Design Types",
                through="evaluations.EvaluationDesignTypeDetail",
                to="evaluations.evaluationdesigntype",
            ),
        ),
    ]