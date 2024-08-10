import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {ShaComponent} from './sha/sha.component';
import {ChartComponent} from './chart/chart.component';

const routes: Routes = [
  { path: 'sha', component: ShaComponent },
  { path: 'chart', component: ChartComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
