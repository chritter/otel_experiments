from flask import Flask, jsonify, request
import requests
from opentelemetry import trace
from opentelemetry.propagate import inject, extract

from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()


app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    
    # The traceparent header in OpenTelemetry encodes multiple pieces of tracing information in a single string.
    # traceparent = {version}-{trace_id}-{span_id}-{trace_flags}
    # request.headers.get("traceparent") value contains the span ID from the upstream caller, not the new span ID that is created inside the get_data function
    otel_headers = {
        "traceparent": request.headers.get("traceparent"),
        "tracestate": request.headers.get("tracestate"),
    }
    # Print the headers (or use a logger)
    traceparent_header = otel_headers.get("traceparent")

    context = extract(request.headers)  # Extract incoming trace context
    headers = {}
    inject(headers)  # Inject trace context for outgoing request

    print(f"[Backend1] Outgoing Headers to Backend2: {headers}")
    
    context = extract(request.headers)

    tracer = trace.get_tracer(__name__)
    
    # Start a span within the existing trace context
    with tracer.start_as_current_span("backend-1-processing", context=context):
        current_span = trace.get_current_span()
        print(f"[Backend1] Active Span: Trace ID = {current_span.get_span_context().trace_id}, Span ID = {current_span.get_span_context().span_id}")
        response = requests.get('http://localhost:8081/more_data', headers=headers)
        return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=8080)