import Vue from "vue";
import VueRouter from "vue-router";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

var user = {
  username: '',
  password: '',
  screenName: ''
};

import Index from './components/Index.vue';
import Home from './components/Home.vue';
import Profile from './components/Profile.vue';
import Users from './components/Users.vue';
import Error from './components/Error.vue';
import './styles.css'
import "./images/favicon.ico";

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
    getName: function () {
      let axiosConfig = {
          headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
          }
      };
      axios.get('https://info3103.cs.unb.ca:24842/users?user=' + user.username, axiosConfig)
          .then((res) => {
            for(var i = 0; i < res.data['users'].length; i ++) {
              if(res.data['users'][i]['username'] === user.username) {
                user.screenName = res.data['users'][i]['screen_name'];
              }
            }
          })
          .catch((err) => {
          });
  },
    signIn: function () {
      user.username = user.username.toLowerCase();
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
          this.screenName = '';
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
  created: async function() {
    await this.getUser();
    this.getName();
  }
})

router.beforeEach((to, from, next) => {
  if(to.path === '/home') {
    app.getName();
  }
  app.getUser();

  next();
})
