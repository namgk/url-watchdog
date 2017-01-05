import { Component, Input } from '@angular/core'
import { Url } from '../models/url'
import { UrlService } from '../services/url.service';

@Component({
  selector: 'url-form',
  template: `
    <div class="form-group url-form">
      <b>Add a url to monitor:</b>
      <input #url (keyup)="validate(url.value)" class="form-control" placeholder='add a url'>
      <div [style.display]="valid ? 'none' : 'block'">Invalid URL</div>
      <button (click)="add(url.value)" type="button" class="btn btn-primary" id="urlAdd">Add Url</button>
    </div>
  `,
})

export class UrlFormComponent  {
  @Input()
  urls: Url[]
  valid: boolean = false

  private static pattern = new RegExp('^(https?:\/\/)+.')

  constructor (private urlService: UrlService) {}

  validate(url: string){
    this.valid = UrlFormComponent.pattern.test(url)
    return this.valid
  }

  add(u: string) : void {
    if(!this.validate(u)){
      return
    }

    for (let i = 0; i < this.urls.length; i++){
      if (this.urls[i].url === u){
        return
      }
    }
    
    let me = this
    this.urlService
    .addUrl(new Url(u))
    .subscribe(
      url => {
        me.urls.push(url)
      },
      error =>  console.log(error)
     );
  }
}
