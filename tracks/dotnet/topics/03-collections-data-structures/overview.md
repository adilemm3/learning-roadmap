# Collections & Data Structures — Обзор

## Что это
Коллекции .NET — от массивов до Span<T>. Выбор правильной структуры данных для задачи. Понимание коллекций критично для написания эффективного и читаемого кода.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Arrays & Lists | Массивы, List<T>, IReadOnlyList, Array vs List |
| 2 | Dictionary & HashSet | Словари, хэш-множества, GetHashCode/Equals |
| 3 | Concurrent Collections | Потокобезопасные коллекции, ConcurrentDictionary |
| 4 | Span & Memory | Span<T>, Memory<T>, stackalloc, производительность |
| 5 | Custom Collections | Создание своих коллекций, IEnumerable<T>, итераторы |

## Порядок изучения
Generics → Arrays & Lists → Dictionary & HashSet
Threads → Concurrent Collections
Memory: Stack & Heap + Arrays & Lists → Span & Memory
Generics + Interfaces → Custom Collections

## Связи с другими разделами
Зависит от Generics, Interfaces. Используется везде. Concurrent Collections требует знания Threads.
