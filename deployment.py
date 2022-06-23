from aws_cdk import Stage, Stack, Tags, Environment
from constructs import Construct

from networking.vpc import VPC
from application.apigw import APIGw
from application.lambdas import LambdaFunc
from application.s3 import S3Bucket


class SwaggerUI(Stage):
    def __init__(self, scope: Construct, id_: str, env: Environment, tags: dict, **kwargs) -> None:
        super().__init__(scope, id_, **kwargs)
        """
        Stateful  : The resources that are going to lose the data, if it is deleted, or persistent infrastructure like a VPC
        Stateless : The resources that are not going to lose the data, even if it is deleted.
        """

        stateful = Stack(self, "Stateful", env=env)
        for k, v in tags.items():
            Tags.of(stateful).add(k, v)

        cidr = "172.50.0.0/16"
        vpc = VPC(
            stateful,
            "Networking",
            cidr=cidr
        )

        s3 = S3Bucket(
            stateful,
            "S3"
        )

        stateless = Stack(self, "Stateless", env=env)
        for k, v in tags.items():
            Tags.of(stateless).add(k, v)

        api = APIGw(
            stateless,
            "APIGw",
        )

        LambdaFunc(
            stateless,
            "LambdaFunc",
            vpc=vpc.vpc,
            sg=vpc.sg,
            bucket=s3.bucket,
            api_gw=api.api_gw,
            api_models=api.api_models
        )


