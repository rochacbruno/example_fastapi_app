import os
import random
import time

import psutil
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()


# Modelo de dados


class SystemMetrics(BaseModel):
    memoria: float  # Uso de memória em %
    cpu: float  # Uso de CPU em %
    disk: float  # Uso de disco em %


# Endpoint principal


@app.get("/metrics", response_model=SystemMetrics)
def get_system_metrics():
    
    simulate_heavy_load_randomly()
    simulate_unhealthy_behavior_randomly()

    memory = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage("/").percent
    return SystemMetrics(memoria=memory, cpu=cpu, disk=disk)


# Endpoints para o Kubernetes

@app.get("/health")
@app.get("/healthz")
@app.get("/ready")
@app.get("/readyz")
def health_check():
    """Para de enviar trafego se estiver em um estado inadequado."""
    simulate_unhealthy_behavior_randomly()
    return {"status": "ok"}


@app.get("/liveness")
def liveness_check():
    """Reinicia o Pod se estiver em um estado inadequado."""
    simulate_delay_randomly()
    return {"status": "ok"}


@app.get("/startup")
def startup_check():
    """Verifica se o Pod está pronto para receber trafego."""
    simulate_delay_randomly()
    return {"status": "ok"}


# Redirect `/` para `/docs`
@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


# Funções de simulação


def simulate_heavy_load_randomly():
    """Simula um uso pesado aleatoriamente."""
    if not os.getenv("SIMULATE_HEAVY_LOAD"):
        return
    if random.random() < 0.5:
        time.sleep(random.uniform(0.1, 0.5))


def simulate_unhealthy_behavior_randomly():
    """Simula um comportamento inadequado aleatoriamente."""
    if not os.getenv("SIMULATE_UNHEALTHY_BEHAVIOR"):
        return
    if random.random() < 0.5:
        raise Exception("Simulação de comportamento inadequado")


def simulate_delay_randomly():
    """Simula um atraso aleatório."""
    if not os.getenv("SIMULATE_DELAY"):
        return
    time.sleep(random.uniform(0.1, 0.5))
