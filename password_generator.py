import random
import string
import argparse
import sys

class PasswordGenerator:
    def __init__(self):
        self.complexity_levels = [
            {
                'name': 'low',
                'description': 'Только буквы (нижний регистр)',
                'chars': string.ascii_lowercase,
                'min_length': 4
            },
            {
                'name': 'medium',
                'description': 'Буквы верхнего и нижнего регистра',
                'chars': string.ascii_letters,
                'min_length': 6
            },
            {
                'name': 'high',
                'description': 'Буквы + цифры',
                'chars': string.ascii_letters + string.digits,
                'min_length': 8
            },
            {
                'name': 'very-high',
                'description': 'Буквы + цифры + специальные символы',
                'chars': string.ascii_letters + string.digits + string.punctuation,
                'min_length': 10
            }
        ]
    
    def get_complexity_by_index(self, index):
        """Получить уровень сложности по индексу"""
        if 0 <= index < len(self.complexity_levels):
            return self.complexity_levels[index]
        return None
    
    def get_complexity_by_name(self, name):
        """Получить уровень сложности по имени"""
        for level in self.complexity_levels:
            if level['name'] == name:
                return level
        return None
    
    def generate_password(self, length, complexity_name):
        """Генерация пароля заданной длины и сложности"""
        complexity = self.get_complexity_by_name(complexity_name)
        if complexity is None:
            raise ValueError(f"Неизвестный уровень сложности: {complexity_name}")
        
        chars = complexity['chars']
        min_length = complexity['min_length']
        
        if length < min_length:
            print(f"⚠️  Внимание: для сложности '{complexity_name}' рекомендуется длина не менее {min_length} символов")
        
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
        for i, level in enumerate(self.complexity_levels, 1):
            print(f"{i}. {level['name']:12} - {level['description']} (мин. длина: {level['min_length']})")
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
    
    # Выбор сложности через номер
    generator.display_complexity_info()
    
    while True:
        try:
            choice = int(input("Выберите уровень сложности (введите номер 1-4): "))
            complexity = generator.get_complexity_by_index(choice - 1)
            if complexity:
                complexity_name = complexity['name']
                break
            print("❌ Неверный номер. Попробуйте снова.")
        except ValueError:
            print("❌ Введите число от 1 до 4.")
    
    # Выбор длины
    min_length = complexity['min_length']
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
    print(f"   Сложность: {complexity_name}")
    print("-" * 40)
    
    for i in range(count):
        password = generator.generate_password(length, complexity_name)
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