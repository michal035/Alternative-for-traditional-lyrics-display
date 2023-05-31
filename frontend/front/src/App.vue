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
            const user = path.substring(1); // Remove the leading "/" from the path
            console.log('User:', user);
        }
    }


</script>


<template>
    
    <div id="app">

        <div class="settings-button" @click="showModal = true">
        <i class="fas fa-cog"></i>
        </div>

        <Modal v-if="showModal">
            <!-- Add the content for your modal here -->
            <h1>Modal Content</h1>
            <p>This is the content of the modal.</p>
            <button @click="showModal = false">Close</button>
        </Modal>

        <h1>{{text}}</h1>
  </div>

  
</template>


