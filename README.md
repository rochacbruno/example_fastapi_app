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

## Outras branches

- simulation = branch contendo simulações de carga e endpoints para o k8s
- testes = branch contendo testes e CI