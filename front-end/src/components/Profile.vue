<template>
    <div>
        <button type="button" class="btn btn-success" v-on:click="getUser">Update Account</button>
        <label v-if="updating">Current Display Name:</label>
        <input v-if="updating" id="currentName" v-model="currentName" readonly>
        <label v-if="updating">New Display Name:</label>
        <input v-if="updating" id="newName" v-model="screen_name">
        <button v-if="updating" type="button" class="btn btn-success" v-on:click="updateUser">Update Screen Name</button>
        <button type="button" class="btn btn-danger" v-on:click="deleteUser">Delete Account</button>
        <button type="button" class="btn btn-primary" v-on:click="goHome">Back</button>
    </div>
</template>
<script>
import axios from "axios";

export default {
    data() {
        return {
            screen_name: '',
            currentName: '',
            updating: false
        }
    },
    methods: {
        goHome: function(){
            this.$router.push('/home');
        },
        getUser: function () {
            let axiosConfig = {
                headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "Access-Control-Allow-Origin": "*",
                }
            };
            axios.get('https://info3103.cs.unb.ca:24842/users?user=' + this.$root.user.username, this.screen_name, axiosConfig)
                .then((res) => {
                this.currentName = res.data['users'][0]['screen_name'];
                this.updating = true;
                })
                .catch((err) => {
                });
        },
        updateUser: function () {
            let axiosConfig = {
                headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "Access-Control-Allow-Origin": "*",
                }
            };
            axios.put('https://info3103.cs.unb.ca:24842/users/' + this.$root.user.username, { screen_name: this.screen_name }, axiosConfig)
                .then((res) => {
                this.updating = false;
                })
                .catch((err) => {
                });
        },
        deleteUser: function () {
            let axiosConfig = {
                headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "Access-Control-Allow-Origin": "*",
                }
            };
            axios.delete('https://info3103.cs.unb.ca:24842/users/' + this.$root.user.username, axiosConfig)
                .then((res) => {
                this.$root.notLoggedIn = true;
                this.$router.push('/');
                })
                .catch((err) => {
                });
        }
    }
}
</script>
