<template>
    <div>
        <table>
            <tr>
                <th>Username</th>
                <th>screen_name</th>
            </tr>
            <tr v-for="user in users" v-on:click="getLists(user)">
                <td>{{ user.username }}</td>
                <td>{{ user.screen_name }}</td>
            </tr>
        </table>
        <table>
            <tr>
                <th>List</th>
                <th>Description</th>
            </tr>
            <tr v-for="list in lists" v-on:click="getItems(list)">
                <td>{{ list.title }}</td>
                <td>{{ list.description }}</td>
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
            items: []
        }
    },
    methods: {
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
        getLists: function() {
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
			};
			axios.get('https://info3103.cs.unb.ca:24842/Lists', {
				params: {
					user: this.$root.user.username
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
            console.log(list);
        }
    },
    beforeMount() {
        this.getUsers();
    }
}
</script>
