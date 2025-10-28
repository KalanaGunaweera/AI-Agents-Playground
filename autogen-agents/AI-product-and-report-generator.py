# pip install pyautogen duckduckgo-search
# export OPENAI_API_KEY="your_openai_api_key"

# product_research_autogen.py

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from duckduckgo_search import DDGS

# === CONFIG ===
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",  # or gpt-4-turbo
            "api_key": "YOUR_OPENAI_API_KEY"
        }
    ]
}

# === Define helper: web search ===
def web_search(query, num=5):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=num)
        return "\n".join([f"{r['title']}: {r['body']}" for r in results])

# === Agents ===
researcher = AssistantAgent(
    name="Researcher",
    system_message=(
        "You are a business research specialist. "
        "Your job is to gather up-to-date, factual insights about the given company or product."
    ),
    llm_config=llm_config,
)

analyst = AssistantAgent(
    name="Analyst",
    system_message=(
        "You are a business strategy analyst. "
        "You take raw research data and create an executive-level summary including "
        "strengths, weaknesses, opportunities, and risks."
    ),
    llm_config=llm_config,
)

writer = AssistantAgent(
    name="Writer",
    system_message=(
        "You are a report writer. Format and present the insights as a clean, professional report."
    ),
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # fully autonomous
)

# === Connect agents ===
researcher.register_function(
    function_map={"web_search": web_search}
)

# === Run the workflow ===
company = input("Enter a company or product name: ")

# Step 1: Research
research_prompt = f"Use the web_search() function to collect data about {company}'s market, competitors, and latest developments."
research_result = researcher.run(research_prompt)

# Step 2: Analysis
analysis_result = analyst.run(f"Analyze the following research data about {company}:\n\n{research_result}")

# Step 3: Report Writing
final_report = writer.run(
    f"Generate a professional market research report for {company} using the following analysis:\n\n{analysis_result}"
)

print("\n📊 === Final Report ===\n")
print(final_report)
