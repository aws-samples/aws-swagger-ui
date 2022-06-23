from aws_cdk import (
    aws_apigateway as apigw,
)
from constructs import Construct
from application.models import ApiModels


class APIGw(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)

        self.api_gw = apigw.RestApi(
            self,
            "APIGw",
            rest_api_name="SwaggerUI",
            description="REST API for Swagger UI",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            ),
            minimum_compression_size=1400
        )

        self.api_models = ApiModels(
            self,
            "ApiModels",
            self.api_gw
        )


