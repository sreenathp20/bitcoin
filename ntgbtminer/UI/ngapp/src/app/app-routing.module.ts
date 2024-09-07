import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BinaryComponent } from './binary/binary.component';
const routes: Routes = [
  { path: 'binary', component: BinaryComponent },
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
