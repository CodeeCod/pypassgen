import pytest
import string
from password_generator import PasswordGenerator
import sys
import os

# Добавляем путь к модулю
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestPasswordGenerator:
    """Тесты для класса PasswordGenerator"""
    
    @pytest.fixture
    def generator(self):
        return PasswordGenerator()
    
    def test_init(self, generator):
        """Тест инициализации генератора"""
        assert generator is not None
        assert hasattr(generator, 'complexity_levels')
        assert len(generator.complexity_levels) == 4
    
    def test_complexity_levels_structure(self, generator):
        """Тест структуры уровней сложности"""
        levels = generator.complexity_levels
        assert levels[0]['name'] == 'low'
        assert levels[1]['name'] == 'medium'
        assert levels[2]['name'] == 'high'
        assert levels[3]['name'] == 'very-high'
    
    @pytest.mark.parametrize("index,expected_name", [
        (0, 'low'),
        (1, 'medium'),
        (2, 'high'),
        (3, 'very-high'),
        (4, None),  # Несуществующий индекс
        (-1, None),  # Отрицательный индекс
    ])
    def test_get_complexity_by_index(self, generator, index, expected_name):
        """Тест получения уровня сложности по индексу"""
        result = generator.get_complexity_by_index(index)
        if expected_name:
            assert result['name'] == expected_name
        else:
            assert result is None
    
    @pytest.mark.parametrize("name,expected", [
        ('low', True),
        ('medium', True),
        ('high', True),
        ('very-high', True),
        ('invalid', False),  # Несуществующее имя
    ])
    def test_get_complexity_by_name(self, generator, name, expected):
        """Тест получения уровня сложности по имени"""
        result = generator.get_complexity_by_name(name)
        if expected:
            assert result['name'] == name
        else:
            assert result is None
    
    @pytest.mark.parametrize("index,expected_chars", [
        (0, string.ascii_lowercase),
        (1, string.ascii_letters),
        (2, string.ascii_letters + string.digits),
        (3, string.ascii_letters + string.digits + string.punctuation)
    ])
    def test_complexity_chars(self, generator, index, expected_chars):
        """Тест правильности наборов символов для каждого уровня сложности"""
        level = generator.get_complexity_by_index(index)
        assert level['chars'] == expected_chars
    
    @pytest.mark.parametrize("index,min_length", [
        (0, 4),
        (1, 6),
        (2, 8),
        (3, 10)
    ])
    def test_complexity_min_length(self, generator, index, min_length):
        """Тест минимальной длины для каждого уровня сложности"""
        level = generator.get_complexity_by_index(index)
        assert level['min_length'] == min_length
    
    @pytest.mark.parametrize("length,complexity_name", [
        (8, 'low'),
        (10, 'medium'),
        (12, 'high'),
        (15, 'very-high')
    ])
    def test_generate_password_length(self, generator, length, complexity_name):
        """Тест генерации пароля правильной длины"""
        password = generator.generate_password(length, complexity_name)
        assert len(password) == length
    
    @pytest.mark.parametrize("complexity_name,expected_chars", [
        ('low', string.ascii_lowercase),
        ('medium', string.ascii_letters),
        ('high', string.ascii_letters + string.digits),
        ('very-high', string.ascii_letters + string.digits + string.punctuation)
    ])
    def test_generate_password_chars(self, generator, complexity_name, expected_chars):
        """Тест что пароль содержит только разрешенные символы"""
        password = generator.generate_password(20, complexity_name)
        for char in password:
            assert char in expected_chars
    
    def test_generate_password_invalid_complexity(self, generator):
        """Тест ошибки при неверном уровне сложности"""
        with pytest.raises(ValueError, match="Неизвестный уровень сложности"):
            generator.generate_password(10, 'invalid')
    
    @pytest.mark.parametrize("password,expected_strength", [
        ('abc', 1),  # только lowercase + длина 0 (1+0)
        ('abcd', 2),  # только lowercase + длина 1 (1+1)
        ('abcABC', 3),  # lowercase + uppercase + длина 1 (2+1)
        ('abc123', 3),  # lowercase + digits + длина 1 (2+1)
        ('abcABC123', 5),  # lowercase + uppercase + digits + длина 2 (3+2)
        ('abcABC123!', 6),  # все категории + длина 2 (4+2)
        ('a' * 4, 2),  # короткий пароль (1+1)
        ('a' * 12, 4),  # длинный пароль с одним типом символов (1+3)
        ('aA1!' * 4, 7),  # все категории + хорошая длина (4+3)
    ])
    def test_calculate_strength(self, generator, password, expected_strength):
        """Тест оценки сложности пароля"""
        assert generator.calculate_strength(password) == expected_strength
    
    def test_display_complexity_info(self, generator, capsys):
        """Тест отображения информации о сложности"""
        generator.display_complexity_info()
        captured = capsys.readouterr()
        assert "Уровни сложности паролей" in captured.out
        assert "1." in captured.out  # Проверяем нумерацию
        assert "4." in captured.out  # Проверяем нумерацию


class TestPasswordGeneratorIntegration:
    """Интеграционные тесты"""
    
    @pytest.fixture
    def generator(self):
        return PasswordGenerator()
    
    def test_multiple_passwords_unique(self, generator):
        """Тест что генерируются уникальные пароли"""
        passwords = [generator.generate_password(12, 'high') for _ in range(10)]
        unique_passwords = set(passwords)
        assert len(unique_passwords) == 10  # Все пароли должны быть уникальными
    
    def test_password_randomness(self, generator):
        """Тест случайности генерации (статистический)"""
        passwords = [generator.generate_password(100, 'very-high') for _ in range(5)]
        
        # Проверяем что пароли разные
        assert len(set(passwords)) == 5
        
        # Проверяем что используются разные символы
        all_chars = ''.join(passwords)
        unique_chars = set(all_chars)
        assert len(unique_chars) > 20  # Должно быть много разных символов


class TestEdgeCases:
    """Тесты граничных случаев"""
    
    @pytest.fixture
    def generator(self):
        return PasswordGenerator()
    
    @pytest.mark.parametrize("complexity_name,min_length", [
        ('low', 4),
        ('medium', 6),
        ('high', 8),
        ('very-high', 10)
    ])
    def test_minimum_length_generation(self, generator, complexity_name, min_length):
        """Тест генерации пароля минимальной длины"""
        password = generator.generate_password(min_length, complexity_name)
        assert len(password) == min_length
    
    def test_very_long_password(self, generator):
        """Тест генерации очень длинного пароля"""
        password = generator.generate_password(1000, 'high')
        assert len(password) == 1000
        assert all(char in (string.ascii_letters + string.digits) for char in password)
    
    def test_single_character_password(self, generator):
        """Тест генерации очень короткого пароля (с предупреждением)"""
        # Этот тест проверяет что функция не падает на очень коротких паролях
        password = generator.generate_password(1, 'low')
        assert len(password) == 1
        assert password in string.ascii_lowercase