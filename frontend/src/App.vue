<template>
  <va-navbar
      color="primary"
      shape
      class="mb-2"
  >
    <template #left>
      <router-link to="/" class="link">
        <va-navbar-item class="logo">
          Library
        </va-navbar-item>
      </router-link>
    </template>

    <template #right>
      <va-navbar-item><router-link v-if="token !== null" to="/books" class="link">Мои книги</router-link></va-navbar-item>
      <va-navbar-item><router-link v-if="token !== null"  to="/book/save" class="link">Сохранить книгу</router-link></va-navbar-item>
      <va-navbar-item v-if="token === null"><router-link to="/login" class="link">Войти</router-link></va-navbar-item>
      <va-navbar-item v-if="token === null"><router-link to="/register" class="link">Регистрация</router-link></va-navbar-item>
      <va-navbar-item v-if="token !== null" @click="onLogout" class="link">Выйти</va-navbar-item>
    </template>
    <div class="upper">
      Добро пожаловать!
    </div>
  </va-navbar>
  <router-view :token="token" @login="onLogin" @userSet="onUserSet">

  </router-view>
</template>

<script>

import {logout} from "@/api/auth";

export default {
  name: 'App',
  data(){
    return {
      token: localStorage.getItem('token'),
      userName: localStorage.getItem('userName')
    }
  },
  mounted() {

  },
  methods: {
    onLogin(token){
      this.token = token;
    },
    onUserSet(userdata){
      this.userName = userdata.username;
    },
    onLogout(){
      logout(this.token).then(() => {
        this.token = null;
        this.userName = null;
        this.$router.push('/')
      }).catch((err) => {
        this.$vaToast.init({ message: String(err), position: 'bottom-right' })
      })
      localStorage.removeItem('token')
      localStorage.removeItem('userName')
    }
  }
}
</script>

<style>
.upper{
  position: relative;
  z-index: 5;
}
.link{
  color: white;
  cursor: pointer;
}
.logo {
  font-weight: 600;
  font-size: 1.5rem;
}
</style>
