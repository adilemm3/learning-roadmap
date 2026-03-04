# Testing — Обзор

## Что это
Тестирование — unit, integration, mocking, TDD, нагрузочное тестирование. Охватывает все уровни тестирования, необходимые для создания надёжного и поддерживаемого кода.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Unit Testing | xUnit, FluentAssertions, организация тестов, AAA |
| 2 | Integration Testing | TestServer, TestContainers, базы в тестах |
| 3 | Mocking Strategies | Moq, NSubstitute, моки vs стабы vs фейки |
| 4 | TDD & BDD | Test-Driven Development, Behavior-Driven Development |
| 5 | Load Testing | k6, NBomber, профилирование под нагрузкой |

## Порядок изучения
Dependency Injection + Interfaces → Unit Testing → Integration Testing
Unit Testing → Mocking Strategies
Unit Testing + Mocking Strategies → TDD & BDD
Integration Testing + Performance Diagnostics → Load Testing

## Связи с другими разделами
Зависит от DI, Interfaces. Связан с Architecture (testability), CI/CD.
