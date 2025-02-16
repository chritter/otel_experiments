from flask import Flask, jsonify
from flask import Flask, jsonify, request
from opentelemetry import trace
import requests
from opentelemetry.propagate import inject, extract


from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()


app = Flask(__name__)

@app.route('/more_data', methods=['GET'])
def more_data():
    
    # current_span = trace.get_current_span()
    # if current_span:
    #     print(f"Active Span Before Forwarding: Trace ID = {current_span.get_span_context().trace_id}, Span ID = {current_span.get_span_context().span_id}")
   
    #headers = {key: value for key, value in request.headers.items()}
    #print(f"[Backend2] Incoming Headers: {headers}")
   
    # Extract trace context from incoming request
    context = extract(request.headers)

    tracer = trace.get_tracer(__name__)
    
    # Start a span within the existing trace context
    with tracer.start_as_current_span("backend-2-processing", context=context):
        current_span = trace.get_current_span()
        print(f"[Backend2] Active Span: Trace ID = {current_span.get_span_context().trace_id}, Span ID = {current_span.get_span_context().span_id}")

        return jsonify({'data': 'Hello from Service 2!'})
   

#    return jsonify({'data': 'Hello from Service 2!'})

if __name__ == '__main__':
    app.run(port=8081)