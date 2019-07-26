import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { map } from "rxjs/operators";

import { Configration } from "./web-config";

@Injectable({
  providedIn: "root"
})
export class SupService {
  constructor(private http: HttpClient) {}

  getid() {
    return new Promise((resolve, reject) => {
      return this.http
        .get(Configration.weburl + "blob/all/")
        .pipe(
          map((response: any) => {
            return response;
          })
        )
        .subscribe(
          (success: any) => {
            console.log("subscribe");
            return resolve(success);
          },
          error => {
            console.log(error);
          }
        );
    });
  }

  submit(payload) {
    return new Promise((resolve, reject) => {
      return this.http
        .post(Configration.weburl + "blob/all/", payload)
        .pipe(
          map((response: any) => {
            return response;
          })
        )
        .subscribe(
          (success: any) => {
            console.log("subscribe");
            return resolve(success);
          },
          error => {
            console.log(error);
          }
        );
    });
  }
}
