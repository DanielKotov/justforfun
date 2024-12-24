<template>
  <div class="container">
    <va-card tag="div">
      <va-card-title>Sign In</va-card-title>
      <va-card-content>
        <va-form style="width: 250px;">
          <p class="error" v-if="error">{{ error }}</p>

          <!-- Show remaining attempts warning -->
          <p class="warning" v-if="remainingAttempts !== null">
            Warning: {{ remainingAttempts }} login attempts remaining
          </p>

          <!-- Changed from login to email -->
          <va-input
              v-model="email"
              label="Email"
              :rules="[(value) => (value && value.length > 0) || 'Введите почту']"
          />
          <va-input
              v-model="password"
              class="mt-3"
              label="Password"
              type="password"
              :rules="[(value) => (value && value.length > 0) || 'Введите пароль']"
          />
          <div class="container">
            <va-button
                type="submit"
                class="mt-3"
                @click="onSubmit"
                :disabled="isLocked"
            >
              {{ isLocked ? `Locked (${lockoutTimeRemaining})` : 'Войти' }}
            </va-button>

            <va-button
                v-if="isLoggedIn"
                class="mt-3 ml-3"
                @click="onLogout"
                color="danger"
            >
              Выйти
            </va-button>

            <router-link to="/auth/register" class="link-small">Register</router-link>
          </div>

        </va-form>
      </va-card-content>
    </va-card>
  </div>
</template>

<script>
import { loginGetToken } from "@/api/auth";

export default {
  name: "LoginView",
  data() {
    return {
      email: "",  // Changed from login to email
      password: "",
      error: "",
      remainingAttempts: null,
      lockoutUntil: null,
      isLoggedIn: false
    };
  },
  mounted() {
    // Проверяем, есть ли токен при загрузке компонента
    this.isLoggedIn = !!localStorage.getItem('token');
  },
  computed: {
    isLocked() {
      return this.lockoutUntil && new Date() < new Date(this.lockoutUntil);
    },
    lockoutTimeRemaining() {
      if (!this.lockoutUntil) return '';
      const minutes = Math.ceil((new Date(this.lockoutUntil) - new Date()) / (1000 * 60));
      return `${minutes} min`;
    }
  },
  methods: {
    async onSubmit() {
      if (this.isLocked) return;

      try {
        this.error = "";
        this.remainingAttempts = null;

        const token = await loginGetToken(this.email, this.password);
        localStorage.setItem('token', token);
        this.isLoggedIn = true;
        this.$emit('login', token);
        this.$router.push('/');

      } catch (error) {
        console.log(error);
        this.error = error.message;

        if (error.message.includes('Too many failed attempts')) {
          // Set lockout timer for 15 minutes
          this.lockoutUntil = new Date(Date.now() + 15 * 60 * 1000);
        } else if (error.message.includes('attempts remaining')) {
          // Extract remaining attempts from error message
          const match = error.message.match(/(\d+) attempts remaining/);
          if (match) {
            this.remainingAttempts = parseInt(match[1]);
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
  margin-bottom: 10px;
}
.warning {
  color: orange;
  margin-bottom: 10px;
}
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100%;
  padding: 20px;
}
.link-small {
  font-size: 12px;
  margin-top: 10px;
}
va-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.ml-3 {
  margin-left: 12px;
}
</style>
