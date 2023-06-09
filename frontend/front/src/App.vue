<script>
    import Modal from './Modal.vue';

    export default {
        name: 'App',
        components: {Modal},
        data(){
            return{
                text: '',
                showModal:false
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
                    console.log(data);
                })
                .catch(error => {
                    console.error(error);
                });

        }
    }


</script>


<template>
    
    <div id="app">

        <div class="settings-button" @click="showModal = true">
        <i class="fas fa-cog"></i>
        </div>

        <Modal v-if="showModal">
            <input type="file" id="the_file">
            <button @click="validate"></button>
            <button @click="CloseModal">Close</button>
        </Modal>

        <h1>{{text}}</h1>
  </div>

  
</template>