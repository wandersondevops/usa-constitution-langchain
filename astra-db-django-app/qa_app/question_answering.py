from django.conf import settings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from qa_app.prompt_templates import PROMPT

# auth settings
auth_provider = PlainTextAuthProvider("token", settings.ASTRA_DB_APPLICATION_TOKEN)
cluster = Cluster(cloud=settings.CLOUD_CONFIG, auth_provider=auth_provider)
astra_session = cluster.connect()
embeddings = OpenAIEmbeddings()

# slightly modified from Jupyter - no longer calling "from_documents"
# instead, we just create a Cassandra object, and pass the session + embeddings in.
astra_vectorstore = Cassandra(
    embedding=embeddings,
    session=astra_session,
    keyspace=settings.ASTRA_DB_KEYSPACE,
    table_name=settings.ASTRA_DB_TABLE_NAME
)

# gpt-3.5-turbo-16k == 16k token context window - easy to fit retrieved docs into Context for a query
llm = ChatOpenAI(temperature=0.0, model='gpt-4-32k-0314')


def run_retrieval_qa_pipeline(text, instructions='', k=100):
    partial_prompt = PROMPT.partial(instructions=instructions)

    retriever = astra_vectorstore.as_retriever(search_kwargs={'k': k})

    chain_type_kwargs = {"prompt": partial_prompt}
    qa_retriever = RetrievalQA.from_chain_type(
        llm=llm, 
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs=chain_type_kwargs
    )
    return qa_retriever.run(text)
    
