var app=new Vue({
  el: '#app',
  data: {
    // status: '',
    schs:  '',
    sch: '',
    addedSch: ''
  },
  created: function () {
  },
  methods:{
      addSchool : function (){

        var postData = {
          Name: "sch2",
          Province: "NB",
          Language: "EN",
          Level: "simple"

            };
          let axiosConfig = {
              headers: {
                  'Content-Type': 'application/json;charset=UTF-8',
                  "Access-Control-Allow-Origin": "*",
              }
            };
            axios.post('http://info3103.cs.unb.ca:61011/schools', postData, axiosConfig)
            .then((res) => {
              app.addedSch=res.data;
            })
            .catch((err) => {
              app.addedSch= err;
            });
    },//end addSchool

        schoolIDget: function (schid) {
          // this.status='loading';
          var app=this;
          axios.get('http://info3103.cs.unb.ca:61011/schools/'+schid)
          .then(function (response){
            app.sch=response.data;
          })
          .catch(function(error){
            app.sch='An error ocurred: '+error;

          });

        },//end schoolIDget

        schoolsget: function () {
          // this.status='loading';
          var app=this;
          axios.get('http://info3103.cs.unb.ca:61011/schools')
          .then(function (response){
            app.schs=response.data.schools;
          })
          .catch(function(error){
            app.schs='An error ocurred: '+error;

          });

        },//end schoolsget

      }//end methods

    })//end Vue
