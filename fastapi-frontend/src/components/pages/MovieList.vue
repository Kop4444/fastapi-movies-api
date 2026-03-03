<template>
  <layout-div>
    <!-- Верхний баннер на всю ширину -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="display-4 fw-bold text-white">
          <i class="bi bi-collection-play me-3"></i> Movie Catalog
        </h1>
        <router-link to="/create" class="btn btn-light btn-lg">
          <i class="bi bi-plus-circle me-2"></i> Add New Movie
        </router-link>
      </div>
    </div>

    <!-- Таблица на всю ширину -->
    <div class="table-wrapper">
      <div class="table-card">
        <div class="table-header">
          <h3 class="mb-0">
            <i class="bi bi-list-stars me-2"></i> All Movies
          </h3>
        </div>
        
        <div class="table-responsive">
          <table class="custom-table">
            <thead>
              <tr>
                <th>#ID</th>
                <th>TITLE</th>
                <th>YEAR</th>
                <th>RATING</th>
                <th class="text-center">ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="movies.length === 0">
                <td colspan="5" class="text-center py-5">
                  <div class="empty-state">
                    <i class="bi bi-emoji-frown display-1"></i>
                    <h3>No movies found</h3>
                    <p>Click "Add New Movie" to create your first movie!</p>
                  </div>
                </td>
              </tr>
              <tr v-for="movie in movies" :key="movie.id">
                <td class="fw-bold">{{ movie.id }}</td>
                <td>{{ movie.title }}</td>
                <td>{{ movie.year }}</td>
                <td>
                  <span :class="['rating-badge', getRatingClass(movie.rating)]">
                    <i class="bi bi-star-fill me-1"></i>
                    {{ movie.rating || 'N/A' }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/show/${movie.id}`" class="btn-view">
                      <i class="bi bi-eye"></i> View
                    </router-link>
                    <router-link :to="`/edit/${movie.id}`" class="btn-edit">
                      <i class="bi bi-pencil"></i> Edit
                    </router-link>
                    <button @click="handleDelete(movie.id)" class="btn-delete">
                      <i class="bi bi-trash"></i> Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Нижняя информация -->
        <div class="table-footer">
          <span>
            <i class="bi bi-info-circle me-2"></i>
            Total movies: <strong>{{ movies.length }}</strong>
          </span>
          <span>
            <i class="bi bi-clock me-2"></i>
            Last updated: <strong>{{ new Date().toLocaleDateString() }}</strong>
          </span>
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
  name: 'MovieList',
  components: { LayoutDiv },
  data() {
    return { movies: [] };
  },
  created() {
    this.fetchMovies();
  },
  methods: {
    fetchMovies() {
      axios.get('/movies/')
        .then(response => {
          this.movies = response.data;
        })
        .catch(error => {
          Swal.fire({ icon: 'error', title: 'Error', text: 'Failed to load movies' });
        });
    },
    getRatingClass(rating) {
      if (!rating) return 'rating-na';
      if (rating >= 8) return 'rating-high';
      if (rating >= 5) return 'rating-medium';
      return 'rating-low';
    },
    handleDelete(id) {
      Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
          axios.delete(`/movies/${id}`)
            .then(() => {
              Swal.fire({ icon: 'success', title: 'Deleted!', timer: 1500, showConfirmButton: false });
              this.fetchMovies();
            })
            .catch(() => {
              Swal.fire({ icon: 'error', title: 'Error', text: 'Failed to delete' });
            });
        }
      });
    }
  }
};
</script>

<style scoped>
/* Герой секция на всю ширину */
.hero-section {
  width: 100vw;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 3rem 2rem;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
  position: relative;
  left: 50%;
  right: 50%;
  transform: translateX(-50%);
}

.hero-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Обертка таблицы на всю ширину */
.table-wrapper {
  width: 100%;
  padding: 2rem;
  margin: 0;
}

.table-card {
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  overflow: hidden;
}

.table-header {
  background: #0d6efd;
  color: white;
  padding: 1.5rem 2rem;
}

/* Таблица на всю ширину */
.custom-table {
  width: 100%;
  border-collapse: collapse;
}

.custom-table th {
  background: #212529;
  color: white;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 1px;
  padding: 1.2rem 1rem;
}

.custom-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.custom-table tbody tr:hover {
  background-color: #f8f9fa;
}

/* Рейтинги */
.rating-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: 600;
  min-width: 80px;
  text-align: center;
}

.rating-high {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.rating-medium {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
  color: #212529;
}

.rating-low {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
}

.rating-na {
  background: #6c757d;
  color: white;
}

/* Кнопки действий */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-view, .btn-edit, .btn-delete {
  padding: 0.4rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
  border: 2px solid transparent;
  cursor: pointer;
}

.btn-view {
  background: #0dcaf0;
  color: white;
}

.btn-view:hover {
  background: #0b9ec0;
  transform: translateY(-2px);
}

.btn-edit {
  background: #ffc107;
  color: #212529;
}

.btn-edit:hover {
  background: #e0a800;
  transform: translateY(-2px);
}

.btn-delete {
  background: #dc3545;
  color: white;
  border: none;
}

.btn-delete:hover {
  background: #c82333;
  transform: translateY(-2px);
}

/* Футер таблицы */
.table-footer {
  background: #f8f9fa;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #6c757d;
  border-top: 1px solid #dee2e6;
}

/* Пустое состояние */
.empty-state {
  padding: 3rem;
  color: #6c757d;
}

/* Адаптивность */
@media (max-width: 768px) {
  .hero-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .custom-table th,
  .custom-table td {
    font-size: 0.85rem;
    padding: 0.5rem;
  }
}
</style>