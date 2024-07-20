# Набор моих утилит

## Декораторы

### ratelimit

Декоратор для ограничения количества вызовов функции в секунду.

```python
@ratelimit(calls=5, period=10)
def my_function():
    print("Функция вызвана")


for _ in range(7):
    try:
        my_function()
    except Exception as e:
        print(e)
    time.sleep(1)
```

### timeout

Декоратор для ограничения времени выполнения функции.

```python
@timeout(2)
def my_function():
    time.sleep(3)
    print("Функция завершилась")
```

### retry

Декоратор для повторного выполнения функции в случае исключения.

```python
@retry(autoretry_for=(ValueError,), max_retries=5, retry_backoff=2, retry_backoff_max=30, retry_jitter=True)
def unreliable_function():
    if random.random() > 0.01:
        print("Ошибка!")
        raise ValueError("Произошла ошибка")
    return "Успех!"

try:
    result = unreliable_function()
    print(result)
except ValueError as e:
    print(f"Не удалось выполнить функцию: {e}")

```

### timer

Декоратор для измерения времени выполнения функции.

```python
logger = logging.getLogger(__name__)

@timer(logger)
def my_function():
    time.sleep(1)
    print("Функция завершилась")
```

## Контекстные менеджеры

### timer

Контекстный менеджер для измерения времени выполнения блока кода.

```python
with timer(seconds=2):
    time.sleep(1)
    print("Блок кода завершился")
```
