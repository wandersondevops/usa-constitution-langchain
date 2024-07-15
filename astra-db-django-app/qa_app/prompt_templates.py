from langchain.prompts import PromptTemplate
prompt_template = """

{context}

Question: {question}

Instructions: {instructions}"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question", "instructions"]
)