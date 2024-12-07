from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from datetime import datetime
import json
import os
import re
import streamlit as st

load_dotenv()

class Agents:

    def __init__(self, comp, model):
        self.llm=LLM(
            model=f"gemini/{model}"
        )

        self.search_tool=SerperDevTool()

        self.industry_researcher = Agent(
            role="Industry Research Specialist",
            goal=f"""Thoroughly research and analyze industry trends, company details, 
                      and competitor analysis for {comp}""",
            backstory=f"""
            You are an experienced industry analyst with expertise in understanding business domains, 
            market dynamics, and competitor landscapes. You excel at gathering and synthesizing information 
            about the company, industry, and its competitors.
            """,
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

        self.use_case_analyst=Agent(
            role="AI/ML use case analyst",
            goal="Generate relevant AI/ML use cases based on the industry research",
            backstory="""
            You are an AI/ML solutions architect with deep knowledge of implementing AI/ML solutions to solve business problems.
            You excel at finding opportunities to implement AI/ML solutions.
            """,
            llm=self.llm,
            verbose=True
        )

        self.resource_collector=Agent(
            role="Resource Asset Collector",
            goal="Find and collect relevant resources and implementation resources for the use cases",
            backstory="""
            You are a data resource specialist skilled at finding relevant datasets and implementation resources from various platforms
            like Kaggle, HuggingFace, and GitHub.
            """,
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )

class Tasks:

    def __init__(self, agents, comp):
        self.comp = comp

        # Research Task
        self.research_task = Task(
            description=f"Research the company or industry {self.comp}, including competitor analysis.",
            expected_output="""
            The output MUST be in proper formatted JSON format in the structure below:
            - **industry**: Name of the industry (string).
            - **key_offerings**: List of key offerings provided by the company or industry (list of strings).
            - **strategic_focus_area**: List of strategic focus areas for the company or industry (list of strings).
            - **current_technology_landscape**: List of technologies or trends relevant to the company or industry (list of strings).
            - **competitor_analysis**: List of key competitors in the industry (list of objects).
              - Each competitor should include:
                - **name**: Name of the competitor (string).
                - **key_offerings**: List of key offerings by the competitor (list of strings).
                - **strengths**: Strengths of the competitor (string).
                - **weaknesses**: Weaknesses of the competitor (string).
            """,
            agent=agents.industry_researcher
        )


        # Use Case Task
        self.use_case_task = Task(
            description="Generate relevant AI/ML use cases.",
            expected_output="""
            The output MUST be in proper formatted JSON format in the structure below:
            - **trends**: List of trends in the industry.
              - Each trend should include:
                - **trend**: Name of the trend (string).
                - **use_cases**: List of use cases relevant to the trend.
                  - Each use case should include:
                    - **title**: Title of the use case (string).
                    - **description**: Detailed description of the use case (string).
                    - **benefits**: Benefits of implementing the use case (string).
                    - **implementation_complexity**: Complexity level of implementation (Low/Medium/High).
            """,
            agent=agents.use_case_analyst
        )

        # Resource Task
        self.resource_task = Task(
            description="Find relevant resources for the use cases.",
            expected_output="""
            The output MUST be in proper formatted JSON format in the structure below:
            - **datasets**: List of relevant datasets.
              - Each dataset should include:
                - **name**: Name of the dataset (string).
                - **platform**: Platform where the dataset is hosted (string).
                - **url**: URL of the dataset (string).
                - **description**: Brief description of the dataset (string).
            - **implementation_resources**: List of implementation resources.
              - Each resource should include:
                - **title**: Title of the resource (string).
                - **type**: Type of resource (e.g., tutorial, guide, paper) (string).
                - **url**: URL of the resource (string).
                - **relevance**: Relevance of the resource to the use case (string).
            """,
            agent=agents.resource_collector
        )

class MainCrew:

    def __init__(self, comp, model):

        self.comp=comp

        self.agents=Agents(comp, model)

        self.tasks=Tasks(self.agents, comp)

        self.crew=Crew(
            agents=[
                self.agents.industry_researcher,
                self.agents.use_case_analyst,
                self.agents.resource_collector
            ],

            tasks=[
                self.tasks.research_task,
                self.tasks.use_case_task,
                self.tasks.resource_task
            ],

            verbose=True,
            process=Process.sequential
        )

    def run(self):
        results=self.crew.kickoff(inputs={"comp": self.comp})

        return results

def clean_json(json_string):
    cleaned_string = re.sub(r'^\s*//.*$', '', json_string, flags=re.MULTILINE)
    return json.loads(cleaned_string)

def format_as_markdown(data, task_type):
    data=clean_json(data)
    if task_type == 0:
        markdown = f"### Industry Research\n"
        markdown += f"- **Industry**: {data['industry']}\n"
        markdown += f"- **Key Offerings**:\n" + "\n".join([f"  - {offering}" for offering in data['key_offerings']])
        markdown += f"\n\n- **Strategic Focus Areas**:\n" + "\n".join([f"  - {focus}" for focus in data['strategic_focus_area']])
        markdown += f"\n\n- **Current Technology Landscape**:\n" + "\n".join([f"  - {tech}" for tech in data['current_technology_landscape']])
        if "competitor_analysis" in data:
            markdown += "\n\n### Competitor Analysis\n"
            for competitor in data["competitor_analysis"]:
                markdown += f"- **Name**: {competitor['name']}\n"
                markdown += f"  - Key Offerings: {', '.join(competitor['key_offerings'])}\n"
                markdown += f"  - Strengths: {competitor['strengths']}\n"
                markdown += f"  - Weaknesses: {competitor['weaknesses']}\n"
    elif task_type == 1:
        markdown = f"### AI/ML Use Cases\n"
        for trend in data['trends']:
            markdown += f"- **Trend**: {trend['trend']}\n"
            for use_case in trend['use_cases']:
                markdown += f"  - **Title**: {use_case['title']}\n"
                markdown += f"    - Description: {use_case['description']}\n"
                markdown += f"    - Benefits: {use_case['benefits']}\n"
                markdown += f"    - Implementation Complexity: {use_case['implementation_complexity']}\n"
    elif task_type == 2:
        markdown = f"### Resources\n"
        markdown += f"#### Datasets\n"
        for dataset in data['datasets']:
            markdown += f"- **Name**: {dataset['name']}\n"
            markdown += f"  - Platform: {dataset['platform']}\n"
            markdown += f"  - URL: {dataset['url']}\n"
            markdown += f"  - Description: {dataset['description']}\n"
        markdown += f"\n#### Implementation Resources\n"
        for resource in data['implementation_resources']:
            markdown += f"- **Title**: {resource['title']}\n"
            markdown += f"  - Type: {resource['type']}\n"
            markdown += f"  - URL: {resource['url']}\n"
            markdown += f"  - Relevance: {resource['relevance']}\n"
    else:
        return "Give proper task type"
    return markdown

def save_resources_to_markdown(data, company):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"resources/{company}/{company}_{timestamp}_resources.md"
    
    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        formatted_markdown = format_as_markdown(data, 2)
        
        with open(file_name, "w") as f:
            f.write(formatted_markdown)
        
        st.success(f"Resources have been saved to {file_name}!")
    except Exception as e:
        st.error(f"Failed to save resources: {str(e)}")


def main():
    st.title("Industry Research")

    company_name = st.text_input("Enter the company name:")

    if company_name:
        with st.spinner("Researching the Company..."):
            crew = MainCrew(comp=company_name, model="gemini-1.5-flash")
            result = crew.run()

        st.success("Research Completed!")

        tab1, tab2, tab3 = st.tabs(["Researcher Output", "Use Cases", "Resources"])

        with tab1:
            researcher_output = result.tasks_output[0].raw.split("```")[1][5:]
            st.markdown(format_as_markdown(researcher_output, 0))

        with tab2:
            use_cases_output = result.tasks_output[1].raw.split("```")[1][5:]
            st.markdown(format_as_markdown(use_cases_output, 1))

        with tab3:
            resources_output = result.tasks_output[2].raw.split("```")[1][5:]
            st.markdown(format_as_markdown(resources_output, 2))

            save_resources_to_markdown(resources_output, company_name)

if __name__=="__main__":
    main()