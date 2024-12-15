# Genetic Tests API

## Установка
1. Клонируйте репозиторий.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройте базу данных в settings.py.
4. Примените миграции:
    ```bash
    python manage.py migrate
    ```

5. Запуск сервера
    ```bash
    python manage.py runserver
    ```

##Примеры запросов
1. Добавление теста:
    ```bash
    POST /api/tests
    Content-Type: application/json
    {
    "animal_name": "Буренка",
    "species": "корова",
    "test_date": "2023-11-18",
    "milk_yield": 28.5,
    "health_status": "good"
    }
    ```
2. Получение всех записей:
    ```bash
    GET /api/tests
    ```
3. Получение отфильтрованных записей:
    ```bash
    GET /api/tests?species=корова
    ```
4. Получение статистики:
    ```bash
    GET /api/statistics
    ```