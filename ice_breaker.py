from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import dotenv

from agents.linkedin_search_agent import lookup
from third_party.linkedin import scrape_linkedin_profile, scrape_demo_linkedin_profile

dotenv.load_dotenv()


if __name__ == "__main__":
    summary_template = """
        given the Linkedin information {information} about a person, I want you to create:
        1. a short summary.
        2. two interesting facts about the person.
        
    """
    #         response in this format:  ["summary": "your summary", "facts": ["fact1", "fact2"]]

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_profile_url =lookup(name ="Ouriel Tapiero")
    print(linkedin_profile_url)
    # linkedin_data = scrape_demo_linkedin_profile(
    #     linkedin_profile_url
    # )
    linkedin_data = scrape_linkedin_profile(
    linkedin_profile_url
    )

    print(chain.run(information=linkedin_data))
