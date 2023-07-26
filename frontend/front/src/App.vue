<script>
    import Modal from './Modal.vue'


    export default {
        name: 'App',
        components: {Modal},

        data(){
            return{
                text: '',
                showModal:false,
                showModal_main: false,
                showModal_final: false,
                showmodal_first_page: false,
                showmodal_join_via_code: false,
                showmodal_create_code: false,
                showModal_set_code: false,
                showPasswdDiv: false,
                imgUrl: '',
                token: '',
                doc_url: ''
            }
        },

        created() {
            const path = window.location.pathname
            var token = path.substring(1)
            console.log('Token:', token)
        },

        methods:{

         send(file,the_code_r) {
            
            const encoder = new TextEncoder()
            const data = encoder.encode(the_code_r)

            crypto.subtle.digest('SHA-256', data)
                .then(hashBuffer => {
                var hashArray = Array.from(new Uint8Array(hashBuffer))
                var hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('')
                
                //console.log('SHA-256 Hash:', hashHex)

                const formData = new FormData()
                formData.append('file', file)
                formData.append('code', hashHex)


                const path = window.location.pathname
                var token = path.substring(1)


                console.log('http://127.0.0.1:8000/upload/'+token)
                fetch('http://127.0.0.1:8000/upload/'+token+'/', {
                method: 'POST',
                body: formData,
                })
                .then(response => {
                    console.log(response)
                })

                })
            
          },
          send_just_code(code_){
            const data = {code: code_}
            
            const path = window.location.pathname
            var token = path.substring(1)


            console.log('http://127.0.0.1:8000/upload/'+token)
            fetch('http://127.0.0.1:8000/upload/'+token+'/', {
              method: 'POST',
              body: JSON.stringify(data),
            })
              .then(response => {
                console.log(response)
              })
          },

          validate(){
                
                var doc = document.querySelector('input[type="file"]')
                var the_code_r = document.getElementById("the_code_r").value
                var file = doc.files[0]
                let extension = (doc.value.split("."))[(doc.value.split(".")).length - 1]
                
                console.log(the_code_r)
                if (extension == "doc" || extension== "docx"){
                   let f_size = file.size
                   f_size = (f_size/1000)/1000
                   if (f_size > 500){
                    console.log("file is too big!")
                   }
                   this.send(file,the_code_r)
                }
                else{
                    if(the_code_r != ""){
                        console.log(the_code_r)
                        this.send_just_code(the_code_r)
                    }
                    console.log("Unaccepted file type")}
                
          },

          RedirectToPage_from_join_modal(){
            this.doc_url = '/'+ document.getElementById("join_token").value
            window.location.href = this.doc_url
          },

          CloseModal(){
            this.showModal = false
            this.showPasswdDiv = false
            location.reload()
          },

          CloseModal_main(){
            this.showModal_main = false
            // I guess the doc not found should be called or if it got reated it should be redirected to the right page
            location.reload()
          },
          CloseModalv3(){
            this.showModal = false
            location.reload()
          },

          GetQR(token_){
            var data = {token: token_}

            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }

                    fetch("http://127.0.0.1:8000/" + token_ + "/qr")
                        .then((response) => response.blob()) 
                        .then((blob) => {
                            var imgUrl = URL.createObjectURL(blob); 

                            //var modal_div = document.getElementById("create_new");
                            
                            this.token = data.token
                            this.imgUrl = imgUrl
                            
                            this.showmodal_create_code = false
                            this.showModal_final = true
                            
                        })
                        .catch((err) => console.log(err));
        
          },

          NewDocument(){
            console.log("new doc")
            this.showModal_main = true
          },

          ShowInfo(){
            //var code = document.getElementById("the_code").value
            this.showModal_main = false
            var code ="tempCode"
            //document.getElementById("create_new").innerHTML = ""

             if (!code) {
                console.error('No input provided')
                return
            }

                const encoder = new TextEncoder()
                const data = encoder.encode(code)

                crypto.subtle.digest('SHA-256', data)
                    .then(hashBuffer => {
                    var hashArray = Array.from(new Uint8Array(hashBuffer))
                    var hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('')
                    
                    console.log('SHA-256 Hash:', hashHex)


                    var data = {code: hashHex}

                    const requestOptions = {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(data)
                    }

                    fetch('http://127.0.0.1:8000/create-new', requestOptions)
                   .then((response) => {
                      return response.json()
                    }).then((data)=>{

                    
                        console.log(data.token)
                        var modal_div = document.getElementById("create_new")

                        this.GetQR(data.token)
                        
                        })
                    })
                    .catch(error => {
                    console.error('Error', error);
                    });  
            },
            SetPasswd(){
               let p_value = document.getElementById("the_passwd").value

                const encoder = new TextEncoder()
                const data = encoder.encode(p_value)
                //call an API
               crypto.subtle.digest('SHA-256', data)
                    .then(hashBuffer => {
                    var hashArray = Array.from(new Uint8Array(hashBuffer))
                    var hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('')
                    

                    var data = {code: hashHex}

                    const requestOptions = {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(data)
                    }
                    
                    fetch("http://127.0.0.1:8000/"+this.token+"/set", requestOptions)
                   .then((response) => {
                    this.showmodal_create_code = false
                      return response
                    })
                    })
                    .catch(error => {
                    console.error('Error', error);
                    }); 
            },
            Create_new(){
                this.showModal_main = false;
                this.showmodal_create_code = true;
            },
            Join_via_code(){
                this.showModal_main = false;
                this.showmodal_join_via_code = true;
            },
            notFound(){
                var the_doc = document.getElementById("main")
                the_doc.innerHTML = `<br> <h3>No document associated with this token</h3>`
            },

            GetQR_settings(token_){
            var data = {token: token_}

            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }

                    fetch("http://127.0.0.1:8000/" + token_ + "/qr")
                        .then((response) => response.blob()) 
                        .then((blob) => {
                            var imgUrl = URL.createObjectURL(blob); 

                            
                            this.token = data.token
                            this.imgUrl = imgUrl
                            
                        })
                        .catch((err) => console.log(err));
                
          },

            ShowSettings(){
                
                this.showModal = true
                const path = window.location.pathname
                var token = path.substring(1)


                const requestOptions = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                }

                fetch("http://127.0.0.1:8000/" + token + "/check")
                    .then(function(serverPromise){  
                    serverPromise.json()
                        .then(function(j) { 
                        if(j[0]["passwd"] == true){this.showPasswdDiv = true}
                        })
                        .catch(function(e){
                        console.log(e);
                        });
                    }) 
                    .catch((err) => console.log(err));
                

                this.GetQR_settings(token)
            },
            
            RedirectToPage(){

            this.doc_url = '/'+this.token
            window.location.href = '/'+ this.token
            this.GetQR_settings(this.token)

          },
          CloseModal_create_code(){
            this.showmodal_create_code = false;
          },
          IsTheCodeSet(){
            
          }
            
        },

        mounted() {

            const path = window.location.pathname;
            var token = path.substring(1); 


            fetch('http://127.0.0.1:8000/' + token)
                .then(response => {
                    
                    if (response.status == 200) {
                        return response.json();
                    } else if (response.status === 404) {
                        this.NewDocument()
                        throw new Error('Resource not found');
                    } else if (response.status === 204) {
                        this.notFound()
                        throw new Error('There is no such .docx');
                    } else {
                        throw new Error('Something went wrong');
                    }
                })

                .then(data => {
                    var tab = '<br>'
                    console.log(data);

                    console.log(data[2]["paragraph"])

                    for(let i =0;data.length > i;i++){

                        let row = data[i]["paragraph"]
                        if(row == ""){tab += "<br>"}
                        else{tab += "<p style='text-align: center'>"+row+"</p>"}


                    }

                    console.log(tab)
                    var the_doc = document.getElementById("main")
                    the_doc.innerHTML = tab
                })
                .catch(error => {
                    console.error(error);
                });

        }
    }



