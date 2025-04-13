from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from projects.models import Project, Category
from django.utils import timezone
from datetime import timedelta
import random
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Seed categories and projects with sample data"

    def handle(self, *args, **options):
        try:
            # Get the admin user (id=1)
            user = User.objects.get(id=1)

            # Create categories
            categories_data = [
                {
                    "title": "Technology",
                    "description": "Projects involving innovative tech solutions and gadgets. "
                    * 3,
                },
                {
                    "title": "Art & Design",
                    "description": "Creative projects in visual arts, design, and multimedia. "
                    * 3,
                },
                {
                    "title": "Education",
                    "description": "Educational initiatives and learning platforms. "
                    * 3,
                },
                {
                    "title": "Environment",
                    "description": "Projects focused on environmental sustainability and conservation. "
                    * 3,
                },
                {
                    "title": "Health",
                    "description": "Healthcare innovations and wellness projects. " * 3,
                },
            ]

            created_categories = []
            for cat_data in categories_data:
                category, created = Category.objects.get_or_create(
                    title=cat_data["title"],
                    defaults={"description": cat_data["description"]},
                )
                created_categories.append(category)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created category: {category.title}")
                    )

            # Default thumbnail path
            default_thumbnail = os.path.join(
                os.path.dirname(__file__), "../../../media/images/default_thumbnail.jpg"
            )

            # Create 10 projects
            for i in range(10):
                # Set featured true for first 5 projects
                is_featured = i < 5

                start_time = timezone.now() + timedelta(days=1)
                end_time = start_time + timedelta(days=30)

                project = Project.objects.create(
                    title=f"Test Project {i + 1}",
                    details="This is a test project with detailed description that meets the minimum character requirement. "
                    * 3,
                    total_target=random.randint(10000, 100000),
                    start_time=start_time,
                    end_time=end_time,
                    user=user,
                    is_featured=is_featured,
                    category=random.choice(created_categories),
                    is_accepted=True,
                )

                # Add thumbnail
                with open(default_thumbnail, "rb") as image_file:
                    project.thumbnail.save(
                        f"project_{i + 1}_thumbnail.jpg", File(image_file), save=True
                    )

                # Add tags based on category
                project.tags.add(
                    project.category.title.lower(), "test", f"project{i + 1}"
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created project: {project.title} (Category: {project.category.title}, Featured: {is_featured})"
                    )
                )

        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    "User with id=1 does not exist. Please create an admin user first."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
