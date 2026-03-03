<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">
          <i class="bi bi-film"></i> Movie Catalog
        </router-link>
        <div class="navbar-nav ms-auto">
          <router-link class="nav-link" to="/">
            <i class="bi bi-house-door"></i> Home
          </router-link>
          <router-link class="nav-link" to="/create">
            <i class="bi bi-plus-circle"></i> Add Movie
          </router-link>
        </div>
      </div>
    </nav>

    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}

#app {
  width: 100%;
  max-width: 100%;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  width: 100%;
  max-width: 100%;
  padding: 0;
}

.navbar {
  width: 100%;
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.container-fluid {
  width: 100%;
  max-width: 100%;
  padding: 0;
  margin: 0;
}
</style>