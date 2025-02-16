export OTEL_PYTHON_AUTO_INSTRUMENTATION_ENABLED=true


export FLASK_APP=service_two.py


# opentelemetry-instrument \
#     --traces_exporter console \
#     --metrics_exporter none \
#     --logs_exporter console \
#     --service_name service-two \
#     flask run -p 8081

# using jaeger
# export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
# export OTEL_EXPORTER_OTLP_PROTOCOL=grpc  # Jaeger uses gRPC on 4317
# opentelemetry-instrument \
#     --traces_exporter otlp \
#     --metrics_exporter none \
#     --logs_exporter none \
#     --service_name service-two \
#     flask run -p 8081

# using elastic
# defines resource attributes at runtime. 
# Example: service.name=shoppingcard indicates that the telemetry is coming from a service called "shoppingcard."
source ../.env 
export OTEL_RESOURCE_ATTRIBUTES="service.name=service-two,service.version=1.0,deployment.environment=dev"
opentelemetry-instrument \
    --traces_exporter otlp \
    --metrics_exporter otlp \
    --logs_exporter otlp \
    --service_name service-two \
    flask run -p 8081