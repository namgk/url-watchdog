import { Component, OnInit } from '@angular/core';
import { Url } from '../models/url';
import { UrlService } from '../services/url.service';
import { Observable }       from 'rxjs/Observable';

import '../rxjs-operators';

@Component({
  selector: 'urls',
  template: `
  <div id='container'>
    <url-form  [urls]="urls"></url-form>
    <ul class="list-group .col-md-6">
      <li class="list-group-item" *ngFor="let url of urls">
        <button (click)="delUrl(url)" type="button" class="btn btn-default delete">Delete</button>
        <span class='url'>{{url.url}} </span>
        <span class="status {{url.status}}">{{url.status}}</span>
      </li>
    </ul>
   </div>
  `,
  providers: [UrlService]
})

export class AppComponent implements OnInit { 
  errorMessage: string;
  urls = [
    {
      url: 'http://hub.urbanopus.test', 
      status: 'ok'
    },
    {
      url: 'http://hub.urbanopus.test2', 
      status: 'failed'
    }
  ]; 
  items: Observable<string[]>;
  mode = 'Observable';

  constructor (private urlService: UrlService) {}

  ngOnInit() { 
    this.urls = []
    this.getUrls(); 
  }

  delUrl(url: Url) : void {
    let toBeDelete : number
    let me = this

    for (let i = 0; i < this.urls.length; i++){
      if (this.urls[i].url === url.url){
        toBeDelete = i

        let encodedUrl = encodeURIComponent(url.url)
        this.urlService
        .delUrl(encodedUrl)
        .subscribe(
          res  => me.urls.splice(toBeDelete, 1),
          error =>  this.errorMessage = <any>error);
        break
      }
    }
  }

  getUrls() {
    this.urlService
    .getUrls()
    .subscribe(
      urls => {
        this.urls = []
        for (let u of urls){
          this.urls.push({url: decodeURIComponent(u.url), status: u.status})
        }
      },
      error =>  this.errorMessage = <any>error);
  }
}
