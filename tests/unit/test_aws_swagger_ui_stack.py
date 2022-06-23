import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_swagger_ui.aws_swagger_ui_stack import AwsSwaggerUiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_swagger_ui/aws_swagger_ui_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsSwaggerUiStack(app, "aws-swagger-ui")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
