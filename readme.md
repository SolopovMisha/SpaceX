# Космический Телеграм

Бот для Telegram, который автоматически публикует космические изображения из различных источников (NASA APOD, NASA EPIC, SpaceX) с заданным интервалом. Изображения загружаются, сохраняются локально и отправляются в указанный чат.

## Как установить

1. **Клонируйте репозиторий:**
   ```bash
   git clone [ваш репозиторий]
   cd [папка проекта]
   ```

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Получите API-ключи:**
   - **NASA API**: Зарегистрируйтесь на [NASA API Portal](https://api.nasa.gov/) и получите ключ.
   - **Telegram Bot Token**: Создайте бота через [BotFather](https://t.me/BotFather) и сохраните токен.
   - **Chat ID**: Узнайте ID чата, куда бот будет отправлять сообщения (можно использовать бота @userinfobot).

4. **Создайте файл `.env`** в корне проекта и добавьте ключи:
   ```plaintext
   api_token=ваш_ключ_NASA
   TELEGRAM_BOT_TOKEN=ваш_токен_бота_Telegram
   TELEGRAM_CHAT_ID=ваш_ID_чата
   ```

5. **Запустите бота:**
   ```bash
   python main.py
   ```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/). Проект демонстрирует работу с API, обработку изображений и интеграцию с Telegram.

## Функционал
- Загрузка изображений от NASA (APOD и EPIC).
- Загрузка последних фотографий запусков SpaceX.
- Автоматическая публикация изображений в Telegram с настраиваемым интервалом.
- Сжатие изображений при необходимости для соответствия ограничениям Telegram.

## Примеры команд
- Для запуска загрузки изображений NASA APOD:
  ```python
  save_apod()
  ```
- Для запуска загрузки изображений NASA EPIC:
  ```python
  save_EPIC()
  ```
- Для загрузки фотографий SpaceX:
  ```python
  fetch_spacex_last_launch("images")
  ```

## Требования
- Python 3.6+
- Зависимости: `requests`, `python-telegram-bot`, `python-dotenv`, `Pillow`
