''' Configurations for Swagger  '''

template = {
    "swagger": "2.0",
    "info": {
        "title": "Classroom Monitoring Using AI APIs",
        "description": "APIs",
        "contact": {
            "responsibleOrganization": "AUC",
            "responsibleDeveloper": "Mohamed Ashraf Taha",
            "email": "mohammedashraf@aucegypt.edu",
            "url": "/api",
        },
        "termsOfService": "",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}