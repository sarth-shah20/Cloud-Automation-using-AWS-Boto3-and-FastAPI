from fastapi import FastAPI
from ec2_automation import launch_instance, get_output, terminate_instance

app = FastAPI()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Cloud Automator API!"}

@app.get("/run-script")
def run_script():
    instance_id, dns = launch_instance()
    output = get_output(instance_id)
    terminate_instance(instance_id)
    return {
        "instance_id": instance_id,
        "dns": dns,
        "output": output
    }
