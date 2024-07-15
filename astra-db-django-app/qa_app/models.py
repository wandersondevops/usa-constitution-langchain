from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class TextQaVectors(DjangoCassandraModel):
    __keyspace__ = 'text_qa_keyspace'

    row_id = columns.Text(primary_key=True)
    body_blob = columns.Text()


class Answers(DjangoCassandraModel):
    __keyspace__ = 'text_qa_keyspace'

    row_id = columns.UUID(primary_key=True)
    answer = columns.Text()
    question = columns.Text()
    instructions = columns.Text()
    created_at = columns.DateTime()
    updated_at = columns.DateTime()
