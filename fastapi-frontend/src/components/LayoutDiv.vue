<template>
  <div class="layout-fullwidth">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'LayoutDiv',
};
</script>

<style scoped>
.layout-fullwidth {
  width: 100%;
  max-width: 100%;
  padding: 0;
  margin: 0;
}
</style>