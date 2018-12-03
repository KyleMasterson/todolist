<template>
    <div>
        <h1 v-if="$root.user.screenName===null||$root.user.screenName===''">Welcome home, {{ $root.user.username }}</h1>
		<h1 v-else>Welcome home, {{ $root.user.screenName }}</h1>
        <br>
        <button v-on:click="gotoProfile">Profile</button>
        <h2>Todo Lists:</h2>
        <button v-on:click="getLists">Get Lists</button>
        
        <p>New List Name </p>
        <input Type="text" v-model="name" placeholder="Name goes here">
        <p>New List Discription</p>
        <input Type="text" v-model="description" placeholder = "Description Goes Here">
        <br>
        <button v-on:click="addList">Add List</button>

        <table>
            
        </table>
    </div>
</template>

<script>
import axios from "axios";
const url = 'https://info3103.cs.unb.ca:24842/lists';
export default {
    
    data() {
        return {
            name: '',
            description: ''
        }
    },
    methods:{
        gotoProfile: function(){
            this.$router.push('/profile');
        },
        getLists: function(){
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
			};
			axios.get(url, {
				params: {
					username: this.$root.user.username
				}
			}, axiosConfig)
			.then((res) => {
				this.res=res.data;
			})
			.catch((err) => {
				this.res= err;
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
        },
    }

}
</script>
