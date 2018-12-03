import Vue from "vue";
import VueRouter from "vue-router";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

var user = {
  username: '',
  password: ''
};

import Index from './components/Index.vue';
import Home from './components/Home.vue';
import Profile from './components/Profile.vue';
import Users from './components/Users.vue';
import Error from './components/Error.vue';
import './styles.css'

Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    { path: '/', component: Index },
    { path: '/users', component: Users },
    { path: '/home', component: Home },
    { path: '/profile', component: Profile },
    { path: '*', component: Error }
  ]
})

var app = new Vue({
  el: '#vueRoot',
  data: {
    user: user,
    res: '',
    notLoggedIn: true
  },
  router: router,
  methods: {
    signIn: function () {
      
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.post('https://info3103.cs.unb.ca:24842/signin', user, axiosConfig)
        .then((res) => {
          app.res = res.data;
          router.push('/home');
          app.notLoggedIn = false;
          user.password = '';
        })
        .catch((err) => {
          app.res = err;
          alert("Please ensure you used a valid UNB FCS login");
        });
    },
    signOut: function () {
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.delete('https://info3103.cs.unb.ca:24842/signin', axiosConfig)
        .then((res) => {
          app.res = res.data;
          app.notLoggedIn = true;
          router.push('/');
        })
        .catch((err) => {
          app.res = err;
        });
    },
    getUser: function() {
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.get('https://info3103.cs.unb.ca:24842/signin', axiosConfig)
        .then((res) => {
          app.notLoggedIn = false;
          user.username = res.data['Username'];
          router.push('/home');
        })
        .catch((err) => {
          app.notLoggedIn = true;
          router.push('/');
        })
      }
  },
  created: function() {
    this.getUser();
  }
})