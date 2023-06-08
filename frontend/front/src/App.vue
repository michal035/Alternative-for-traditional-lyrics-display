<script>
    import Modal from './Modal.vue';

    export default {
        name: 'App',
        components: {Modal},
        data(){
            return{
                text: 'd',
                showModal:false
            }
        },
        created() {
            const path = window.location.pathname;
            const user = path.substring(1); 
            console.log('User:', user);
        },
        methods:{

         send(file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('http://127.0.0.1:8000/upload/', {
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
                var extension = (doc.value.split("."))[(doc.value.split(".")).length - 1]
                // if != docx or != doc raise some stuff
                var f_size = file.size
                // if size > x rasie some stuff
                this.send(file)
          }
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
            <button @click="showModal = false">Close</button>
        </Modal>

        <h1>{{text}}</h1>
  </div>

  
</template>