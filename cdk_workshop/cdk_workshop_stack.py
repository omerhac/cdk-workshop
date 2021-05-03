from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    core
)
from hitcounter import HitCounter
from cdk_dynamo_table_viewer import TableViewer

class CdkWorkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_handler = _lambda.Function(self, 'HelloHandler', runtime=_lambda.Runtime.PYTHON_3_8,
                                         code=_lambda.Code.asset('lambda'), handler='hello.handler')
        hitcount_hello = HitCounter(self, 'HitCounterHello', downstream=hello_handler)
        hello_api = apigw.LambdaRestApi(self, 'HelloHandlerAPI', handler=hitcount_hello.handler)

        table_viewer = TableViewer(self, 'HitCountTableViewer', table=hitcount_hello.table)
        #hitcount_hello.table.grant_read_data(table_viewer)
