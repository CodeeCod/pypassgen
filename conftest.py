import pytest
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(autouse=True)
def add_namespace(doctest_namespace):
    """Добавляем модули в namespace для doctest"""
    doctest_namespace['sys'] = sys
    doctest_namespace['os'] = os