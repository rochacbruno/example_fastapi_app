# Metrics API

Esta é uma aplicação de exemplo,
criada apenas para ser usada como demonstação.


## Rodando em Container

```bash
docker build -t metrics -f Dockerfile .
docker run --net=host --rm -it metrics
```

## Rodando local com UV

Instale o UV.

```bash
uv sync  
uv run uvicorn main:app --host 0.0.0.0 --port 8081
```

## Simulação

```bash
docker run --net=host --rm -it \
-e SIMULATE_HEAVY_LOAD=1 \
-e SIMULATE_UNHEALTHY_BEHAVIOR=1 \
-e SIMULATE_DELAY=1 \
metrics
```

- SIMULATE_HEAVY_LOAD faz com que o `/metrics` tenha spikes aleatorios e demore a responder de vez em quando, util para os testes de carga.

- SIMULATE_UNHEALTHY_BEHAVIOR faz com que aleatoriamente os health e ready probes retornem erro fazendo o k8s parar de enviar trafego para o POD.

- SIMULATE_DELAY faz com que o startup e o liveness tenham delay fazendo o k8s reiniciar o POD ou esperar para enviar trafego.