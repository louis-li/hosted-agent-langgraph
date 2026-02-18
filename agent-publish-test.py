# filepath: Direct OpenAI compatible approach
from openai import OpenAI 
from azure.identity import DefaultAzureCredential, get_bearer_token_provider 

# edit base_url with your <foundry-resource-name>, <project-name>, and <app-name>
openai = OpenAI(
    api_key=get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default"),
    # base_url="https://<foundry-resource-name>.services.ai.azure.com/api/projects/<project-name>/applications/<app-name>/protocols/openai",
    base_url="https://2026agent-nc.services.ai.azure.com/api/projects/proj-default/applications/td-langgraph-appinsight-demo/protocols/openai/responses?api-version=2025-11-15-preview",
    default_query = {"api-version": "2025-11-15-preview"}
)

response = openai.responses.create( 
  input="What is the size of France in square miles, divided by 27?", 
) 
print(f"Response output: {response.output_text}")