import pytest
import subprocess
import sys
import os
from password_generator import main, interactive_mode
from unittest.mock import patch, MagicMock

# Добавляем путь к модулю
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestCLI:
    """Тесты командной строки"""
    
    def test_cli_help(self):
        """Тест вывода справки"""
        result = subprocess.run([
            sys.executable, '-m', 'password_generator', '--help'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Генератор безопасных паролей' in result.stdout
        assert '--length' in result.stdout
        assert '--complexity' in result.stdout
    
    @pytest.mark.parametrize("complexity", ['low', 'medium', 'high', 'very-high'])
    def test_cli_complexity_levels(self, complexity):
        """Тест всех уровней сложности через CLI"""
        result = subprocess.run([
            sys.executable, '-m', 'password_generator',
            '--length', '12',
            '--complexity', complexity,
            '--number', '1'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Генерация паролей' in result.stdout
    
    def test_cli_multiple_passwords(self):
        """Тест генерации нескольких паролей"""
        result = subprocess.run([
            sys.executable, '-m', 'password_generator',
            '--length', '8',
            '--complexity', 'medium',
            '--number', '3'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        # Должно быть 3 пароля в выводе
        assert result.stdout.count('Пароль') == 3
    
    def test_cli_info_flag(self):
        """Тест флага --info"""
        result = subprocess.run([
            sys.executable, '-m', 'password_generator', '--info'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Уровни сложности паролей' in result.stdout
        assert 'low' in result.stdout
        assert 'very-high' in result.stdout
    
    def test_cli_invalid_complexity(self):
        """Тест неверного уровня сложности"""
        result = subprocess.run([
            sys.executable, '-m', 'password_generator',
            '--complexity', 'invalid'
        ], capture_output=True, text=True)
        
        assert result.returncode != 0
        assert 'error' in result.stderr.lower() or 'Ошибка' in result.stderr
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_mode(self, mock_print, mock_input):
        """Тест интерактивного режима"""
        # Мокируем ввод пользователя
        mock_input.side_effect = ['high', '12', '2']
        
        # Запускаем интерактивный режим
        interactive_mode()
        
        # Проверяем что были вызовы print с ожидаемыми сообщениями
        output = '\n'.join([call[0][0] for call in mock_print.call_args_list])
        assert 'Интерактивный генератор паролей' in output
        assert 'Результаты' in output


class TestMainFunction:
    """Тесты основной функции"""
    
    @patch('password_generator.interactive_mode')
    def test_main_no_args_calls_interactive(self, mock_interactive):
        """Тест что без аргументов вызывается интерактивный режим"""
        with patch('sys.argv', ['password_generator']):
            main()
            mock_interactive.assert_called_once()
    
    @patch('password_generator.PasswordGenerator.generate_password')
    @patch('password_generator.PasswordGenerator.calculate_strength')
    def test_main_with_args(self, mock_strength, mock_generate):
        """Тест main с аргументами"""
        mock_generate.return_value = 'TestPassword123'
        mock_strength.return_value = 5
        
        with patch('sys.argv', [
            'password_generator', 
            '--length', '12', 
            '--complexity', 'high',
            '--number', '2'
        ]):
            with patch('sys.exit'):
                main()
        
        assert mock_generate.call_count == 2
        assert mock_strength.call_count == 2
    
    @patch('password_generator.PasswordGenerator.display_complexity_info')
    def test_main_info_flag(self, mock_display):
        """Тест флага --info в main"""
        with patch('sys.argv', ['password_generator', '--info']):
            with patch('sys.exit'):
                main()
        
        mock_display.assert_called_once()