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


def task_app():
    """Run the app."""
    return {
        'actions': ['python src/tgbot/__main__.py'],
        'task_dep': ['verify_model']
    }
