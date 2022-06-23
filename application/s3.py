from aws_cdk import CfnOutput
from aws_cdk import (
    aws_s3 as s3,
)
from constructs import Construct


class S3Bucket(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)

        # S3 Bucket
        cors_rule = s3.CorsRule(
            allowed_methods=[
                s3.HttpMethods.GET
            ],
            allowed_origins=[
                "*"
            ],
            allowed_headers=[
                "Authorization",
                "Content-Type"
            ],
            max_age=3000
        )

        self.bucket = s3.Bucket(
            self,
            "APIDocs",
            cors=[cors_rule]
        )

        CfnOutput(
            self,
            "BucketName",
            value=self.bucket.bucket_name
        )
