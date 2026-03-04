# Qwen2.5-72B-Instruct on RunPod

## Деплой на RunPod

### 1. Создай GPU Pod

1. Зайди на [runpod.io](https://runpod.io) → **GPU Pods** → **Deploy**
2. Выбери шаблон: **RunPod vLLM**
3. GPU: **1x A100 80GB** — AWQ квантизация, ~36GB VRAM
4. В настройках шаблона укажи переменные окружения:

```
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct-AWQ
TENSOR_PARALLEL_SIZE=1
MAX_MODEL_LEN=32768
GPU_MEMORY_UTILIZATION=0.95
QUANTIZATION=awq
```

5. Нажми **Deploy**

### 2. Дождись загрузки

- Модель ~140GB, загрузка займёт 10-20 минут
- В логах пода увидишь `Uvicorn running on http://0.0.0.0:8000`
- Это значит модель готова

### 3. Получи URL

В панели пода будет **Connect** → скопируй публичный URL.
Формат: `https://<pod-id>-8000.proxy.runpod.net/v1`

## Использование

### Установи зависимости

```bash
pip install -r requirements.txt
```

### Быстрый тест

```bash
python test_model.py https://<pod-id>-8000.proxy.runpod.net/v1
```

### Тест с Excel файлом

```bash
python test_excel.py https://<pod-id>-8000.proxy.runpod.net/v1 your_file.xlsx
```

### Через curl

```bash
curl https://<pod-id>-8000.proxy.runpod.net/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-72B-Instruct-AWQ",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 512
  }'
```

### Через Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://<pod-id>-8000.proxy.runpod.net/v1",
    api_key="not-needed",
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-72B-Instruct-AWQ",
    messages=[{"role": "user", "content": "Привет!"}],
)
print(response.choices[0].message.content)
```

## Смена модели

Просто поменяй `MODEL_NAME` в настройках пода и перезапусти:

```
MODEL_NAME=meta-llama/Llama-3.1-70B-Instruct
```

или для моделей поменьше (быстрее, дешевле):

```
MODEL_NAME=Qwen/Qwen2.5-32B-Instruct
TENSOR_PARALLEL_SIZE=1          # хватит 1x A100
```

## Стоимость

| GPU | Цена/час | Подходит для |
|-----|----------|--------------|
| 1x A100 80GB | ~$1.7/hr | 72B AWQ, 32B FP16 |
| 1x A40 48GB | ~$0.7/hr | 32B AWQ, 7B-14B FP16 |
| 1x RTX 4090 24GB | ~$0.4/hr | 7B FP16 |

**Не забудь остановить Pod после тестирования!**
