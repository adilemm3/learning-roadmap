# Type System
> Уровень: Junior
> Зависимости: нет (корневая тема)

## Ключевые концепции

### Блок 1: CTS — Common Type System
- **Unified type system** — все типы наследуются от `System.Object`
- Иерархия: `Object` → `ValueType` → конкретные struct/enum
- `System.ValueType` сам является reference type (class), но CLR обрабатывает его наследников как value types
- `string` — reference type, но ведёт себя как value type благодаря переопределённому `==` и immutability
- Каждый struct неявно наследует `ValueType`, хотя struct нельзя наследовать явно

## Примеры кода
```csharp
typeof(int).BaseType;             // System.ValueType
typeof(int).BaseType.BaseType;    // System.Object
typeof(string).BaseType;          // System.Object
typeof(int).IsValueType;          // True
typeof(string).IsValueType;       // False
```

## Частые вопросы на собесе
<!-- Q&A формат — заполняется при завершении темы -->

## Подводные камни и нюансы
- `ValueType` — class, не struct (частая ловушка)
- Boxing: value type → object = heap allocation + копирование + GC pressure
- `ArrayList` боксит каждый value type, `List<T>` — нет (generics решают проблему)

## Блок 2: Встроенные типы и числовые нюансы

### Ключевые концепции
- Все числовые типы — struct'ы (value types), хранятся на стеке
- Псевдонимы: int = System.Int32, long = System.Int64 и т.д.
- Полная таблица: sbyte, short, int, long, nint (знаковые); byte, ushort, uint, ulong, nuint (беззнаковые); float, double, decimal; bool, char; string/object (reference types)
- nint/nuint — C# 9, для interop и низкоуровневой работы с памятью

### Overflow
- По умолчанию unchecked — переполнение оборачивается тихо (byte: 255 + 1 = 0)
- checked — бросает OverflowException
- unchecked — явное разрешение переполнения (хэш-алгоритмы)

### decimal vs double
- double: IEEE 754, аппаратная поддержка через FPU, 0.1 = бесконечная двоичная дробь → ошибки округления
- decimal: десятичное хранение, программная арифметика, точно 0.1 = 0.1, в 10-20x медленнее
- double → физика/графика/ML; decimal → деньги/финансы

## Связь с другими темами
- → Value vs Reference (тема #2): углубляет разницу между двумя ветками CTS
- → Garbage Collector (#4): boxing создаёт объекты в куче → GC должен их собрать
- → Generics (#10): созданы во многом для устранения boxing в коллекциях

## Блок 3: Enums — внутреннее устройство (в процессе, 2026-03-08)

### Ключевые концепции

- **Enum — value type**: наследует System.Enum → System.ValueType → System.Object
- **Underlying type**: по умолчанию `int`; можно указать любой целочисленный тип (`byte`, `short` и т.д.)
- **Implicit values**: без явных значений — 0, 1, 2, ...
- **ToString("D")** → числовое значение; `ToString()` → имя константы
- **Enum.Parse<T>()** → строка → enum; **Enum.IsDefined()** → проверка валидности
- **Cast не валидирует**: `(TrafficLight)99` не бросает исключение → использовать Enum.IsDefined() для внешних данных

### [Flags] — битовые маски

- Значения должны быть степенями двойки (каждый бит — отдельный флаг)
- Комбинация: `Read | Write` (bitwise OR)
- Проверка: `(user & Permissions.Read) != 0` (bitwise AND)
- `HasFlag()` — удобнее, но медленнее (boxing)
- `ToString()` с [Flags] возвращает "Read, Write" вместо числа

### Код

```csharp
public enum TrafficLight { Red, Yellow, Green }
public enum StatusCode : short { Ok = 200, NotFound = 404 }

[Flags]
public enum Permissions { None=0, Read=1, Write=2, Execute=4, Admin=8 }

// Комбинирование
Permissions user = Permissions.Read | Permissions.Execute; // = 5

// Проверка (производительный вариант)
bool canRead = (user & Permissions.Read) != 0;

// Валидация внешних данных
if (Enum.IsDefined(typeof(TrafficLight), input))
    TrafficLight safe = (TrafficLight)input;
```
