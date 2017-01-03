import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'

import { UrlFormComponent }  from './components/url_form.component';
import { AppComponent }  from './components/app.component';

@NgModule({
  imports:      [ BrowserModule, FormsModule],
  declarations: [ AppComponent, UrlFormComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
