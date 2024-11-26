# Django Admin Autocomplete

A Django package that adds autocomplete functionality to the Django admin search bar. It provides a seamless way to search through your models in the admin interface with real-time suggestions.

## Features

- Real-time search suggestions in Django admin
- Keyboard navigation support (arrow keys, enter, escape)
- Customizable minimum characters for search
- Supports multiple search fields
- Modern and responsive design
- Easy integration with existing Django admin

## Installation

```bash
pip install django-admin-autocomplete
```

## Quick Start

1. Add `admin_autocomplete` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'admin_autocomplete',
]
```

2. Use the `AutocompleteAdminMixin` in your ModelAdmin:

```python
from django.contrib import admin
from admin_autocomplete.admin import AutocompleteAdminMixin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(AutocompleteAdminMixin, admin.ModelAdmin):
    search_fields = ['title', 'description']  # Fields to search
```

## Configuration

You can customize the autocomplete behavior in your Django settings:

```python
ADMIN_AUTOCOMPLETE = {
    'MIN_CHARS': 2,  # Minimum characters before showing suggestions
    'MAX_RESULTS': 10,  # Maximum number of suggestions to show
}
```

## Example

Here's a complete example using a Book model:

```python
# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.title} by {self.author}"

# admin.py
from django.contrib import admin
from admin_autocomplete.admin import AutocompleteAdminMixin
from .models import Book

@admin.register(Book)
class BookAdmin(AutocompleteAdminMixin, admin.ModelAdmin):
    search_fields = ['title', 'author', 'isbn']
```

## Running Tests

The package includes comprehensive tests, including end-to-end tests using Selenium. To run the tests:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
python manage.py test admin_autocomplete.tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
