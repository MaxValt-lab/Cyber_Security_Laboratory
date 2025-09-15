# 📱 Создание APK для Cyber Security Laboratory

## Созданные файлы для сборки APK

### 1. Структура проекта
```
apk_build/
├── src/main/
│   ├── AndroidManifest.xml
│   ├── java/org/cyberseclab/app/MainActivity.java
│   ├── assets/index.html
│   └── res/
└── build.gradle
```

### 2. Методы сборки APK

#### Метод 1: Android Studio (Рекомендуется)
1. Установите Android Studio
2. Откройте проект `apk_build/`
3. Build → Build APK(s)

#### Метод 2: Командная строка (Gradle)
```bash
cd apk_build
./gradlew assembleDebug
```

#### Метод 3: Python автоматизация
```bash
py build_apk.py
```

### 3. Альтернативные методы

#### Buildozer (Linux/WSL)
```bash
# Установка
pip install buildozer

# В директории mobile/
buildozer android debug
```

#### Python-for-Android
```bash
pip install python-for-android
p4a apk --private mobile --package=org.cyberseclab.app --name="CyberSecLab" --version=1.0
```

### 4. Веб-версия APK

Создан WebView APK с HTML интерфейсом:
- Подключение к серверу
- Отправка событий безопасности
- Проверка статуса
- Получение статистики

### 5. Функции мобильного приложения

- 🔗 Подключение к серверу Cyber Security Lab
- 📝 Отправка событий безопасности
- 📊 Просмотр статистики
- ⚡ Проверка статуса сервера
- 📱 Адаптивный интерфейс

### 6. Настройка сервера

Для работы с мобильным приложением:

1. Запустите сервер: `py start.py`
2. Узнайте IP адрес: `ipconfig`
3. В приложении укажите: `http://YOUR_IP:8000`

### 7. Разрешения Android

- `INTERNET` - для сетевых запросов
- `ACCESS_NETWORK_STATE` - для проверки сети

### 8. Требования

- Android 5.0+ (API 21)
- Подключение к интернету
- Доступ к серверу Cyber Security Lab

## Быстрый старт

1. **Создание структуры**: `py create_simple_apk.py`
2. **Сборка**: Откройте `apk_build/` в Android Studio
3. **Установка**: Скопируйте APK на устройство
4. **Настройка**: Укажите IP сервера в приложении