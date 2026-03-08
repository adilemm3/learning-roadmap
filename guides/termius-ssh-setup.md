# Claude Code с телефона (macOS)
> Управляй Mac-терминалом с iPhone/Android — учись где угодно
>
> ⚠️ Гайд написан для macOS. Windows не поддерживает tmux без WSL.

**Схема:** Телефон (Termius) → Tailscale VPN → Mac (SSH) → Claude CLI

---

## Что такое эти приложения

### Tailscale — VPN-сеть между твоими устройствами

Mesh VPN, который соединяет твои устройства в приватную сеть. Каждое устройство получает постоянный IP (`100.x.x.x`), доступный из любой сети — домашний Wi-Fi, мобильный интернет, кафе, другая страна. Без Tailscale пришлось бы пробрасывать порты, настраивать DDNS и разбираться с NAT. Tailscale делает это автоматически.

- Бесплатный план — до 100 устройств
- Трафик идёт напрямую между устройствами (peer-to-peer), не через сервер
- Шифрование WireGuard

> ⚠️ **Tailscale + корпоративный VPN (Zscaler, GlobalProtect и т.д.)** — могут конфликтовать. Оба перехватывают сетевой трафик. Если корпоративный VPN в режиме tunnel-all, Tailscale может не установить соединение. Решение зависит от IT-политик компании.

### Termius — SSH-клиент для телефона

Мобильное приложение для подключения к серверам по SSH. По сути — терминал на телефоне. Сохраняет хосты, пароли, ключи. Бесплатной версии достаточно.

### tmux — мультиплексор терминала

Утилита, которая создаёт сессии терминала, живущие на Mac независимо от подключения. Два сценария:

- **Продолжить сессию:** начал на Mac → закрыл → подключился с телефона → всё на месте
- **Общий экран:** Mac и телефон подключены к одной сессии одновременно — оба видят и печатают в одно окно

Без tmux при отключении SSH весь вывод терминала теряется.

---

## Что понадобится

| Где | Что установить |
|-----|---------------|
| **Mac** | Включить SSH + установить [Tailscale](https://tailscale.com/download/mac) |
| **Телефон** | [Termius](https://termius.com) + Tailscale ([iOS](https://apps.apple.com/app/tailscale/id1470499037) / [Android](https://play.google.com/store/apps/details?id=com.tailscale.ipn.android)) |

---

## Настройка Mac (один раз)

### 1. Включить SSH

**System Settings → General → Sharing → Remote Login** — включить.

Проверка:
```bash
sudo systemsetup -getremotelogin
# Remote Login: On
```

### 2. Установить Tailscale

1. Скачай с [tailscale.com/download/mac](https://tailscale.com/download/mac)
2. Запусти → **Log in** → войди через Google или GitHub
3. Запомни свой Tailscale IP:

```bash
tailscale ip -4
# Например: 100.94.183.79
```

> ⚠️ Tailscale IP начинается с `100.x.x.x` и не меняется.

### 3. Подготовить tmux (для общих сессий)

```bash
brew install tmux
```

---

## Настройка телефона (один раз)

### 1. Установить Tailscale

- **iOS** — [Tailscale из App Store](https://apps.apple.com/app/tailscale/id1470499037)
- **Android** — [Tailscale из Google Play](https://play.google.com/store/apps/details?id=com.tailscale.ipn.android)
- Войди в **тот же аккаунт** что и на Mac

### 2. Настроить Termius

1. Открой Termius → **+** → **New Host**
2. Заполни:

| Поле | Значение |
|------|----------|
| Alias | `Mac` (любое имя) |
| Hostname | `100.x.x.x` (твой Tailscale IP) |
| Port | `22` |
| Username | логин Mac (результат `whoami`) |
| Password | пароль от Mac |

3. **Save** — хост готов

---

## Ежедневное использование

### Подключиться с телефона

1. Убедись что **Tailscale включён** на телефоне (тоггл в приложении)
2. Открой **Termius** → тапни на хост **Mac**
3. Ты в терминале Mac

### Запустить Claude CLI

```bash
cd ~/Documents/myProjects/learning-roadmap
claude
```

> ⚠️ Claude должен быть запущен из папки проекта — иначе он не увидит `CLAUDE.md` и систему обучения.

Если кодировка сломана:
```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 claude
```

### Общая сессия через tmux

Одна сессия — два экрана. Начал на Mac, продолжил с телефона.

**На Mac — создать сессию:**
```bash
tmux new -s main
```

**На телефоне — подключиться:**
```bash
tmux attach -t main
```

> ⚠️ Выйти из tmux не завершая сессию: `Control+B`, затем `D`

---

## Справочник команд

| Команда | Описание |
|---------|----------|
| `tailscale ip -4` | Узнать Tailscale IP |
| `tailscale status` | Проверить статус подключения |
| `claude` | Запустить Claude CLI |
| `tmux new -s main` | Создать tmux-сессию |
| `tmux attach -t main` | Подключиться к существующей сессии |
| `tmux ls` | Список активных сессий |
| `exit` | Выйти из SSH |
