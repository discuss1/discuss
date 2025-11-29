import { Component, OnInit, Input, Output, ChangeDetectorRef } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';

import { debounceTime, distinctUntilChanged } from "rxjs/operators";
import { MatDialog } from '@angular/material/dialog';
import { HttpEventType } from '@angular/common/http';
// import FroalaEditor from 'froala-editor';
import * as ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import { PostService } from '@reddit/core/services/post/post.service';
import { UserService } from '@reddit/core/services/user/user.service';
import { GroupService } from '@reddit/core/services/group/group.service';
import { User } from '@reddit/core/models/user.model';
import { Group } from '@reddit/core/models/group.model';


@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.scss']
})
export class CreatePostComponent implements OnInit {
  public Editor = ClassicEditor;
  public editorConfig = {
    toolbar: {
      items: [
        'heading',
        '|',
        'bold',
        'italic',
        'link',
        'bulletedList',
        'numberedList',
        '|',
        'outdent',
        'indent',
        '|',
        'blockQuote',
        'insertTable',
        'undo',
        'redo'
      ]
    },
    language: 'en',
    table: {
      contentToolbar: [
        'tableColumn',
        'tableRow',
        'mergeTableCells'
      ]
    }
  };

  postForm: FormGroup;
  content: any;
  user: User;
  isLoading: boolean = true;
  selected: null;
  formData: any;
  @Input() group: Group;
  edit: boolean = false;
  
  constructor(
    private postService: PostService,
    private userService: UserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.initializeForm();
    this.getAuthUser();
  }

  initializeForm() {
    this.postForm = new FormGroup({
      title: new FormControl('', {
        validators: [Validators.required]
      }),
      content: new FormControl(this.content, {
        validators: [Validators.required]
      })
    });

    this.postForm.valueChanges
      .pipe(debounceTime(3000), distinctUntilChanged())
      .subscribe(
        (response) => {
          console.log(response);
        });
    this.isLoading = false;
  }

  public onEditorReady(editor: any) {
    console.log('CKEditor is ready to use!', editor);
  }

  public onEditorChange(event: any, editor: any) {
    const data = editor.getData();
    this.postForm.patchValue({ content: data });
  }

  getAuthUser(): void {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if (initialized) {
          this.userService.user.subscribe(
            (user: User) => {
              this.user = user;
            });
        }
      });
  }

  submit() {
    const data = {
      title: this.postForm.controls.title.value,
      content: this.postForm.controls.content.value,
      author: this.user.id,
      group: this.group ? this.group.id : null
    }

    this.postService.createPost(data).subscribe(
      (response: any) => {
        this.router.navigate(['', response.uuid])
      },
      (err: any) => {
        console.log(err)
      });
  }

}
