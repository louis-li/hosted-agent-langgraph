###
# Create capacity host - Azure Bash shell
# 
# TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)
# curl --request PUT --url 'https://management.azure.com/subscriptions/8480def5-8f7a-4285-99f7-295b61d7b22a/resourceGroups/2026agent-ne-rg/providers/Microsoft.CognitiveServices/accounts/2026agent-nc/capabilityHosts/accountcaphost?api-version=2025-10-01-preview' --header 'content-type: application/json' --header "authorization: Bearer $TOKEN" --data '{"properties": {"capabilityHostKind": "Agents", "enablePublicHostingEnvironment": true}}'
#
###

# pip install --pre azure-ai-projects==2.0.0b2
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition, ProtocolVersionRecord, AgentProtocol
from azure.identity import DefaultAzureCredential

# Initialize the client
client = AIProjectClient(
    endpoint="https://ai-foundry202604.services.ai.azure.com/api/projects/proj-default",
    credential=DefaultAzureCredential()
)

# Create the agent from a container image
agent = client.agents.create_version(
    agent_name="td-langgraph-appinsight-demo",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="superbotcr.azurecr.io/langgraph-foundry-v2:latest",
        environment_variables={
            "AZURE_OPENAI_ENDPOINT": "https://ai-foundry202604.openai.azure.com/openai/v1",
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-5.4-mini",
            "OPENAI_API_VERSION": "2025-03-01-preview",
            "AZURE_AI_PROJECT_ENDPOINT": "https://ai-foundry202604.services.ai.azure.com/api/projects/proj-default",
            "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=6acf3fff-45a5-409b-aff3-9cb77d9e5010;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=d016af11-c2d3-4fdf-9efb-7e7f681633f2"
        }
    )
)