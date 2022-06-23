from aws_cdk import (
    aws_apigateway as apigw,
)

from constructs import Construct


class ApiModels(Construct):

    def __init__(self, scope: Construct, construct_id: str, api: apigw.RestApi) -> None:
        super().__init__(scope, construct_id)

        # /sample GET Response
        self.res_sample_output = apigw.Model(
            self,
            "SampleOutput",
            rest_api=api,
            model_name="SampleListOutput",
            content_type="application/json",
            schema=apigw.JsonSchema(
                schema=apigw.JsonSchemaVersion.DRAFT4,
                title="SampleListOutputModel",
                type=apigw.JsonSchemaType.ARRAY,
                items=apigw.JsonSchema(
                    ref="#/definitions/Sample"
                ),
                definitions={
                    "Sample": apigw.JsonSchema(
                        type=apigw.JsonSchemaType.OBJECT,
                        properties={
                            "title": apigw.JsonSchema(type=apigw.JsonSchemaType.STRING),
                            "description": apigw.JsonSchema(type=apigw.JsonSchemaType.STRING),
                            "category": apigw.JsonSchema(type=apigw.JsonSchemaType.STRING),
                            "view": apigw.JsonSchema(type=apigw.JsonSchemaType.INTEGER),
                            "tag": apigw.JsonSchema(
                                type=apigw.JsonSchemaType.ARRAY,
                                items=apigw.JsonSchema(
                                    type=apigw.JsonSchemaType.STRING
                                )
                            ),
                        }
                    )
                }
            )
        )

        # /sample POST Request
        self.req_sample_input = apigw.Model(
            self,
            "SampleInput",
            rest_api=api,
            model_name="SampleInput",
            content_type="application/json",
            schema=apigw.JsonSchema(
                schema=apigw.JsonSchemaVersion.DRAFT4,
                title="SampleInputModel",
                type=apigw.JsonSchemaType.OBJECT,
                properties={
                    "title": apigw.JsonSchema(type=apigw.JsonSchemaType.STRING),
                    "description": apigw.JsonSchema(type=apigw.JsonSchemaType.STRING),
                    "category": apigw.JsonSchema(type=apigw.JsonSchemaType.STRING),
                    "tag": apigw.JsonSchema(
                        type=apigw.JsonSchemaType.ARRAY,
                        items=apigw.JsonSchema(
                            type=apigw.JsonSchemaType.STRING
                        )
                    ),
                }
            )
        )
