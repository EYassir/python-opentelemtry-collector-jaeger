from flask import Flask
import requests
import os
import time
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

SERVER_ENDPOINT=os.getenv('SERVER_URI')
OTLP_ENDPOINT=os.getenv('OTLP_URI')

resource = Resource(attributes={
    SERVICE_NAME: "client-api"
})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/health")
def check_health():
    return {"message":"ok"}

@app.route("/data")
def get_data():
    resp=requests.get(SERVER_ENDPOINT+"/user")
    return resp.text

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)