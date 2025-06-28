import psutil
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()


class SystemMetrics(BaseModel):
    memoria: float  # Uso de memória em %
    cpu: float  # Uso de CPU em %
    disk: float  # Uso de disco em %


@app.get("/metrics", response_model=SystemMetrics, tags=["main"])
def get_system_metrics():
    memory = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage("/").percent
    return SystemMetrics(memoria=memory, cpu=cpu, disk=disk)


@app.get("/", tags=["util"])
def redirect_to_docs():
    return RedirectResponse(url="/docs")
