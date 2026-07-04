from fastapi.openapi.utils import get_openapi


def setup_openapi(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=getattr(app, "version", "1.0.0"),
            routes=app.routes,
        )

        for component in schema.get("components", {}).get("schemas", {}).values():
            props = component.get("properties", {})
            for key, field in props.items():
                if key in ("file", "files", "image") and field.get("type") == "array":
                    items = field.get("items", {})
                    items["type"] = "string"
                    items["format"] = "binary"
                elif key in ("file", "image") and field.get("type") == "string":
                    field["format"] = "binary"

        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi
