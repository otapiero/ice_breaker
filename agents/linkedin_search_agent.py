from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url, check_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL
                         the URL should be a link to a Linkedin profile page
                         the format of the URL should be only
                          https://www.linkedin.com/in/[unique identifier]/
                          example: https://www.linkedin.com/in/eden-marco/
                          """

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url,
            description="useful for finding linkedin profile pages",
        ),
        Tool(
            name="Check if URL is a valid Linkedin Profile Page",
            func=check_profile_url,
            description="useful for checking if a URL is a valid Linkedin Profile Page",
        ),
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt = PromptTemplate(input_variables=["name_of_person"], template=template)

    linkedin_url = agent.run(prompt.format_prompt(name_of_person=name)
    )

    return linkedin_url
