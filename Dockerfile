FROM docker.io/library/python:3.12-slim
# meta
ARG IMAGE_VERSION=0.0.1
LABEL authoritative-source-url="docker.repo.usaa.com" \
    io.k8s.display-name="pipeline-ops-mcp" \
    io.k8s.description="Python Fast API for Pipeline Operations MCP" \
    description="Python Fast API for Pipeline Operations MCP" \
    name="usaa/pipeline-ops-mcp" \
    image-version=${IMAGE_VERSION} \
    summary="Python Fast API for Pipeline Operations MCP" \
    io.openshift.tags="mcp"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --create-home appuser

COPY --chown=appuser:appuser src/app.py src/

USER appuser

EXPOSE 8000

CMD ["python", "src/app.py"]