# Async & Multithreading — Обзор

## Что это
Асинхронное и многопоточное программирование — потоки, Task, async/await, синхронизация. Один из ключевых разделов для Middle-разработчика, без которого невозможно писать производительные серверные приложения.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Threads & ThreadPool | Потоки, пул потоков, Thread vs ThreadPool |
| 2 | Task & async/await | Task, async/await, ConfigureAwait, ValueTask |
| 3 | Synchronization Primitives | lock, Monitor, SemaphoreSlim, ReaderWriterLockSlim |
| 4 | Parallel & PLINQ | Parallel.ForEach, PLINQ, параллелизм vs конкурентность |
| 5 | Channels | System.Threading.Channels, producer-consumer |
| 6 | Cancellation Patterns | CancellationToken, паттерны отмены |

## Порядок изучения
Threads & ThreadPool → Task & async/await → Synchronization Primitives
Task & async/await + LINQ → Parallel & PLINQ
Task & async/await → Channels
Task & async/await → Cancellation Patterns

## Связи с другими разделами
Зависит от Memory, Delegates. Используется в ASP.NET Core, EF Core, System Design. Synchronization Primitives связаны с .NET Internals.