</script>



<style>


  .modal-content{
    background: transparent;
    border: none;
    box-shadow: none;
    align-items: center;
    justify-items: center;
  }

  .modal-dialog  {
    margin: 0;
    max-width: none;
  }

  .modal-body{
    padding: 0;
  }

</style>


<template>
    <div id="app">
        <div class="settings-button" @click="ShowSettings">
            <i class="fas fa-cog"></i>
        </div>

        <!--First modal the user would see -->
        <Modal v-if="showModal_main">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" id="main_page" style="background: transparent; width: 50%">
                <div class="modal-content" style="background: transparent;" id="the_content_part" >
                    

                    <div class=" d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%; margin: 20px;" @click="ShowInfo">Create new</button>
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%; margin: 20px;" @click="Join_via_code">Join via code</button>
                    </div>
                </div>
                    
            </div>     
        </Modal>


        <Modal v-if="showModal_final">
            
                
                <div class="modal-body d-flex flex-column align-items-center background: transparent; width: 50%" style="width: 100%">
                            <br>
                            
                            <p style="text-align: center; color: white;">Here is the code: <h3>{{ this.token }}</h3></p>
                           
                            <br>
                            <img :src=this.imgUrl onclick="downloadFile('${imgUrl}')">
                            <br>
                            <div style="text-align: center;">
                                <a :href=this.imgUrl download style="text-decoration: none; margin:20px;">
                                    <i class="fas fa-download" style="font-size: 40px; color: white; "></i> 
                                </a>

                                <a href="#" :onclick=this.Create_new style="text-decoration: none; margin:20px;">
                                    <i class="fas fa-lock" style="font-size: 40px; color: white; "></i> 
                                </a>


                                  <a :href=this.doc_url @click="RedirectToPage" style="text-decoration: none; margin:20px;">
                                    <i class="fas fa-window-close" style="font-size: 40px; color: white; "></i>
                                </a>

                            </div>

                </div>
                       
        </Modal>


        <Modal v-if="showModal">
            
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" style="background: transparent; width: 50%">
                <div class="modal-content" id="the" style="background: transparent;" >
                    
                    <div v-if="showPasswdDiv" class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" placeholder="Type in the code " type="text" id="the_code_r">
                    </div>
                    
                    <br>

                    <div class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" type="file"  id="the_file">
                    </div>
                    <div class="modal-footer d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="validate">Save</button>
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="CloseModal">Close</button>
                    </div>
                    <br>
                    <br>
                    <div>
                    <div id="qrcode"></div>
                        <img :src=this.imgUrl onclick="downloadFile('${imgUrl}')">
                    </div>
                    
                </div>
                    
            </div>



        </Modal>

 
        <!-- Create the code  -->
        <Modal v-if="showmodal_create_code">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable"  style="background: transparent; width: 50%">
                <div class="modal-content" style="background: transparent;" >

                    <div class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" placeholder="Type in the code - this will alow you to make changes, treat this like a password" type="text" id="the_passwd">
                    </div>
                                   
                    <div class="modal-footer d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="SetPasswd">Create</button>
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="CloseModal_create_code">Close</button>
                    </div>                
                </div>
            </div>     
        </Modal>


        <!-- Join via code modal -->
        <Modal v-if="showmodal_join_via_code">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" style="background: transparent; width: 50%">
                <div class="modal-content" style="background: transparent;"  >
                    
                    <div class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" placeholder="Type in the token" type="text" id="join_token">
                    </div>
                                
                    <div class="modal-footer d-flex justify-content-center mt-4 col-md-6" style="background: transparent; width:100%">
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="RedirectToPage_from_join_modal">Join</button>
                        <button class="btn btn-dark btn-lg px-4 " style="width: 45%;" @click="CloseModal">Close</button>
                    </div>                
                      
                </div>
            </div>     
        </Modal> 


        <h1>{{text}}</h1>
        <div>
            <div class="a" id="main"></div>
        </div>
    </div>
</template>