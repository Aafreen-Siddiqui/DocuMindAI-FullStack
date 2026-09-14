
from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000
    )

    job_id: str = Field(
        ...,
        min_length=1
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value