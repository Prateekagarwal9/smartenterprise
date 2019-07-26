from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.storage.blob import BlockBlobService
import json


class Deployer(object):
    def __init__(self, resource_group, subscription_id, azure_client_id, azure_client_secret, azure_tenant_id):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.credentials = ServicePrincipalCredentials(
            client_id=azure_client_id,
            secret=azure_client_secret,
            tenant=azure_tenant_id
        )
        print(azure_client_secret)
        self.client = ResourceManagementClient(self.credentials, self.subscription_id)

    def deploy(self, arm, parms, connectstring):
        self.client.resource_groups.create_or_update(
            self.resource_group,
            {
                'location': 'Central US'
            }
        )
        self.arm = arm
        self.parms = parms
        block_blob_service = BlockBlobService(connection_string=connectstring)
        print(block_blob_service)
        template = block_blob_service.get_blob_to_text(container_name='marketplacecodes', blob_name=self.arm,
                                                       encoding="utf-8-sig")
        template = json.loads(template.content)
        # template_path = "/home/mohit/Downloads/azured
        block_blob_service = BlockBlobService(connection_string=connectstring)
        parameters = block_blob_service.get_blob_to_text(container_name='marketplacecodes', blob_name=self.parms,
                                                         encoding="utf-8-sig")
        parameters = json.loads(parameters.content)
        parameters = parameters["parameters"]
        deployment_properties = {
            'mode': DeploymentMode.incremental,
            'template': template,
            'parameters': parameters
        }
        file1 = open("FinalParameters.json", "w")
        file1.write(json.dumps(deployment_properties))
        file1.close()
        print("hello")
        deployment_async_operation = self.client.deployments.create_or_update(
            self.resource_group,
            'azure-sample',
            deployment_properties
        )
        print("bye")
        deployment_async_operation.wait()
        return "success!"
