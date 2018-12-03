<template>
    <div>
        <h1>Welcome home, {{ $root.user.username }}</h1>
        <br>
        <button v-on:click="gotoProfile">Profile</button>
        <h2>Todo Lists:</h2>
        <button v-on:click="getLists">Click Me!</button>
        
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
import VueRouter from "vue-router";
import Vue from "vue";
const url = 'https://info3103.cs.unb.ca:24843/lists';
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
				params: {
                    title: this.name,
                    description: this.description
				}
			}, axiosConfig)
			.then((res) => {
				this.res=res.data;
			})
			.catch((err) => {
				this.res= err;
			});
        }
    }

}
</script>
