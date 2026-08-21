from pydantic import BaseModel, Field


# query api endpoint request format
class QueryRequest(BaseModel):
    query: str = Field(description="The user's question")


# query api endpoint response format
class QueryResponse(BaseModel):
    query: str
    answer: str
    policy_citations: str
    page_no: str
    document_name: str


class AIResponse(BaseModel):
    query: str = Field(description="The given query by user")
    answer: str = Field(description="The generated response")
    policy_citations: str = Field(
        description="Policy citation for the documents retrieved"
    )
    page_no: str = Field(description="Page number in the metadata")
    document_name: str = Field(description="Name of the document")
