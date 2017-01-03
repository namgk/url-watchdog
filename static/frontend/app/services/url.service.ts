import { Injectable }     from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';

import { Url }           from '../models/url';
import { Observable }     from 'rxjs/Observable';

@Injectable()
export class UrlService {
  private urlResource = '/api/url';  // URL to web API
  private urlsResource = '/api/urls';  // URL to web API

  constructor (private http: Http) {}

  getUrls(): Observable<Url[]> {
    return this.http.get(this.urlsResource)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  addUrl (encodedUrl: string): Observable<Url> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });

    return this.http.post(this.urlResource, { u:encodedUrl }, options)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  delUrl (encodedUrl: string): Observable<Url> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });

    return this.http.delete(this.urlResource + '/' + encodedUrl, options)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  private extractData(res: Response) {
    return res.json() || {};
  }

  private handleError (error: Response | any) {
    // In a real world app, we might use a remote logging infrastructure
    let errMsg: string;
    if (error instanceof Response) {
      const body = error.json() || '';
      const err = body.error || JSON.stringify(body);
      errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
    } else {
      errMsg = error.message ? error.message : error.toString();
    }
    console.error(errMsg);
    return Observable.throw(errMsg);
  }
}
