from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    core
)


class HitCounter(core.Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(self, scope, id, downstream, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(self, 'Hits', partition_key={'name': 'path', 'type': ddb.AttributeType.STRING})
        self._handler = _lambda.Function(self, 'HitCountHandler', code=_lambda.Code.asset('lambda'),
                                        handler='hitcount.handler', runtime=_lambda.Runtime.PYTHON_3_8,
                                        environment={
                                            'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                                            'HITS_TABLE_NAME': self.table.table_name
                                        })

        self.table.grant_read_write_data(self._handler)
        downstream.grant_invoke(self.handler)