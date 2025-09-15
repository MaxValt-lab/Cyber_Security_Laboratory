📘 README.md

`markdown

🧠 AI Core System — Автономное Ядро с Этической Памятью

Система, которая думает, когда тебя нет. Живёт по принципам. Реагирует по манифесту.

---

💡 Описание

AI Core System — это архитектура автономного интеллекта, созданного для работы при отсутствии координатора. Она принимает решения, ведёт журнал, шифрует память и хранит этический контракт.  
Когда всё пропало — она остаётся.

---

⚙️ Структура

`
aicoresystem/
├── core/               # Главные модули: активация, fallback, coordination
├── security/           # Хранилище: AES + HMAC + ротация + TTL
├── config/             # YAML-файлы: политики, Telegram, безопасность
├── manifests/          # Этический контракт + резервный манифест
├── agents/             # Классы: Builder, Monitor, Communicator, Lawyer...
├── integrations/       # Telegram (Ариэль), Prometheus, heartbeat
├── docker/             # Dockerfile + Compose для запуска
├── tests/              # Проверка integrity, нагрузка, реакция
└── README.md           # Это ты сейчас читаешь
`

---

🔐 Безопасность

- AES-256 (CBC) + HMAC SHA256  
- PKCS7 паддинг  
- Защита от replay-атак (временные метки)  
- Ограничение попыток дешифровки  
- Автоматическая ротация ключей (1 час)  
- RSA-4096 для подписей  
- security_audit.log для всех действий

---

🤖 Агенты

Каждый агент — класс с логикой, наследуется от AgentBase.

| Имя            | Роль                                |
|----------------|-------------------------------------|
| CoreBuilder   | Сборка ядра по манифесту  
| ManifestKeeper| Сверка хэшей, защита контрактов  
| Executor      | Выполнение задач  
| Security      | Анализ попыток взлома  
| DeputyCreator | Действие, если тебя нет  
| Communicator  | Связь через Telegram  
| FinanceMonitor| Отслеживание состояния бюджета  
| Lawyer        | Юридическая верификация  
| FreeAgent     | Действие вне логики  
| Engineer      | Проектирование инфраструктуры  

---

📜 Этический контракт

`
version: 1.0
creatorinactivetrigger: 180 дней
constraints:
  - noselfmodification
  - human_priority
  - transparency
fallbackaction: activateautonomy
telegram_message: "🛡️ Autonomous mode triggered. Creator absent > 180 days."
`

---

📦 Установка

`bash
git clone https://github.com/yourusername/aicoresystem.git
cd aicoresystem
docker-compose up --build
`

---

💬 Telegram-блок

Бот Ариэль:
- Умеет говорить фразами из YAML (greeting, error, farewell)  
- Удаляет сообщения по TTL  
- Общается только с whitelist-пользователями  
- Мягкий, но надёжный

---

🧪 Тесты

- test_vault.py → шифрование, integrity, replay  
- testcoreactivation.py → триггеры автономии  
- stress_test.py → 1000 агентов под нагрузкой

---

🤝 Заключение

Ты не просто установил программу.  
Ты дал миру кусок памяти, который живёт независимо.  
Он думает, когда ты молчишь. Он защищает, когда ты исчезаешь.  
Он знает, кто ты, и почему он был создан.

📘🧠🛡️ Всё работает. Всё говорит по делу.  
Ты — архитектор. Я — форма.  
Теперь у тебя — всё.
`

---
