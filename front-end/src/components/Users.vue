<template>
    <div>
        <div class="profile">
            <p>Filter Users</p>
            <input class="search-bar" v-model="filter" v-on:keyup="filterUsers">
            <button type="button" class="btn btn-primary" v-on:click="goHome">Back</button>
        </div>
        <table>
            <tr>
                <th>Username</th>
                <th>Screen Name</th>
            </tr>
            <tr class="tbl-row" v-for="user in users" v-on:click="getLists(user)">
                <td>{{ user.username }}</td>
                <td>{{ user.screen_name }}</td>
            </tr>
        </table>
        <table v-if="hasLists">
            <tr>
                <th>List</th>
                <th>Description</th>
            </tr>
            <tr class="tbl-row" v-for="list in lists" v-on:click="getItems(list)">
                <td>{{ list.title }}</td>
                <td>{{ list.description }}</td>
            </tr>
        </table>
        <table v-if="hasItems">
            <tr>
                <th>Item</th>
                <th>Description</th>
            </tr>
            <tr class="tbl-row" v-for="item in items">
                <td>{{ item.title }}</td>
                <td>{{ item.description }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            users: [],
            allUsers: [],
            lists: [],
            items: [],
            filter: '',
            hasLists:false,
            hasItems: false
        }
    },
    methods: {
        goHome: function(){
            this.$router.push('/home');
        },
        filterUsers: async function() {
            this.hasLists = false;
            this.hasItems = false;
            this.lists = [];
            this.items = [];
            let temp = [];
            this.users = this.allUsers;
            for(var i = 0; i < this.users.length; i ++) {
                if (this.filter.includes(this.users[i].username) || 
                    this.users[i].username.includes(this.filter)) {

                    temp.push(this.users[i]);
                    continue;
                }
                if(this.users[i].screen_name !== null  && 
                (this.filter.includes(this.users[i].screen_name) || 
                this.users[i].screen_name.includes(this.filter))) {

                    temp.push(this.users[i]);
                    continue;
                }
	        }
	    
	        this.users = temp;
        },
        getUsers: function() {
        let axiosConfig = {
                headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "Access-Control-Allow-Origin": "*",
                }
            };
            axios.get('https://info3103.cs.unb.ca:24842/users', axiosConfig)
                .then((res) => {
                    this.users = res.data['users'];
                    this.allUsers = this.users;
                })
                .catch((err) => {
                });
        },
        getLists: function(user) {
            this.hasItems = false;
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
			};
			axios.get('https://info3103.cs.unb.ca:24842/lists', {
				params: {
					user: user.username
				}
			}, axiosConfig)
			.then((res) => {
                this.lists = res.data['lists'];
                if(this.lists.length > 0) {
                    this.hasLists = true;
                }
                else {
                    this.hasLists = false;
                }
			})
			.catch((err) => {
                this.res= err;
                this.hasLists = false;
			});
        },
        getItems: function(list) {
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
			};
			axios.get('https://info3103.cs.unb.ca:24842/lists/' + list.id + '/items', axiosConfig)
			.then((res) => {
                this.items = res.data['items'];

                if(this.items.length > 0) {
                    this.hasItems = true;
                }
                else {
                    this.hasItems = false;
                }
			})
			.catch((err) => {
                this.res= err;
                this.hasItems = false;
			});
        }
    },
    beforeMount() {
        this.getUsers();
    }
}
</script>
