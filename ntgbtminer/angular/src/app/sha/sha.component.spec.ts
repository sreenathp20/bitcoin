import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShaComponent } from './sha.component';

describe('ShaComponent', () => {
  let component: ShaComponent;
  let fixture: ComponentFixture<ShaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShaComponent]
    });
    fixture = TestBed.createComponent(ShaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
