import { Component } from '@angular/core';
import { ApiService } from '../api.service';



@Component({
  selector: 'app-sha',
  templateUrl: './sha.component.html',
  styleUrls: ['./sha.component.css'],
})
export class ShaComponent {
  blocks: any = [];
  block: any;


  constructor(private apiService: ApiService) {}

  ngOnInit() {
    
    this.apiService.getBlocks().subscribe((data: any[]) => {
      this.blocks.push(data);

    });
  }

  byteSplit(str: string) {
    let len = str.length;
    let new_str = '';
    for(let i = 0; i<len; i+=4) {
      new_str += str.slice(i, i+4)+' ';
    }
    return new_str;

  }

  nextBlock(str: string) {
    this.apiService.getBlocksByHash(str).subscribe((data: any[]) => {
      this.blocks = [data].concat(this.blocks)

    });
  }

}
