<template>
  <div class="modal">
    <div class="modal-content">
      <!-- Add your modal content here -->
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  // Add any necessary component options here
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999; /* Ensure the modal appears on top of other elements */
}


</style>
