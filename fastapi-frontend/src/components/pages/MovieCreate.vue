<template>
  <layout-div>
    <h2 class="text-center mt-4 mb-4">Add New Movie</h2>
    <div class="card">
      <div class="card-header">
        <router-link to="/" class="btn btn-secondary btn-sm">Back to List</router-link>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleSave">
          <div class="mb-3">
            <label class="form-label">Title *</label>
            <input v-model="movie.title" type="text" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Year *</label>
            <input v-model="movie.year" type="number" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Rating</label>
            <input v-model="movie.rating" type="number" step="0.1" class="form-control">
          </div>
          <button type="submit" class="btn btn-primary" :disabled="isSaving">
            {{ isSaving ? 'Saving...' : 'Save Movie' }}
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
  name: 'MovieCreate',
  components: { LayoutDiv },
  data() {
    return {
      movie: { title: '', year: '', rating: '' },
      isSaving: false
    };
  },
  methods: {
    handleSave() {
      this.isSaving = true;
      axios.post('/movies/', this.movie)
        .then(() => {
          Swal.fire({ 
            icon: 'success', 
            title: 'Success', 
            text: 'Movie created!', 
            timer: 1500, 
            showConfirmButton: false 
          });
          this.$router.push('/');
        })
        .catch(() => {
          Swal.fire({ 
            icon: 'error', 
            title: 'Error', 
            text: 'Failed to create movie' 
          });
          this.isSaving = false;
        });
    }
  }
};
</script>