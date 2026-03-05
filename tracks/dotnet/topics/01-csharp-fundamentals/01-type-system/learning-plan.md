# Type System — План изучения
> Статус: 🟡 в процессе
> Блок: 1/6 | Последняя сессия: 2026-03-05

## Калибровка
- Базовые концепции: ✅ знает value/reference разделение
- Средний уровень: ✅ понимает копирование value types
- Продвинутый: ✅ struct vs class, value equality, аналогия с монетами
→ Начинаем с блока: 1 (основы знает, углубляем)

## Блоки

- [x] **Блок 1: CTS — Common Type System**
  Иерархия типов в .NET: System.Object → System.ValueType → конкретные типы.
  Почему всё наследуется от object. Unified type system.
  Проверка: 2 вопроса

- [ ] **Блок 2: Встроенные типы и числовые нюансы**
  Алиасы (int = System.Int32), размеры типов, checked/unchecked overflow,
  decimal vs double, IEEE 754 ловушки.
  Проверка: 2 вопроса

- [ ] **Блок 3: Enums — внутреннее устройство**
  Underlying type, [Flags], ToString/Parse, битовые операции.
  Связь: value type, наследует System.Enum → System.ValueType.
  Проверка: 2 вопроса

- [ ] **Блок 4: Boxing и Unboxing**
  Механизм, где происходит в реальном коде, performance implications,
  как избежать. Связь: CTS hierarchy (блок 1).
  Проверка: 3 вопроса

- [ ] **Блок 5: Приведение типов и pattern matching**
  Implicit/explicit cast, as/is, pattern matching (is Type x),
  switch expressions, IConvertible. Связь: CTS hierarchy.
  Проверка: 2 вопроса

- [ ] **Блок 6: Практика + итоговая проверка**
  Задачи на все блоки, 5 вопросов возрастающей сложности.
