<template>
    <div>
        <h1 v-if="$root.user.screenName===null||$root.user.screenName===''">Welcome home, {{ $root.user.username }}</h1>
		<h1 v-else>Welcome home, {{ $root.user.screenName }}</h1>
        <br>
        <button v-on:click="gotoProfile">Your Profile</button>
        <button v-on:click="gotoUsers">Find Friends</button>
        <h2>Todo Lists:</h2>
        <p>New List Name </p>
        <input Type="text" v-model="name" placeholder="Name goes here">
        <p>New List Discription</p>
        <input Type="text" v-model="description" placeholder = "Description Goes Here">
        <br>
        <button v-on:click="addList">Add List</button>
        <br>
        <br>
        <div id="table">
            <table>
                <thead>
                    <tr>
                        <td>Your Lists</td>
                    </tr>
                </thead>
            </table>

            
        
            <table>
                <tbody>
                    <tr v-for="row in lists" v-on:click="getItems(row)">
                        <td>
                            {{ row.title }}
                        </td>
                        <td>
                            {{ row.description }}
                        </td>
                    </tr>
                </tbody>
            </table>
            <table>
                <tr v-for="item in items">
                    <td>
                        {{item.title}}
                    </td>
                    <td>
                        {{item.description}}
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import axios from "axios";
const url = 'https://info3103.cs.unb.ca:24842/lists';
export default {
    
    data() {
        return {
            name: '',
            description: '',
            lists: [],
            items: [],
            res: ""
        }
    },
    methods:{
        gotoProfile: function(){
            this.$router.push('/profile');
        },
        gotoUsers: function(){
            this.$router.push('/users');
        },
        getLists: function(){
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
            };
            const vm = this;
			axios.get(url, {
				params: {
					username: this.$root.user.username
				}
			}, axiosConfig)
			.then((res) => {
				vm.lists=res.data["lists"];
			})
			.catch((err) => {
				vm.res= err;
            });


        },
        addList: function(){
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
            };
            	axios.post(url, {
				title: this.name,
				description: this.description
			}, axiosConfig)
			.then((res) => {
				this.res=res.data;
			})
			.catch((err) => {
				this.res= err;
            });
            this.lists = [];
            this.getLists();
            this.name ='';
            this.description='';
        },
        getItems: function(list){
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
			};
			axios.get('https://info3103.cs.unb.ca:24842/lists/' + list.id + '/items', axiosConfig)
			.then((res) => {
				this.items = res.data['items'];
			})
			.catch((err) => {
				this.res= err;
			});
        }
        
    },
    beforeMount() {
            this.getLists();
    }

}
</script>

