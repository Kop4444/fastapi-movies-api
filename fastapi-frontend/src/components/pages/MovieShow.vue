<template>
  <layout-div>
    <h2 class="text-center mt-4 mb-4">Movie Details</h2>
    <div class="card">
      <div class="card-header">
        <router-link to="/" class="btn btn-secondary btn-sm">Back to List</router-link>
      </div>
      <div class="card-body">
        <div v-if="movie">
          <div class="row mb-3">
            <div class="col-sm-3 fw-bold">ID:</div>
            <div class="col-sm-9">{{ movie.id }}</div>
          </div>
          <div class="row mb-3">
            <div class="col-sm-3 fw-bold">Title:</div>
            <div class="col-sm-9">{{ movie.title }}</div>
          </div>
          <div class="row mb-3">
            <div class="col-sm-3 fw-bold">Year:</div>
            <div class="col-sm-9">{{ movie.year }}</div>
          </div>
          <div class="row mb-3">
            <div class="col-sm-3 fw-bold">Rating:</div>
            <div class="col-sm-9">{{ movie.rating || 'N/A' }}</div>
          </div>
        </div>
        <div v-else class="text-center">
          Loading...
        </div>
      </div>
    </div>
  </layout-div>
</template>

<script>
import axios from 'axios';
import LayoutDiv from '../LayoutDiv.vue';
import Swal from 'sweetalert2';

export default {
  name: 'MovieShow',
  components: { LayoutDiv },
  data() {
    return {
      movie: null
    };
  },
  created() {
    const id = this.$route.params.id;
    axios.get(`/movies/${id}`)
      .then(response => {
        this.movie = response.data;
      })
      .catch(() => {
        Swal.fire({ 
          icon: 'error', 
          title: 'Error', 
          text: 'Failed to load movie' 
        });
        this.$router.push('/');
      });
  }
};
</script>