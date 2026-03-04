# .NET Internals — Обзор

## Что это
Внутреннее устройство .NET — CLR, JIT, сборка мусора на низком уровне, модель потоков. Глубокое понимание рантайма, необходимое для Senior-уровня и оптимизации производительности.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | CLR & JIT | Common Language Runtime, Just-In-Time компиляция, AOT |
| 2 | Assembly Loading | Загрузка сборок, AssemblyLoadContext, плагины |
| 3 | GC Internals | Устройство GC, поколения, LOH, pinning, GC modes |
| 4 | Threading Model | Модель потоков .NET, ThreadPool internals, I/O completion ports |
| 5 | Performance Diagnostics | dotnet-trace, dotnet-dump, BenchmarkDotNet, PerfView |

## Порядок изучения
CLR & JIT → Assembly Loading
CLR & JIT + Garbage Collector → GC Internals
CLR & JIT + Threads → Threading Model
GC Internals + Threading Model → Performance Diagnostics

## Связи с другими разделами
Требует глубокого понимания C# Fundamentals и Async. Знания отсюда помогают в оптимизации и профилировании.
