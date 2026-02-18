## Troubleshooting

### Images built on Apple Silicon or other ARM64 machines do not work on our service

We **recommend using `azd` cloud build**, which always builds images with the correct architecture.

If you choose to **build locally**, and your machine is **not `linux/amd64`** (for example, an Apple Silicon Mac), the image will **not be compatible with our service**, causing runtime failures.

**Fix for local builds**

Use this command to build the image locally:

```shell
docker build --platform=linux/amd64 -t langgraph-image .
```

This forces the image to be built for the required `amd64` architecture.

https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry&tabs=foundry-sdk


docker build --platform=linux/amd64 -t langgraph-image .

az acr login -n superbotcr
docker tag langgraph-image:latest superbotcr.azurecr.io/langgraph-image:latest
docker push superbotcr.azurecr.io/langgraph-image:latest

To deploy:

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
    agent_name="langgraph-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="superbotcr.azurecr.io/langgraph-image:latest",
        environment_variables={
            "AZURE_OPENAI_ENDPOINT": "https://2026agent-nc.cognitiveservices.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview",
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-4.1",
            "AZURE_AI_PROJECT_ENDPOINT": "https://2026agent-nc.services.ai.azure.com/api/projects/proj-default",
            "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=cc0032b3-0dee-4dca-bd40-9a89862730b8;IngestionEndpoint=https://northcentralus-0.in.applicationinsights.azure.com/;LiveEndpoint=https://northcentralus.livediagnostics.monitor.azure.com/;ApplicationId=f7ac9e81-daa2-488d-832a-c66fb2ce4ed7"
        }
    )
)