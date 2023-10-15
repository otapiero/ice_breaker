from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url, check_profile_url, reformat_linkedin_url
import dotenv

dotenv.load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """given the full name {name_of_person} I want you to get it me a link to their Twitter profile page.
                        and extract the username from the URL
                        you can manually extract the username from the URL by removing the https://twitter.com/ part
                        in your final answer, you should return only the username.
                        examples of final answers:
                            edenmarco
                            ourielohayon
                            elonmusk
                            IvankaTrump
                            """
    tools_for_agent = [
        Tool(
            name="Crawl Google for twitter url",
            func=get_profile_url,
            description="useful for finding a potential Twitter profile pages",
        )
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt = PromptTemplate(input_variables=["name_of_person"], template=template)

    twitter_username = agent.run(prompt.format_prompt(name_of_person=name))

    return twitter_username


print(lookup(name="Ivanka Trump"))
