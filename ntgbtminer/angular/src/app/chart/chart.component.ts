import { Component } from '@angular/core';
import * as Highcharts from 'highcharts';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css'],
})
export class ChartComponent {
  blocks: any = [];
  block: any = [];

  Highcharts: typeof Highcharts = Highcharts; // required
    chartConstructor: string = 'chart'; // optional string, defaults to 'chart'
    chartCallback: Highcharts.ChartCallbackFunction = function (chart) {  } // optional function, defaults to null
    updateFlag: boolean = false; // optional boolean
    oneToOneFlag: boolean = true; // optional boolean, defaults to false
    runOutsideAngular: boolean = false;

    chartOptions: Highcharts.Options = {};

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    
    this.apiService.getOnesCount().subscribe((data: any[]) => {
      data.forEach((element:any) => {
        this.blocks.push([element.block_1, element.nonce_1])
      });
      this.chartOptions = {
        xAxis: {
          title: {
              text: 'block_1'
          },
          labels: {
              format: '{value}'
          },
          startOnTick: true,
          endOnTick: true,
          showLastLabel: true
      },
      yAxis: {
          title: {
              text: 'nonce_1'
          },
          labels: {
              format: '{value}'
          }
      },
      tooltip: {
        pointFormat: 'block_1: {point.x} <br/> nonce_1: {point.y}'
    },
        series: [{
          data: this.blocks,
          type: 'scatter'
        }]
      };

    });

    
    
  }
  

}
