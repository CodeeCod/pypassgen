import random
import string
import argparse
import sys

class PasswordGenerator:
    def __init__(self):
        self.complexity_levels = {
            'low': {
                'description': 'Только буквы (нижний регистр)',
                'chars': string.ascii_lowercase,
                'min_length': 4
            },
            'medium': {
                'description': 'Буквы верхнего и нижнего регистра',
                'chars': string.ascii_letters,
                'min_length': 6
            },
            'high': {
                'description': 'Буквы + цифры',
                'chars': string.ascii_letters + string.digits,
                'min_length': 8
            },
            'very-high': {
                'description': 'Буквы + цифры + специальные символы',
                'chars': string.ascii_letters + string.digits + string.punctuation,
                'min_length': 10
            }
        }
    
    def generate_password(self, length, complexity):
        """Генерация пароля заданной длины и сложности"""
        if complexity not in self.complexity_levels:
            raise ValueError(f"Неизвестный уровень сложности: {complexity}")
        
        chars = self.complexity_levels[complexity]['chars']
        min_length = self.complexity_levels[complexity]['min_length']
        
        if length < min_length:
            print(f"⚠️  Внимание: для сложности '{complexity}' рекомендуется длина не менее {min_length} символов")
        
        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
    
    def calculate_strength(self, password):
        """Оценка сложности пароля"""
        strength = 0
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in string.punctuation for c in password):
            strength += 1
        
        length_score = min(len(password) // 4, 3)  # Максимум 3 балла за длину
        return strength + length_score
    
    def display_complexity_info(self):
        """Показать информацию о уровнях сложности"""
        print("\n📊 Уровни сложности паролей:")
        print("-" * 50)
        for level, info in self.complexity_levels.items():
            print(f"{level:12} - {info['description']} (мин. длина: {info['min_length']})")
        print()

def main():
    parser = argparse.ArgumentParser(description='Генератор безопасных паролей')
    parser.add_argument('-l', '--length', type=int, default=12, 
                       help='Длина пароля (по умолчанию: 12)')
    parser.add_argument('-c', '--complexity', type=str, default='high',
                       choices=['low', 'medium', 'high', 'very-high'],
                       help='Уровень сложности: low, medium, high, very-high')
    parser.add_argument('-n', '--number', type=int, default=1,
                       help='Количество генерируемых паролей')
    parser.add_argument('--info', action='store_true',
                       help='Показать информацию о уровнях сложности')
    
    # Исправляем обработку аргументов
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    args = parser.parse_args()
    generator = PasswordGenerator()
    
    if args.info:
        generator.display_complexity_info()
        return
    
    try:
        print(f"\n🔐 Генерация паролей:")
        print(f"   Длина: {args.length} символов")
        print(f"   Сложность: {args.complexity}")
        print(f"   Количество: {args.number}")
        print("-" * 40)
        
        for i in range(args.number):
            password = generator.generate_password(args.length, args.complexity)
            strength = generator.calculate_strength(password)
            strength_stars = "★" * strength + "☆" * (8 - strength)
            
            print(f"Пароль {i+1}: {password}")
            print(f"Сложность: {strength_stars} ({strength}/8)")
            print()
            
    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

def interactive_mode():
    """Интерактивный режим с выбором параметров"""
    generator = PasswordGenerator()
    
    print("🎯 Интерактивный генератор паролей")
    print("=" * 50)
    
    # Выбор сложности
    generator.display_complexity_info()
    
    while True:
        complexity = input("Выберите уровень сложности (low/medium/high/very-high): ").lower()
        if complexity in generator.complexity_levels:
            break
        print("❌ Неверный выбор. Попробуйте снова.")
    
    # Выбор длины
    min_length = generator.complexity_levels[complexity]['min_length']
    while True:
        try:
            length = int(input(f"Введите длину пароля (мин. {min_length}): "))
            if length >= min_length:
                break
            print(f"❌ Длина должна быть не менее {min_length} символов.")
        except ValueError:
            print("❌ Введите число.")
    
    # Количество паролей
    while True:
        try:
            count = int(input("Сколько паролей сгенерировать? (1-20): "))
            if 1 <= count <= 20:
                break
            print("❌ Введите число от 1 до 20.")
        except ValueError:
            print("❌ Введите число.")
    
    # Генерация
    print(f"\n🔐 Результаты:")
    print("-" * 40)
    
    for i in range(count):
        password = generator.generate_password(length, complexity)
        strength = generator.calculate_strength(password)
        strength_stars = "★" * strength + "☆" * (8 - strength)
        
        print(f"Пароль {i+1}: {password}")
        print(f"Сложность: {strength_stars} ({strength}/8)")
        print()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()