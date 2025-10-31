#pip install langchain openai langchainhub langchain-community duckduckgo-search

#export OPENAI_API_KEY="your_openai_api_key"

# ai_market_research_agent.py

from langchain.agents import initialize_agent, AgentType, load_tools
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# === 1. LLM Configuration ===
llm = ChatOpenAI(
    model="gpt-4o-mini",  # or gpt-4-turbo
    temperature=0.3
)

# === 2. Tools ===
# Add web search and summarization capabilities
search_tool = DuckDuckGoSearchResults()
tools = [search_tool]

# === 3. Memory ===
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# === 4. Agent ===
agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)

# === 5. Run the Agent ===
def run_market_research(company: str):
    print(f"\n🔍 Running market research for: {company}\n")
    prompt = f"""
    You are an AI business analyst.
    Conduct a market research report on "{company}" including:
    - Brief company overview
    - Key competitors
    - Recent developments or trends
    - Opportunities and risks
    - Actionable recommendations
    Use the available tools (like web search) as needed.
    """
    response = agent.run(prompt)
    print("\n📊 === Market Research Summary ===\n")
    print(response)

if __name__ == "__main__":
    company_name = input("Enter a company or product name: ")
    run_market_research(company_name)
