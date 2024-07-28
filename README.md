# Набор моих утилит

## Декораторы

### ratelimit

Декоратор для ограничения количества вызовов функции в секунду.

```python
from wrng.decorators import ratelimit

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
from wrng.decorators import timeout

@timeout(2)
def my_function():
    time.sleep(3)
    print("Функция завершилась")
```

### retry

Декоратор для повторного выполнения функции в случае исключения.

```python
from wrng.decorators import retry

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
from wrng.decorators import timer

logger = logging.getLogger(__name__)

@timer(logger)
def my_function():
    time.sleep(1)
    print("Функция завершилась")
```

### return_stub
```python
from wrng.decorators import return_stub
from wrng.decorators.return_stub import ModeType

@return_stub(42, mode=ModeType.Fail)
def my_function(raise_exception=False):
    if raise_exception:
        raise ValueError("Произошла ошибка")
    return 'kek'
    
assert my_function() == 'kek'
assert my_function(raise_exception=True) == 42
```

## Контекстные менеджеры

### timer

Контекстный менеджер для измерения времени выполнения блока кода.

```python
from wrng.context_managers import timer

with timer(seconds=2):
    time.sleep(1)
    print("Блок кода завершился")
```
