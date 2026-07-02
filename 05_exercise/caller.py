import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Author, Book
# Create queries within functions


def show_all_authors_with_their_books() -> str:
    authors = Author.objects.all()
    result = []
    for author in authors:
        books = author.books.all()
        result.append(f"{author.name} has written - {', '.join(str(b) for b in books)}!" )
    return "\n".join(result)

def delete_all_authors_without_books() -> None:
    authors = Author.objects.all()
    for author in authors:
        if author.books.count() == 0:
            author.delete()


