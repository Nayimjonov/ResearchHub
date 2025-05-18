from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Tag

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(
            name="Quantum Physics",
            category="discipline"
        )

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Quantum Physics")
        self.assertEqual(self.tag.slug, "quantum-physics")
        self.assertEqual(self.tag.category, "discipline")
        self.assertEqual(self.tag.usage_count, 0)
        self.assertIsNotNone(self.tag.created_at)

    def test_slug_autogeneration(self):
        tag = Tag.objects.create(name="Deep Learning", category="technology")
        self.assertEqual(tag.slug, "deep-learning")

    def test_category_choices_validation(self):
        tag = Tag(name="Invalid Category", category="biology")
        with self.assertRaises(ValidationError):
            tag.full_clean()

    def test_str_method(self):
        self.assertEqual(str(self.tag), "Quantum Physics")
