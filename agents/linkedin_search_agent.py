from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url, check_profile_url, reformat_linkedin_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                        the URL should be a link to a Linkedin profile page
                        always reformat the URL before returning it to me
                        Your answer should contain only a URL.
                        examples of final answers:
                            https://www.linkedin.com/in/eden-marco/
                            https://www.linkedin.com/in/ouriel-ohayon/                        """

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin url",
            func=get_profile_url,
            description="useful for finding a potential Linkedin profile pages",
        ),
        Tool(
            name="Check if URL contains a Linkedin Profile Page to be reformatted",
            func=check_profile_url,
            description="useful for checking if a URL is a valid Linkedin Profile Page",
        ),
        Tool(
            name="Reformat URL to be a valid Linkedin Profile Page",
            func=reformat_linkedin_url,
            description="useful for reformatting a URL to be a valid Linkedin Profile Page,",
        ),
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    prompt = PromptTemplate(input_variables=["name_of_person"], template=template)

    linkedin_url = agent.run(prompt.format_prompt(name_of_person=name)
    )

    return linkedin_url
