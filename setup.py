from setuptools import find_packages, setup

setup(
    name="med-self-discover",
    version="0.1",
    license="MIT",
    description="""
        Implementation of the Code from the Paper SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures,
        (https://arxiv.org/pdf/2402.03620v1.pdf)
        """,
    packages=find_packages(exclude=[]),
    url="https://github.com/Dyke-F/medical-self-discover",
    keywords=[
        "Large Language Models",
        "Self Prompting",
        "Medical LLM Prompting",
        "LLMs for Medicine",
    ],
    author="Dyke Ferber",
    author_email="dykeferber@gmail.com",
    install_requires=[
        "openai=1.12.0",
        "tenacity=8.2.3",
        "fire=0.5.0",
        "termcolor=2.4.0",
    ],
)
