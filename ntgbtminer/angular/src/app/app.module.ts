import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from  '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ShaComponent } from './sha/sha.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import {MatIconModule} from '@angular/material/icon';
import {MatDividerModule} from '@angular/material/divider';
import {MatButtonModule} from '@angular/material/button';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { ChartComponent } from './chart/chart.component';
import { HighchartsChartModule } from 'highcharts-angular';

@NgModule({
  declarations: [
    
    AppComponent,
    ShaComponent,
    ChartComponent
    
  ],
  imports: [
    HighchartsChartModule,
    MatSlideToggleModule,
    MatButtonModule, MatDividerModule, MatIconModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
