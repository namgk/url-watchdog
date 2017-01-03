import { Component, Input } from '@angular/core'
import { Url } from '../models/url'

@Component({
  selector: 'url-form',
  template: `
    <div class="form-group url-form">
      <b>Add a url to monitor:</b>
      <input [(ngModel)]="url" type="url" class="form-control" id="url" placeholder='add a url'>
      <div [style.display]="valid ? 'none' : 'block'">Invalid URL</div>
      <button (click)="add(url)" type="button" class="btn btn-primary" id="urlAdd">Add Url</button>
    </div>
  `,
})


export class UrlFormComponent  {
  @Input()
  urls: Url[]

  valid: boolean

  add(u: string) : void {
    var pattern = new RegExp('^(https?:\/\/)+.')
    if(!pattern.test(u)){
      this.valid=false
      return
    }
    this.valid = true

    let url =  new Url();
    url.setUrl(u)
    for (let i = 0; i < this.urls.length; i++){
      if (this.urls[i].url === u){
        return
      }
    }
    this.urls.push(url)
  }
}
