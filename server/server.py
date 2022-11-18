from flask import Flask
import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

OTLP_ENDPOINT=os.getenv('OTLP_URI')

resource = Resource(attributes={
    SERVICE_NAME: "server-api"
})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

users=[
    {
        "id":1,
        "name":"john",
        "age":20
    },
    {
        "id":2,
        "name":"Alice",
        "age":40
    },
    {
        "id":3,
        "name":"Ronny",
        "age":25
    },
    {
        "id":4,
        "name":"Madelaine",
        "age":23
    }
]

@app.route("/health")
def check_health():
    return {"message":"ok"}


@app.route("/user")
def get_data():
    return users


if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)