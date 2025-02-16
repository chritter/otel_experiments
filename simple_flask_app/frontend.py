import streamlit as st
import requests
from opentelemetry import trace

from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()


# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.propagate import inject

# # Enable OpenTelemetry for outgoing requests
# RequestsInstrumentor().instrument()

st.title('Front-end Service')

if st.button('Call Back-end Service'):
    # headers = {}
    # inject(headers)  # Inject trace context into headers
    
    current_span = trace.get_current_span()
    if current_span:
        print(f"Active Span Before Forwarding: Trace ID = {current_span.get_span_context().trace_id}, Span ID = {current_span.get_span_context().span_id}")
    
    response = requests.get('http://localhost:8080/data')#, headers=headers)
    st.write(response.text)
