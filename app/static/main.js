var user = {
  username: '',
  password: ''
};

import Index from './components/Index.vue';
import Home from './components/Home.vue';
import Profile from './components/Profile.vue';
import Users from './components/Users.vue';
import Error from './components/Error.vue';

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
    username: user.username,
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
          app.notLoggedIn = false;
          router.push({ path: 'Home', params: { userId }})
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
          router.push({ path: 'Index', params: { userId }})
        })
        .catch((err) => {
          app.res = err;
        });
    },
    updateUser: function () {
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.put('https://info3103.cs.unb.ca:24842/signin', app.screenName, axiosConfig)
        .then((res) => {
          app.res = res.data;
          app.loggedIn = true;
          router.push({ path: 'Home', params: { userId }})
        })
        .catch((err) => {
          app.res = err;
        });
    },
    deleteUser: function () {
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.delete('https://info3103.cs.unb.ca:24842/users/' + user.username, axiosConfig)
        .then((res) => {
          app.res = res.data;
          app.loggedIn = false;
          router.push({ path: 'Index' })
        })
        .catch((err) => {
          app.res = err;
        });
    },
  }
})