# Experiments of monitoring GenAI Applications with OpenTelemetry


## SEtup

* pip install opentelemetry-distro
* opentelemetry-bootstrap -a install: detects necessary tools. Scans the Environment: Analyzes the installed packages in your Python environment to identify libraries that have corresponding OpenTelemetry instrumentation available.

### setting up otel collector

    docker run -p 4317:4317 \
        -v otel-collector-config.yaml:/etc/otel-collector-config.yaml \
        otel/opentelemetry-collector:latest \
        --config=/etc/otel-collector-config.yaml
