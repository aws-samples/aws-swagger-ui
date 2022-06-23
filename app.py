#!/usr/bin/env python3
import os
import aws_cdk as cdk

from deployment import SwaggerUI

app = cdk.App()

SwaggerUI(
    app,
    "SwaggerUI",
    env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]),
    tags={"Owner": "swagger"}
)


app.synth()

