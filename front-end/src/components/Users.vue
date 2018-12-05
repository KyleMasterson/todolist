<template>
    <div>
        <!-- TODO: Search bar to use method to filter user list -->
        <input v-model="filter">
        <button type="button" class="btn btn-success" v-on:click="filterUsers">Search</button>
        <table>
            <tr>
                <th>Username</th>
                <th>screen_name</th>
            </tr>
            <tr class="tbl-row" v-for="user in users" v-on:click="getLists(user)">
                <td>{{ user.username }}</td>
                <td>{{ user.screen_name }}</td>
            </tr>
        </table>
        <table>
            <tr>
                <th>List</th>
                <th>Description</th>
            </tr>
            <tr class="tbl-row" v-for="list in lists" v-on:click="getItems(list)">
                <td>{{ list.title }}</td>
                <td>{{ list.description }}</td>
            </tr>
        </table>
        <table>
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
            lists: [],
            items: [],
            filter: ''
        }
    },
    methods: {
        filterUsers: function() {
            lists = [];
            items = [];
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
                })
                .catch((err) => {
                });
        },
        getLists: function(user) {
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
			})
			.catch((err) => {
				this.res= err;
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
			})
			.catch((err) => {
				this.res= err;
			});
        }
    },
    beforeMount() {
        this.getUsers();
    }
}
</script>
