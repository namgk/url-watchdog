import { Component, OnInit } from '@angular/core';
import { Url } from '../models/url';
import { UrlService } from '../services/url.service';
import { Observable }       from 'rxjs/Observable';

import '../../../public/css/styles.css';
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
  urls : Url[]; 
  items: Observable<string[]>;
  mode = 'Observable';

  constructor (private urlService: UrlService) {}

  ngOnInit() { 
    this.urls = []
    this.getUrls(); 
  }

  delUrl(url: Url) : void {
    let me = this

    for (let i = 0; i < this.urls.length; i++){
      if (this.urls[i].id === url.id){
        // let encodedUrl = encodeURIComponent(url.url)
        this.urlService
        .delUrl(url.id)
        .subscribe(
          res  => me.urls.splice(i, 1),
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
        this.urls = urls
      },
      error =>  this.errorMessage = <any>error);
  }
}
