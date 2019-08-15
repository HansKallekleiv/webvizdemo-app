FROM webviz/base_image:latest
RUN pip install --user requests
COPY --chown=appuser . dash_app
