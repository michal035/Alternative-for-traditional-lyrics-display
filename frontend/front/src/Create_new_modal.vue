<template>
  <div class="Modal2">
    <div class="Modal2-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
.Modal2 {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.5);
}

.Modal2-content {
  background-color: transparent;
  padding: 20px;
  max-width: 500px;
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal2-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal2-image {
  width: 200px;
  height: 200px;
  object-fit: contain;
  margin-bottom: 20px;
}

.modal2-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

.modal2-buttons {
  display: flex;
  justify-content: space-between;
}

.modal2-button {
  padding: 10px 20px;
}
</style>