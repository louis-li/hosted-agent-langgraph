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
    endpoint="https://2026agent-nc.services.ai.azure.com/api/projects/proj-default",
    credential=DefaultAzureCredential()
)

# Create the agent from a container image
agent = client.agents.create_version(
    agent_name="td-langgraph-appinsight-demo",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="superbotcr.azurecr.io/langgraph-appinsight-image:latest",
        environment_variables={
            "AZURE_OPENAI_ENDPOINT": "https://2026agent-nc.cognitiveservices.azure.com/",
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-5-mini",
            "OPENAI_API_VERSION": "2025-01-01-preview",
            "AZURE_AI_PROJECT_ENDPOINT": "https://2026agent-nc.services.ai.azure.com/api/projects/proj-default",
            "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=cc0032b3-0dee-4dca-bd40-9a89862730b8;IngestionEndpoint=https://northcentralus-0.in.applicationinsights.azure.com/;LiveEndpoint=https://northcentralus.livediagnostics.monitor.azure.com/;ApplicationId=f7ac9e81-daa2-488d-832a-c66fb2ce4ed7"
        }
    )
)