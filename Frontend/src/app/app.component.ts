import { Component, OnInit, ViewEncapsulation } from "@angular/core";
import { SupService } from './sup.service';
@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent implements OnInit {
  title = "supplychain";
  formdata: any = {
    customername: null,
    generateuniqueid: null,
    appservicename: null,
    appserviceurl: null,
    datafactoryname: null,
    datafactorylocation: null,
    datafactorysources: null,
    bgprojectname: null,
    bqclientid: null,
    bqclientsecret: null,
    bqtoken: null,
    bgtableschema: null,
    bgtablevalues: null,
    oracleservername: null,
    oracleport: null,
    oraclesid: null,
    oracleuser: null,
    oraclepassword: null,
    oracleschema: null,
    oracletables: null,
    sapservername: null,
    sapusername: null,
    sappassword: null,
    sapschema: null,
    saptables: null,
    salesforceusername: null,
    salesforcepassword: null,
    salesforcetoken: null,
    salesforceschema: null,
    salesforcetables: null,
    storageaccountname: null,
    accesskey: null,
    storageconnectionstring: null,
    sqlservername: null,
    sqlserverusername: null,
    sqlserverpassword: null,
    sqlserverdatabasename: null,
    sqlserverconnectionstring: null,
    databricksname: null,
    accesstoken: null,
    databricksworkspaceurl: null,
    powerbiembedded: null,
    powerbiadmin: null,
    keyvaultname: null,
    keyvaultlocation: null,
    subscriptionid: null,
    subscriptiontenantid: null,
    subscriptionclientid: null,
    subscriptionclientsecret: null,
    subscriptopnresourcegroup: null,
    resourcegrouplocation: null,
    azurefunctionurl: null
  };
  constructor(private supservice: SupService) {}
  ngOnInit() {}
  getid() {
    this.supservice.getid().then(
      data => {
        console.log(data);
        this.formdata.generateuniqueid = data['output'];
      },
      error => {
        console.log(error);
      }
    );
  };
  submit() {
    console.log(this.formdata);
    this.supservice.submit(this.formdata).then(
      data => {
        console.log(data);
      },
      error => {
        console.log(error);
      }
    );
  }
}
