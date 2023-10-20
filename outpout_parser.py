from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional


class PersonIntel(BaseModel):
    summary: str = Field(description="A short summary about the person")
    facts: List[str] = Field(description="interesting facts about the person")

    topics_of_interest: List[str] = Field(
        description="topic that might interest the person"
    )
    ice_breakers: List[str] = Field(
        description="creative Ice Breakers that can be used to start a conversation with the person"
    )

    def to_dict(self):
        return {
            "summary": self.summary,
            "facts": self.facts,
            "topic_of_interest": self.topic_of_interest,
            "ice_breakers": self.ice_breakers,
        }


person_intel_parser = PydanticOutputParser(pydantic_object=PersonIntel)
