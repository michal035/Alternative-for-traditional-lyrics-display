<script>
    import Modal from './Modal.vue';

    export default {
        name: 'App',
        components: {Modal},

        data(){
            return{
                text: '',
                showModal:false,
                downloadLink: '',
            }
        },
        created() {
            const path = window.location.pathname;
            var token = path.substring(1); 
            console.log('Token:', token);
        },
        methods:{

         send(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            
            const path = window.location.pathname;
            var token = path.substring(1); 


            console.log('http://127.0.0.1:8000/upload/'+token)
            fetch('http://127.0.0.1:8000/upload/'+token+'/', {
              method: 'POST',
              body: formData,
            })
              .then(response => {
                console.log(response)
              });
          },

          validate(){
                
                var doc = document.querySelector('input[type="file"]')
                var file = doc.files[0]
                let extension = (doc.value.split("."))[(doc.value.split(".")).length - 1]
                
                
                if (extension == "doc" || extension== "docx"){
                   let f_size = file.size
                   f_size = (f_size/1000)/1000
                   if (f_size > 500){
                    console.log("file is too big!")
                   }
                   this.send(file)
                }
                else{console.log("Unaccepted file type")}
                
          },
          CloseModal(){
            this.showModal = false
            location.reload()
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
                        throw new Error('Resource not found');
                    } else if (response.status === 204) {
                        //Custom message will need to appear 
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



    var qrCodeElement = document.getElementById("qrcode");

    

</script>

<style>
  .modal-content {
    background: transparent;
    border: none;
    box-shadow: none;
    align-items: center;
    justify-items: center;
  }

  .modal-dialog {
    margin: 0;
    max-width: none;
  }

  .modal-body {
    padding: 0;
  }



</style>


<template>
    <div id="app">
        <div class="settings-button" @click="showModal = true">
            <i class="fas fa-cog"></i>
        </div>


        <Modal v-if="showModal">
            
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" style="background: transparent; width: 50%">
                <div class="modal-content" id="the" style="background: transparent;" >
                    
                    <div class="modal-body d-flex justify-content-center" style="width: 100%">
                        <br>
                        <input class="form-control outline-danger" placeholder="Type in the code " type="text" id="the_file">
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
                        <a :href="downloadLink" download="qrcode.png">Download QR Code</a>
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