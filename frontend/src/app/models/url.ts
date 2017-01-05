export class Url {
  url: string;
  id: string;
  status: string = 'unknown';

  constructor(url:string){
    this.url = url
  }

  setUrl(url:string){
    this.url = url
  }
}