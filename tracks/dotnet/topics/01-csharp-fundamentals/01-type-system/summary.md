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

## Связь с другими темами
- → Value vs Reference (тема #2): углубляет разницу между двумя ветками CTS
- → Garbage Collector (#4): boxing создаёт объекты в куче → GC должен их собрать
- → Generics (#10): созданы во многом для устранения boxing в коллекциях
