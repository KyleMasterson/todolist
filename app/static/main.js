var user = {
  username:'',
  password: ''
};

var app = new Vue({
  el: '#vueRoot',
  data: {
    user: user,
    res: '',
    loggedIn: false
  },
  methods:{
    signIn : function (){
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.post('https://info3103.cs.unb.ca:24842/signin', user, axiosConfig)
      .then((res) => {
        app.res=res.data;
        app.loggedIn=true;
      })
      .catch((err) => {
        app.res= err;
      });
    },
    signOut : function (){
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.delete('https://info3103.cs.unb.ca:24842/signin', axiosConfig)
      .then((res) => {
        app.res=res.data;
        app.loggedIn=false;
      })
      .catch((err) => {
        app.res= err;
      });
    },
  }
})
