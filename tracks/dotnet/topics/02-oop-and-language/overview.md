# OOP & Language Features — Обзор

## Что это
Объектно-ориентированное программирование и продвинутые возможности языка — от наследования до Expression Trees. Этот раздел охватывает ключевые механизмы, которые делают C# мощным и выразительным языком.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Inheritance & Polymorphism | Наследование, виртуальные методы, переопределение |
| 2 | Interfaces & Abstract | Интерфейсы, абстрактные классы, default interface methods |
| 3 | Generics | Обобщения, constraints, ковариантность/контравариантность |
| 4 | Delegates & Events | Делегаты, события, Action/Func, лямбды |
| 5 | LINQ | Language Integrated Query, отложенное выполнение, IEnumerable |
| 6 | Expression Trees | Деревья выражений, компиляция, IQueryable |
| 7 | Reflection | Рефлексия, атрибуты, динамическая генерация |
| 8 | Iterators & yield | IEnumerable<T> через yield, ленивые последовательности |
| 9 | Covariance & Contravariance | out/in в обобщениях, IEnumerable<out T>, IComparer<in T> |

## Порядок изучения
Inheritance & Polymorphism → Interfaces & Abstract → Generics
Type System → Delegates & Events
Delegates & Events + Generics → LINQ
LINQ + Delegates & Events → Expression Trees
Type System + Generics → Reflection
Generics + Interfaces → Iterators & yield
Generics + Interfaces → Covariance & Contravariance

## Связи с другими разделами
Связан с C# Fundamentals (типы). LINQ используется в Collections, EF Core, Async. Delegates — основа для Events и Async.
