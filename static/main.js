var user = {
  username:'',
  password: ''
};

var app = new Vue({
  el: '#vueRoot',
  data: {
    user: user,
    res: ''
  },
  methods:{
    signIn : function (){
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.post('http://info3103.cs.unb.ca:24842/signin', user, axiosConfig)
      .then((res) => {
        app.res=res.data;
      })
      .catch((err) => {
        app.res= err;
      });
    },
  }
})
