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
        assert 'low' in generator.complexity_levels
        assert 'very-high' in generator.complexity_levels
    
    @pytest.mark.parametrize("complexity,expected_chars", [
        ('low', string.ascii_lowercase),
        ('medium', string.ascii_letters),
        ('high', string.ascii_letters + string.digits),
        ('very-high', string.ascii_letters + string.digits + string.punctuation)
    ])
    def test_complexity_chars(self, generator, complexity, expected_chars):
        """Тест правильности наборов символов для каждого уровня сложности"""
        assert generator.complexity_levels[complexity]['chars'] == expected_chars
    
    @pytest.mark.parametrize("complexity,min_length", [
        ('low', 4),
        ('medium', 6),
        ('high', 8),
        ('very-high', 10)
    ])
    def test_complexity_min_length(self, generator, complexity, min_length):
        """Тест минимальной длины для каждого уровня сложности"""
        assert generator.complexity_levels[complexity]['min_length'] == min_length
    
    @pytest.mark.parametrize("length,complexity", [
        (8, 'low'),
        (10, 'medium'),
        (12, 'high'),
        (15, 'very-high')
    ])
    def test_generate_password_length(self, generator, length, complexity):
        """Тест генерации пароля правильной длины"""
        password = generator.generate_password(length, complexity)
        assert len(password) == length
    
    @pytest.mark.parametrize("complexity,expected_chars", [
        ('low', string.ascii_lowercase),
        ('medium', string.ascii_letters),
        ('high', string.ascii_letters + string.digits),
        ('very-high', string.ascii_letters + string.digits + string.punctuation)
    ])
    def test_generate_password_chars(self, generator, complexity, expected_chars):
        """Тест что пароль содержит только разрешенные символы"""
        password = generator.generate_password(20, complexity)
        for char in password:
            assert char in expected_chars
    
    def test_generate_password_invalid_complexity(self, generator):
        """Тест ошибки при неверном уровне сложности"""
        with pytest.raises(ValueError, match="Неизвестный уровень сложности"):
            generator.generate_password(10, 'invalid')
    
    @pytest.mark.parametrize("password,expected_strength", [
        ('abc', 1),  # только lowercase
        ('abcABC', 2),  # lowercase + uppercase
        ('abc123', 2),  # lowercase + digits
        ('abcABC123', 3),  # lowercase + uppercase + digits
        ('abcABC123!', 4),  # все категории
        ('a' * 4, 1),  # короткий пароль
        ('a' * 12, 2),  # длинный пароль с одним типом символов
        ('aA1!' * 4, 5),  # все категории + хорошая длина
    ])
    def test_calculate_strength(self, generator, password, expected_strength):
        """Тест оценки сложности пароля"""
        assert generator.calculate_strength(password) == expected_strength
    
    def test_display_complexity_info(self, generator, capsys):
        """Тест отображения информации о сложности"""
        generator.display_complexity_info()
        captured = capsys.readouterr()
        assert "Уровни сложности паролей" in captured.out
        assert "low" in captured.out
        assert "very-high" in captured.out


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
    
    @pytest.mark.parametrize("complexity,min_length", [
        ('low', 4),
        ('medium', 6),
        ('high', 8),
        ('very-high', 10)
    ])
    def test_minimum_length_generation(self, generator, complexity, min_length):
        """Тест генерации пароля минимальной длины"""
        password = generator.generate_password(min_length, complexity)
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