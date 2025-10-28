# crew_ai_business_researcher.py
from crewai import Agent, Task, Crew, LLM
from langchain_community.tools import DuckDuckGoSearchResults

# === LLM configuration ===
gpt4o = LLM(model="gpt-4o-mini")  # or gpt-4-turbo

# === Agents ===
researcher = Agent(
    role="Market Research Analyst",
    goal="Gather up-to-date data about a given company or industry.",
    backstory="An expert in business intelligence and trend analysis.",
    tools=[DuckDuckGoSearchResults()],
    llm=gpt4o
)

analyst = Agent(
    role="Business Strategy Analyst",
    goal="Interpret the research data, identify opportunities, and assess threats.",
    backstory="A management consultant with experience in competitive strategy.",
    llm=gpt4o
)

writer = Agent(
    role="Technical Report Writer",
    goal="Create a concise, professional market summary report for executives.",
    backstory="A senior business writer skilled in summarizing complex insights.",
    llm=gpt4o
)

# === Tasks ===
task_research = Task(
    description="Search the web for data about {company_name}'s market, key competitors, and recent trends.",
    expected_output="A structured list of recent facts, stats, and competitor information.",
    agent=researcher
)

task_analysis = Task(
    description="Analyze the research data and extract key insights, opportunities, and risks.",
    expected_output="A bullet-point analysis of key insights and recommendations.",
    agent=analyst
)

task_report = Task(
    description="Write a polished executive summary report combining the research and analysis.",
    expected_output="A formatted business report with an executive summary, insights, and action items.",
    agent=writer
)

# === Crew ===
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task_research, task_analysis, task_report],
    process="sequential"  # or "parallel"
)

# === Run the Crew ===
if __name__ == "__main__":
    try: 
        company = input("Enter a company or industry: ").strip() 
        if not company: 
            print("Error: Please enter a valid company or industry name.") 
        else: print(f"\nStarting business research for: {company}...\n") 
            result = crew.kickoff(inputs={"company_name": company}) print("\n=== Business Research Report ===\n") print(result)
    except Exception as e: print(f"\nAn error occurred while running the research: {e}\n")
