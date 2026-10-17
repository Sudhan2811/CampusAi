CREATOR_INFO = {
    "name": "Sudhanshu Chaudhary",
    "education": "B.Tech in Electronics and Communication Engineering",
    "institute": "NIT Srinagar",
    "project": "CampusAI",
}


def get_creator_response():
    return (
        f"I was developed by {CREATOR_INFO['name']}, "
        f"a {CREATOR_INFO['education']} student at "
        f"{CREATOR_INFO['institute']}. "
        f"He built me as part of the {CREATOR_INFO['project']} project "
        f"using Generative AI technologies."
    )