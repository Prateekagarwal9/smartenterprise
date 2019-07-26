from django.http.response import JsonResponse
from rest_framework.views import APIView
from .deployer_file import Deployer
from azure.storage.blob import BlockBlobService
import json
from collections import defaultdict
from .logging_file import get_logger
import random
from supplychain.settings import BASE_DIR
import os
from .models import RandomId


# Create your views here.
class FirstTrail(APIView):
    logger = get_logger()

    def get(self, request):
        while True:
            random_no = "".join([str(random.randint(0, 9)) for i in range(0, 9)])
            random_obj = RandomId.objects.filter(random_id=random_no)
            if random_obj.exists():
                continue
            else:
                random_obj = RandomId()
                random_obj.random_id = random_no
                random_obj.save()
                return JsonResponse({"output": random_no})

    def post(self, request):
        try:
            appservicename = request.data["appservicename"]  # should display 'bar' # response to your request.
            appurl = request.data["appurl"]
            datafactoryname = request.data["datafactoryname"]
            accountname = request.data["accountname"]
            accesskey = request.data["accesskey"].replace(" ", "+")
            # sql credentials
            connectstring = request.data["connectstring"].replace(" ", "+")
            servername = request.data["servername"]
            sqlusername = request.data["sqlusername"]
            sqlpass = request.data["sqlpass"]
            sqlcon = request.data["sqlcon"]
            dbname = request.data["dbname"]
            databricksname = request.data["databricksname"]
            accesstoken = request.data["accesstoken"]
            workspaceurl = request.data["workspaceurl"]
            powerbiname = request.data["powerbiname"]
            powerbiadmin = request.data["powerbiadmin"]
            keyvaultname = request.data["keyvaultname"]
            subid = request.data["subid"]
            tenid = request.data["tenid"]
            clientid = request.data["clientid"]
            clientsecret = request.data["clientsecret"]
            resourcegroup = request.data["resourcegroup"]
            rglocation = request.data["rglocation"]
            dflocation = request.data["dflocation"]
            azurefunction = request.data["azurefunction"]
            keyvaultlocation = request.data["keyvaultlocation"]
            rglocation = request.data["rglocation"]
            sources = request.data["sources"]
            # bq project data
            bqproject = request.data["bqproject"]
            bqclient = request.data["bqclient"]
            bqsecret = request.data["bqsecret"]
            bqtoken = request.data["bqtoken"]
            bqschema = request.data["bqschema"]
            bqtables = request.data["bqtables"]
            # oracle data
            oracleport = request.data["oracleport"]
            oraclesid = request.data["oraclesid"]
            oracleuser = request.data["oracleuser"]
            oraclepassword = request.data["oraclepassword"]
            oracleschema = request.data["oracleschema"]
            oracletable = request.data["oracletable"]
            # sap data
            sapserver = request.data["sapserver"]
            sapusername = request.data["sapusername"]
            sappassword = request.data["sapschema"]
            saptable = request.data["saptable"]
            sapschema = request.data["sapschema"]
            # salesforce data
            salesforceuser = request.data["salesforceuser"]
            salesforcepass = request.data["salesforcepass"]
            salesforcetoken = request.data["salesforcetoken"]
            salesforceschema = request.data["salesforceschema"]
            salesforcetables = request.data["salesforcetables"]
            resource_group = resourcegroup
            subscription_id = subid
            azure_client_id = clientid
            azure_client_secret = clientsecret
            azure_tenant_id = tenid
            li_salesforce = list()
            li_sap = list()

            if len(salesforceuser) > 0:
                schema_list = salesforceschema.split(",")
                table_list = salesforcetables.split(",")
                li_salesforce = [{"objects_label": schema_list[i], "objects_name": table_list[i]} for i in
                                 range(0, len(schema_list))]
            elif len(sapserver) > 0:
                schema_list = sapschema.split(",")
                table_list = saptable.split(",")
                li_sap = [{"table_schema": schema_list[i], "table_name": table_list[i]} for i in
                          range(len(schema_list))]

            dic = dict()
            dic['$schema'] = 'https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#'
            dic['contentVersion'] = '1.0.0.0'
            dic['parameters'] = defaultdict(dict)
            dic['parameters']['DataFactoryName']['value'] = datafactoryname
            dic['parameters']['DataFactoryLocation']['value'] = dflocation
            dic['parameters']['StorageConnectionString']['value'] = connectstring
            dic['parameters']['SQLConnectionString']['value'] = sqlcon
            dic['parameters']['AzureFunctionURL']['value'] = azurefunction
            dic['parameters']['Sources']['value'] = sources
            if len(li_salesforce) != 0:
                dic['parameters']['SalesForceUsername']['value'] = salesforceuser
                dic['parameters']['SalesForcePassword']['value'] = salesforcepass
                dic['parameters']['SalesForceToken']['value'] = salesforcetoken
                dic['parameters']['SalesForceTables']['value'] = li_salesforce
            if len(li_sap) != 0:
                dic['parameters']['SAPServer']['value'] = sapserver
                dic['parameters']['SAPUsername']['value'] = sapusername
                dic['parameters']['SAPPassword']['value'] = sappassword
                dic['parameters']['SAPTables']['value'] = li_sap

            for key, value in dic['parameters'].items():
                if value['value'] == None:
                    del dic['parameters'][key]

            with open(os.path.join(BASE_DIR, "ADFParameters.json"), "w") as f:
                f.write(json.dumps(dic))

            # new file

            dic2 = dict()
            dic2['$schema'] = 'https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#'
            dic2['contentVersion'] = '1.0.0.0'
            dic2['parameters'] = defaultdict(dict)
            dic2['parameters']['SubscriptionID']['value'] = str(subid)
            dic2['parameters']['TenantID']['value'] = tenid
            dic2['parameters']['ClientID']['value'] = clientid
            dic2['parameters']['CientSecret']['value'] = clientsecret
            dic2['parameters']['DataFactoryName']['value'] = datafactoryname
            dic2['parameters']['StorageAccountName']['value'] = accountname
            dic2['parameters']['StorageAccessKey']['value'] = accesskey
            dic2['parameters']['StorageConnectionString']['value'] = connectstring
            dic2['parameters']['SQLServerName']['value'] = servername
            dic2['parameters']['SQLUsername']['value'] = sqlusername
            dic2['parameters']['SQLPassword']['value'] = sqlpass
            dic2['parameters']['SQLConnectionString']['value'] = sqlcon
            dic2['parameters']['SQLDatabaseName']['value'] = dbname
            dic2['parameters']['DatabricksName']['value'] = databricksname
            dic2['parameters']['DataBricksWorkspaceURL']['value'] = workspaceurl
            dic2['parameters']['DataBricksToken']['value'] = accesstoken
            dic2['parameters']['PowerBIEmbeddedName']['value'] = powerbiname
            dic2['parameters']['PowerBIEmbeddedAdmin']['value'] = powerbiadmin
            dic2['parameters']['AppServiceName']['value'] = appservicename
            dic2['parameters']['AppServiceURL']['value'] = appurl
            dic2['parameters']['AzureFunctionURL']['value'] = azurefunction
            dic2['parameters']['KeyVaultName']['value'] = keyvaultname
            dic2['parameters']['KeyVaultLocation']['value'] = keyvaultlocation
            dic2['parameters']['ResourceGroupName']['value'] = resourcegroup
            dic2['parameters']['ResourceGroupLocation']['value'] = rglocation

            with open(os.path.join(BASE_DIR, "KeyVaultParameters.json"), "w") as f:
                f.write(json.dumps(dic2))

            container_name = 'marketplacecodes'
            blob_name = 'ADFParameters.json'
            blob_client = BlockBlobService(connection_string=connectstring)
            resp = blob_client.create_blob_from_path(container_name=container_name, blob_name=blob_name,
                                                     file_path=os.path.join(BASE_DIR, "KeyVaultParameters.json"))
            blob_name = 'KeyVaultParameters.json'
            resp = blob_client.create_blob_from_path(container_name=container_name, blob_name=blob_name,
                                                     file_path=os.path.join(BASE_DIR, "KeyVaultParameters.json"))
            obj = Deployer(resource_group, subscription_id, azure_client_id, azure_client_secret, azure_tenant_id)
        except KeyError as k:
            self.logger.error(str(k))
            return JsonResponse({"output": "", "status": "error", "message": str(k)})
        except Exception as e:
            self.logger.error(str(e))
            return JsonResponse({"output": "", "status": "error", "message": str(e)})
        return JsonResponse({"output": "", "status": "OK", "message": "everthing is okey"})
