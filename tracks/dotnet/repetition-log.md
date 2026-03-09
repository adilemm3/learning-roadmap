# Повторения — .NET/C#

> Лог spaced repetition сессий. Claude генерирует уникальные вопросы по завершённым темам при startup.
> Интервалы: 7 → 14 → 30 дней. При ❌ — сброс интервала до 7 дней.

---

<!-- Формат записи:

## YYYY-MM-DD
> Темы в пуле повторения: [список тем с количеством дней]

1. [Тема1 + Тема2] Вопрос
   ✅ / ❌ → краткий комментарий

### Результат
- Верно: N/M
- Регрессии → weak-spots.md: [список]
-->

## 2026-03-09
> Темы в пуле повторения: HTTP Clients & IHttpClientFactory (3 дня)

1. [HTTP Clients] Почему нельзя new HttpClient() — socket exhaustion + DNS staleness?
   ✅ → Ответил верно, знает обе проблемы
2. [HTTP Clients] Named vs Typed clients — отличия и когда что?
   ✅ → Понимает разницу, упомянул типобезопасность и инкапсуляцию
3. [HTTP Clients] Что такое DelegatingHandler и зачем?
   ❌ → Не знал, возможно не проходили в сессии

### Результат
- Верно: 2/3
- Регрессии → weak-spots.md: DelegatingHandler (HTTP middleware chain)
