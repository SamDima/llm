FROM vllm/vllm-openai:latest

ENV MODEL_NAME=Qwen/Qwen2.5-72B-Instruct-AWQ
ENV TENSOR_PARALLEL_SIZE=1
ENV QUANTIZATION=awq
ENV MAX_MODEL_LEN=32768
ENV GPU_MEMORY_UTILIZATION=0.95

EXPOSE 8000

CMD python -m vllm.entrypoints.openai.api_server \
    --model ${MODEL_NAME} \
    --tensor-parallel-size ${TENSOR_PARALLEL_SIZE} \
    --max-model-len ${MAX_MODEL_LEN} \
    --gpu-memory-utilization ${GPU_MEMORY_UTILIZATION} \
    --quantization ${QUANTIZATION} \
    --trust-remote-code \
    --host 0.0.0.0 \
    --port 8000
