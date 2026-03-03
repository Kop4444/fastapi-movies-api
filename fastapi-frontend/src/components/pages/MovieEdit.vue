<template>
  <layout-div>
    <h2 class="text-center mt-4 mb-4">Edit Movie</h2>
    <div class="card">
      <div class="card-header">
        <router-link to="/" class="btn btn-secondary btn-sm">Back to List</router-link>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleUpdate">
          <div class="mb-3">
            <label class="form-label">Title</label>
            <input v-model="movie.title" type="text" class="form-control">
          </div>
          <div class="mb-3">
            <label class="form-label">Year</label>
            <input v-model="movie.year" type="number" class="form-control">
          </div>
          <div class="mb-3">
            <label class="form-label">Rating</label>
            <input v-model="movie.rating" type="number" step="0.1" class="form-control">
          </div>
          <button type="submit" class="btn btn-warning" :disabled="isSaving">
            {{ isSaving ? 'Updating...' : 'Update Movie' }}
          </button>
        </form>
      </div>
    </div>
  </layout-div>
</template>

<script>
import axios from 'axios';
import LayoutDiv from '../LayoutDiv.vue';
import Swal from 'sweetalert2';

export default {
  name: 'MovieEdit',
  components: { LayoutDiv },
  data() {
    return {
      movie: { title: '', year: '', rating: '' },
      isSaving: false
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
  },
  methods: {
    handleUpdate() {
      this.isSaving = true;
      const id = this.$route.params.id;
      axios.put(`/movies/${id}`, this.movie)
        .then(() => {
          Swal.fire({ 
            icon: 'success', 
            title: 'Success', 
            text: 'Movie updated!', 
            timer: 1500, 
            showConfirmButton: false 
          });
          this.$router.push('/');
        })
        .catch(() => {
          Swal.fire({ 
            icon: 'error', 
            title: 'Error', 
            text: 'Failed to update movie' 
          });
          this.isSaving = false;
        });
    }
  }
};
</script>