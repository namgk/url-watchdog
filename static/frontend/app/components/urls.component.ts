import { Component } from '@angular/core';

@Component({
  selector: 'urls',
  template: `
    <ul class="list-group .col-md-6">
      <li class="list-group-item" *ngFor="let url of urls">
        <button type="button" class="btn btn-default delete">Delete</button>
        <span class='url'>{{url.url}} </span>
        <span class="status {{url.status}}">{{url.status}}</span>
      </li>
    </ul>
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
}
