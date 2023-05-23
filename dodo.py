"""Automation tasks."""

DOIT_CONFIG = {'default_task': ['all']}


def task_style():
    """Check source files with flake8."""
    return {
        'actions': ['flake8 src']
    }


def task_docstyle():
    """Check source files with pydocstyle."""
    return {
        'actions': ['pydocstyle src']
    }


def task_test():
    """Run tests."""
    return {
        'actions': ['pytest -v'],
        'verbosity': 2
    }


def task_html():
    """Generate html Sphinx documentation."""
    return {
        'actions': ['sphinx-build -M html docs/ docs/build']
    }


def task_check():
    """Perform style checks and run tests."""
    return {
        'actions': None,
        'task_dep': ['style', 'docstyle', 'test']
    }


def task_verify_model():
    """Verify that model can be loaded. Must be run before starting the bot."""
    return {
        'actions': ['python verify_model.py']
    }


def task_app_ru():
    """Run the app."""
    return {
        'actions': ['LC_ALL=ru_RU.UTF-8 python src/tgbot/__main__.py'],
        'task_dep': [
            'verify_model',
            'russian'
        ]
    }


def task_app_en():
    """Run the app."""
    return {
        'actions': ['LC_ALL=en_US.UTF-8 python src/tgbot/__main__.py'],
        'task_dep': [
            # 'verify_model',
            'english'
        ]
    }

def task_gitclean():
    """Remove all generated files."""
    return {
        'actions': ['git clean -xdf']
    }


def task_english():
    """Compile English language."""
    return {
        'actions': ['pybabel compile -D controlnetbot -d locale -l en']
    }


def task_russian():
    """Compile Russian language."""
    return {
        'actions': ['pybabel compile -D controlnetbot -d locale -l ru']
    }
