 ## Установка и запуск

```bash
pip install -r requirements.txt
python -m alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```

## Запуск тестов

```bash
python -m pytest tests/ -v
```
