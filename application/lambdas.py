from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_apigateway as apigw,
)
from constructs import Construct
from application.models import ApiModels


class LambdaFunc(Construct):

    def __init__(self, scope: Construct, id_: str, api_gw: apigw.RestApi, api_models: ApiModels,
                 vpc: ec2.Vpc, sg: ec2.SecurityGroup, bucket: s3.Bucket) -> None:
        super().__init__(scope, id_)

        # Lambda Layer
        layer = lambda_.LayerVersion(
            self,
            "APIDocsLayer",
            code=lambda_.Code.from_asset("layers/swagger.zip"),
            compatible_runtimes=[lambda_.Runtime.NODEJS_14_X],
            description="serverless-http, swagger-ui-express",
            layer_version_name="serverless-swagger-ui",
        )

        # API Docs Lambda
        api_docs_func = lambda_.Function(
            self,
            "APIDocsLambda",
            function_name="APIDocsFunc",
            handler="index.handler",
            runtime=lambda_.Runtime.NODEJS_14_X,
            code=lambda_.Code.from_asset('lambdas/nodejs'),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
            ),
            security_groups=[sg],
            layers=[layer],
            environment={
                "BUCKET_NAME": "",
                "KEY_NAME": "",
            }
        )

        # Add inline policy
        api_docs_func.role.attach_inline_policy(
            policy=iam.Policy(
                self,
                "S3AccessPolicy",
                document=iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "s3:GetObject"
                            ],
                            resources=[
                                bucket.bucket_arn,
                                f"{bucket.bucket_arn}/*"
                            ]
                        )
                    ]
                ),
                policy_name="s3-access-policy"
            )
        )

        # Integrate Lambda to API Gateway
        api_docs = api_gw.root.add_resource("api-docs")
        api_docs.add_method(
            http_method="GET",
            integration=apigw.LambdaIntegration(api_docs_func)
        )

        proxy_plus = api_docs.add_proxy(
            any_method=False,
        )
        proxy_plus.add_method(
            http_method="GET",
            integration=apigw.LambdaIntegration(api_docs_func)
        )

        # Sample API Lambda
        sample_func = lambda_.Function(
            self,
            "SampleLambda",
            function_name="SampleFunc",
            handler="lambda_handler.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('lambdas/python'),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
            ),
            security_groups=[sg]
        )

        # Integrate Lambda to API Gateway
        sample_api = api_gw.root.add_resource("sample")
        sample_api.add_method(
            http_method="GET",
            integration=apigw.LambdaIntegration(sample_func),
            method_responses=[
                apigw.MethodResponse(
                    status_code="200",
                    response_models={
                        "application/json": api_models.res_sample_output
                    }
                )
            ],
        )
        sample_api.add_method(
            http_method="POST",
            integration=apigw.LambdaIntegration(sample_func),
            request_models={
                "application/json": api_models.req_sample_input
            },
        )
