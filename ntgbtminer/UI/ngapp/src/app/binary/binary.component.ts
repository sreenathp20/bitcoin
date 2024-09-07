import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-binary',
  templateUrl: './binary.component.html',
  styleUrls: ['./binary.component.css'],
  providers: [ApiService]

})
export class BinaryComponent {
  constructor(private api: ApiService) { }
  loaded: any = false;
  ngOnInit() {
    this.loadData();
  }
  number_system: any = 2;
  data: any = [];
  words: any = {};
  classButtonFontSize: any = 'btnfsize';
  loadData() {
    this.api.getConfig()
      .subscribe((data):any =>  {
        //console.log(data)
        this.data = data;
        //this.data = this.data.reverse();
        for(let i = 0; i < this.data.length; i++) {
          this.words[i] = [];
          let d = this.data[i];
          let keys = Object.keys(d)
          for(let j = 0; j < keys.length; j ++) {
            let k = keys[j];
            if (k != 'wv' && k != 'initial_hash') {
              this.words[i].push(d[j]);
            }
          }
          if(i < (this.data.length-1)) {
            let keys1 = Object.keys(this.data[i]['wv'])
            for(let j = 1; j < keys1.length; j ++) {
              this.data[i]['wv'][j]['h_diff'] = parseInt(this.data[i]['wv'][j]['h'], 2) - parseInt(this.data[i]['wv'][j-1]['h'], 2);
              
            }
            for(let j = 1; j < keys1.length; j ++) {
              const zeroPad = (res2:any, places:any) => String(res2).padStart(places, '0')
              let hplusword = Number(parseInt(this.data[i]['wv'][j-1]['h'], 2) + parseInt(this.words[i][j], 2)).toString(2)
              hplusword = zeroPad(hplusword, 32);
              this.data[i]['wv'][j]['hplusword'] = hplusword.slice(hplusword.length-32, hplusword.length);
            }
            for(let j = 2; j < keys1.length; j ++) {
              const zeroPad = (res2:any, places:any) => String(res2).padStart(places, '0')
              let hwdiff = parseInt(this.data[i]['wv'][j]['hplusword'], 2) - parseInt(this.data[i]['wv'][j-1]['hplusword'], 2);
              this.data[i]['wv'][j]['hwdiff'] = hwdiff;
            }
          }
          
          
        }
        this.loaded = true;
      });
  }
  hexa() {
    this.classButtonFontSize = 'btnfsizeHexa';
    this.number_system = 16;
  }
  toBinary() {
    this.classButtonFontSize = 'btnfsize';
    this.number_system = 2;
  }
  dividerCommon(w:any, st: any) {
    w = w[w.length-1][st];
    let res = '';
    let sep = 8;
      let j = 0;
      for(let i = 0; i < w.length; i++) {
        if(j==sep) {
          res += ' | '+w[i];
          j = 0;
        }else {
          res += w[i]
        }
        j += 1        
      }  
      return res; 
  }
  divider(w:any) {
    let res = '';
    if(this.number_system == 2) {
      let sep = 8;
      let j = 0;
      for(let i = 0; i < w.length; i++) {
        if(j==sep) {
          res += ' | '+w[i];
          j = 0;
        }else {
          res += w[i]
        }
        j += 1        
      }      
    }else if(this.number_system == 16){
      let places = 8
      let res2 = parseInt(w, 2).toString(16).toUpperCase();
      const zeroPad = (res2:any, places:any) => String(res2).padStart(places, '0')
      res2 = zeroPad(res2, 8);

      let sep = 2;
      let j = 0;
      //let res = ''
      for(let i = 0; i < res2.length; i++) {
        if(j==sep) {
          res += ' | '+res2[i];
          j = 0;
        }else {
          res += res2[i]
        }
        j += 1        
      }      
    }
    return res;
  }
  
}
