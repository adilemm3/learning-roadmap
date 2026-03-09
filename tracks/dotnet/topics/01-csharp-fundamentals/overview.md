# C# Fundamentals — Обзор

## Что это
Основы языка C# — система типов, работа с памятью, строки, исключения. Фундамент для всего остального. Без твёрдого понимания этих концепций невозможно эффективно писать код на C# и понимать, что происходит под капотом.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Type System | Система типов C#: примитивные, ссылочные, boxing/unboxing |
| 2 | Value vs Reference | Различия value и reference типов, передача параметров |
| 3 | Memory: Stack & Heap | Модель памяти, стек и куча, время жизни объектов |
| 4 | Garbage Collector | Сборка мусора, поколения, финализаторы |
| 5 | Strings & Immutability | Строки, неизменяемость, StringBuilder, интернирование |
| 6 | Exceptions | Исключения, иерархия, try/catch/finally, создание своих |
| 7 | Nullable | Nullable types, null-safety, операторы ?. ?? ??= |
| 8 | Extension Methods | Extension methods, цепочки вызовов, fluent API |
| 9 | Pattern Matching | switch expressions, is/when, C# 8–12 паттерны |
| 10 | Records & Structs | record types, primary constructors, with expressions |

## Порядок изучения
Type System → Value vs Reference → Memory: Stack & Heap → Garbage Collector
Value vs Reference → Strings & Immutability
Type System → Exceptions
Value vs Reference → Nullable
Type System + Interfaces → Extension Methods
Type System + Value vs Reference → Pattern Matching
Value vs Reference + Type System → Records & Structs

## Связи с другими разделами
Лежит в основе всех последующих разделов. Напрямую связан с OOP, Collections, .NET Internals.
