import os
import requests
import dotenv

dotenv.load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str):
    """
    scrape information from LinkedIn profile
    :param linkedin_profile_url: the LinkedIn profile url
    :return: a dictionary of the scraped information
    """
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    headers = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=headers
    )
    print(response._content)
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in [None, "", []] and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


def scrape_demo_linkedin_profile(linkedin_profile_url: str):
    """
    scrape information from a demo LinkedIn profile
    :return: a dictionary of the scraped information
    """
    response = requests.get(
        "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
    )
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in [None, "", []] and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
