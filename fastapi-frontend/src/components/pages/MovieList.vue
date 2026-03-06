<template>
  <layout-div>
    <!-- Верхняя панель с кнопками управления -->
    <div class="hero-section p-4 mb-4">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
        <h1 class="display-4 fw-bold text-white mb-0">
          <i class="bi bi-collection-play me-2"></i> Movie Catalog
        </h1>
        
        <div class="d-flex gap-2 flex-wrap">
          <!-- Кнопки управления email -->
          <div class="btn-group" role="group">
            <button 
              @click="toggleEmailSending" 
              class="btn" 
              :class="emailEnabled ? 'btn-success' : 'btn-secondary'"
              style="min-width: 120px;"
            >
              <i :class="emailEnabled ? 'bi bi-envelope-check' : 'bi bi-envelope-slash'"></i>
              {{ emailEnabled ? 'EMAIL ON' : 'EMAIL OFF' }}
            </button>
            
            <button @click="sendEmailNow" class="btn btn-info" style="min-width: 100px;">
              <i class="bi bi-send"></i> SEND
            </button>
          </div>
          
          <router-link to="/create" class="btn btn-light">
            <i class="bi bi-plus-circle me-2"></i> ADD MOVIE
          </router-link>
        </div>
      </div>
      
      <!-- Индикатор статуса -->
      <div class="mt-3 text-white-50 bg-dark bg-opacity-25 p-2 rounded">
        <div class="d-flex align-items-center gap-3 flex-wrap">
          <span>
            <i class="bi bi-envelope me-1"></i>
            Status: 
            <strong :class="emailEnabled ? 'text-success' : 'text-danger'">
              {{ emailEnabled ? '✅ Sending enabled' : '❌ Sending disabled' }}
            </strong>
          </span>
          <span>
            <i class="bi bi-clock me-1"></i>
            Next report: <strong>Every 5 minutes</strong>
          </span>
          <span>
            <i class="bi bi-envelope-paper me-1"></i>
            To: <strong>Yugrinkd@mail.ru</strong>
          </span>
        </div>
      </div>
    </div>

    <!-- Таблица с фильмами -->
    <div class="table-container">
      <div class="card border-0 rounded-0 shadow">
        <div class="card-header bg-primary text-white py-3 border-0">
          <h3 class="mb-0 ms-2">
            <i class="bi bi-list-stars me-2"></i> All Movies
          </h3>
        </div>
        
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-dark">
                <tr>
                  <th scope="col" class="px-4 py-3">#ID</th>
                  <th scope="col" class="py-3">Title</th>
                  <th scope="col" class="py-3">Year</th>
                  <th scope="col" class="py-3">Rating</th>
                  <th scope="col" class="py-3 text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="movies.length === 0">
                  <td colspan="5" class="text-center py-5">
                    <div class="text-muted py-4">
                      <i class="bi bi-emoji-frown display-1"></i>
                      <h3 class="mt-3">No movies found</h3>
                      <p class="lead">Click "ADD MOVIE" to create your first movie!</p>
                    </div>
                  </td>
                </tr>
                <tr v-for="movie in movies" :key="movie.id" class="align-middle">
                  <td class="px-4 fw-bold">{{ movie.id }}</td>
                  <td class="fw-500">{{ movie.title }}</td>
                  <td>{{ movie.year }}</td>
                  <td>
                    <span :class="['badge', getRatingClass(movie.rating)]" class="px-3 py-2">
                      <i class="bi bi-star-fill me-1"></i>
                      {{ movie.rating || 'N/A' }}
                    </span>
                  </td>
                  <td>
                    <div class="d-flex justify-content-center gap-2">
                      <router-link :to="`/show/${movie.id}`" class="btn btn-sm btn-outline-info">
                        <i class="bi bi-eye me-1"></i> View
                      </router-link>
                      <router-link :to="`/edit/${movie.id}`" class="btn btn-sm btn-outline-warning">
                        <i class="bi bi-pencil me-1"></i> Edit
                      </router-link>
                      <button @click="handleDelete(movie.id)" class="btn btn-sm btn-outline-danger">
                        <i class="bi bi-trash me-1"></i> Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Нижний колонтитул -->
        <div class="card-footer bg-light text-muted py-3 border-0">
          <div class="d-flex justify-content-between align-items-center px-2">
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
    return { 
      movies: [],
      emailEnabled: true
    };
  },
  created() {
    this.fetchMovies();
    this.checkEmailStatus();
  },
  methods: {
    fetchMovies() {
      axios.get('/movies/')
        .then(response => {
          this.movies = response.data;
        })
        .catch(error => {
          Swal.fire({ 
            icon: 'error', 
            title: 'Error', 
            text: 'Failed to load movies' 
          });
        });
    },
    async checkEmailStatus() {
      try {
        const response = await axios.get('/email/status');
        this.emailEnabled = response.data.email_sending_enabled;
      } catch (error) {
        console.error('Error checking email status:', error);
      }
    },
    async toggleEmailSending() {
      try {
        const endpoint = this.emailEnabled ? '/email/disable' : '/email/enable';
        const response = await axios.post(endpoint);
        this.emailEnabled = response.data.current_status === 'enabled';
        
        Swal.fire({
          icon: 'success',
          title: `Email ${this.emailEnabled ? 'ON' : 'OFF'}`,
          text: response.data.message,
          timer: 2000,
          showConfirmButton: false
        });
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to toggle email sending'
        });
      }
    },
    async sendEmailNow() {
      try {
        const response = await axios.post('/email/send-now');
        Swal.fire({
          icon: 'success',
          title: 'Sending...',
          text: 'Report is being sent to Yugrinkd@mail.ru',
          timer: 2000,
          showConfirmButton: false
        });
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to send email'
        });
      }
    },
    getRatingClass(rating) {
      if (!rating) return 'bg-secondary';
      if (rating >= 8) return 'bg-success';
      if (rating >= 5) return 'bg-warning text-dark';
      return 'bg-danger';
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
              Swal.fire({ 
                icon: 'success', 
                title: 'Deleted!', 
                timer: 1500, 
                showConfirmButton: false 
              });
              this.fetchMovies();
            })
            .catch(() => {
              Swal.fire({ 
                icon: 'error', 
                title: 'Error', 
                text: 'Failed to delete' 
              });
            });
        }
      });
    }
  }
};
</script>

<style scoped>
/* Герой секция */
.hero-section {
  width: 100vw;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
  position: relative;
  left: 50%;
  right: 50%;
  transform: translateX(-50%);
}

/* Таблица */
.table-container {
  width: 100%;
  padding: 0 1rem;
}

.card {
  border-radius: 0;
  width: 100%;
}

.table th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 1px;
}

.table td {
  vertical-align: middle;
  font-size: 1rem;
}

.btn-sm {
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
  transition: all 0.2s;
  border-width: 2px;
}

.btn-sm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.badge {
  font-size: 0.9rem;
  border-radius: 20px;
  min-width: 70px;
}

/* Убираем отступы */
:deep(body) {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Цвета рейтингов */
.bg-success {
  background: linear-gradient(135deg, #28a745, #20c997) !important;
}

.bg-warning {
  background: linear-gradient(135deg, #ffc107, #fd7e14) !important;
}

.bg-danger {
  background: linear-gradient(135deg, #dc3545, #c82333) !important;
}

.fw-500 {
  font-weight: 500;
}

/* Адаптивность */
@media (max-width: 768px) {
  .hero-section .d-flex {
    flex-direction: column;
    text-align: center;
  }
  
  .btn-group {
    width: 100%;
  }
  
  .btn-group .btn {
    flex: 1;
  }
}
</style>