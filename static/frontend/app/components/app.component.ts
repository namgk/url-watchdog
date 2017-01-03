import { Component } from '@angular/core';
import { Url } from '../models/url';

@Component({
  selector: 'urls',
  template: `
  <div id='container'>
    <url-form  [urls]="urls"></url-form>
    <ul class="list-group .col-md-6">
      <li class="list-group-item" *ngFor="let url of urls">
        <button (click)="delete(url)" type="button" class="btn btn-default delete">Delete</button>
        <span class='url'>{{url.url}} </span>
        <span class="status {{url.status}}">{{url.status}}</span>
      </li>
    </ul>
   </div>
  `,
})

export class AppComponent  { 
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

  delete(url: Url) : void {
    let toBeDelete : number

    for (let i = 0; i < this.urls.length; i++){
      if (this.urls[i].url === url.url){
        toBeDelete = i
        break
      }
    }

    this.urls.splice(toBeDelete, 1)
  }
}
