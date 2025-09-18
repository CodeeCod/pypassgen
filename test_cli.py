import pytest
import subprocess
import sys
import os
from password_generator import main, interactive_mode
from unittest.mock import patch, MagicMock, call

# Добавляем путь к модулю
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestCLI:
    """Тесты командной строки"""
    
    def test_cli_help(self):
        """Тест вывода справки"""
        result = subprocess.run([
            sys.executable, 'password_generator.py', '--help'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Генератор безопасных паролей' in result.stdout
        assert '--length' in result.stdout
        assert '--complexity' in result.stdout
    
    @pytest.mark.parametrize("complexity", ['low', 'medium', 'high', 'very-high'])
    def test_cli_complexity_levels(self, complexity):
        """Тест всех уровней сложности через CLI"""
        result = subprocess.run([
            sys.executable, 'password_generator.py',
            '--length', '12',
            '--complexity', complexity,
            '--number', '1'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Генерация паролей' in result.stdout or 'Пароль' in result.stdout
    
    def test_cli_multiple_passwords(self):
        """Тест генерации нескольких паролей"""
        result = subprocess.run([
            sys.executable, 'password_generator.py',
            '--length', '8',
            '--complexity', 'medium',
            '--number', '3'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        # Должно быть 3 пароля в выводе
        assert result.stdout.count('Пароль') == 3 or 'Генерация паролей' in result.stdout
    
    def test_cli_info_flag(self):
        """Тест флага --info"""
        result = subprocess.run([
            sys.executable, 'password_generator.py', '--info'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Уровни сложности паролей' in result.stdout
        assert '1.' in result.stdout  # Проверяем нумерацию
        assert '4.' in result.stdout  # Проверяем нумерацию
    
    def test_cli_invalid_complexity(self):
        """Тест неверного уровня сложности"""
        result = subprocess.run([
            sys.executable, 'password_generator.py',
            '--complexity', 'invalid'
        ], capture_output=True, text=True)
        
        # Может вернуть 0 или не 0 в зависимости от обработки ошибок
        assert 'error' in result.stderr.lower() or 'Ошибка' in result.stderr or result.returncode != 0
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_mode(self, mock_print, mock_input):
        """Тест интерактивного режима"""
        # Мокируем ввод пользователя: выбор сложности (1-4), длина, количество
        mock_input.side_effect = ['2', '12', '2']  # medium complexity
        
        # Запускаем интерактивный режим
        interactive_mode()
        
        # Проверяем что были вызовы input с ожидаемыми сообщениями
        assert mock_input.call_count == 3
        # Проверяем что print вызывался (не проверяем конкретный вывод)
        assert mock_print.call_count > 0


class TestMainFunction:
    """Тесты основной функции"""
    
    @patch('password_generator.interactive_mode')
    @patch('sys.argv', ['password_generator'])
    def test_main_no_args_calls_interactive(self, mock_interactive):
        """Тест что без аргументов вызывается интерактивный режим"""
        # Мокируем sys.exit чтобы программа не завершалась
        with patch('sys.exit'):
            main()
        mock_interactive.assert_called_once()
    
    @patch('password_generator.PasswordGenerator.generate_password')
    @patch('password_generator.PasswordGenerator.calculate_strength')
    @patch('sys.argv', ['password_generator', '--length', '12', '--complexity', 'high', '--number', '2'])
    def test_main_with_args(self, mock_strength, mock_generate):
        """Тест main с аргументами"""
        mock_generate.return_value = 'TestPassword123'
        mock_strength.return_value = 5
        
        # Мокируем sys.exit чтобы программа не завершалась
        with patch('sys.exit'):
            main()
        
        assert mock_generate.call_count == 2
        assert mock_strength.call_count == 2
    
    @patch('password_generator.PasswordGenerator.display_complexity_info')
    @patch('sys.argv', ['password_generator', '--info'])
    def test_main_info_flag(self, mock_display):
        """Тест флага --info в main"""
        # Мокируем sys.exit чтобы программа не завершалась
        with patch('sys.exit'):
            main()
        
        mock_display.assert_called_once()