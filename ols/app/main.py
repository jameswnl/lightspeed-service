"""Entry point to FastAPI-based web service."""

from fastapi import FastAPI

from ols.app.endpoints import feedback, health, ols
from ols.src.ui.gradio_ui import gradioUI
from ols.utils import config

app = FastAPI(
    title="Swagger OpenShift LightSpeed Service - OpenAPI",
    description="""
              OpenShift LightSpeed Service API specification.
                  """,
)

# config = load_config(os.environ.get("OLS_CONFIG_FILE","olsconfig.yaml"))
config.load_config_from_env()
if config.ols_config.enable_debug_ui:
    app = gradioUI(logger=config.default_logger).mount_ui(app)
else:
    config.default_logger.info(
        "Embedded Gradio UI is disabled. To enable set OLS_ENABLE_DEV_UI to True"
    )


def include_routers(app: FastAPI):
    """Include FastAPI routers for different endpoints.

    Args:
        app: The `FastAPI` app instance.
    """
    app.include_router(ols.router, prefix="/v1")
    app.include_router(feedback.router, prefix="/v1")
    app.include_router(health.router)


include_routers(app)