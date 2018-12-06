<template>
    <div class="profile">
        <button v-if="updating" type="button" class="btn btn-success" v-on:click="hide">Update Account</button>
        <button v-else type="button" class="btn btn-success" v-on:click="getUser">Update Account</button>
        <label v-if="updating">New Display Name</label>
        <input v-if="updating" id="newName" v-model="screen_name">        
        <label v-if="updating">Current Display Name</label>
        <input v-if="updating" id="currentName" v-model="currentName" readonly>
        <button v-if="updating" type="button" class="btn btn-success" v-on:click="updateUser">Update Screen Name</button>
        <button type="button" class="btn btn-danger" v-on:click="confirm">Delete Account</button>
        <button v-if="deleting" type="button" class="btn btn-danger" v-on:click="deleteUser">Click to Delete</button>
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
            updating: false,
            deleting: false
        }
    },
    methods: {
        goHome: function(){
            this.$router.push('/home');
        },
        confirm: function () {
            this.deleting = !this.deleting;
        },
        hide: function () {
            this.updating = false;
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
            if(this.screen_name === '' || this.screen_name === null) {
                alert("Please Enter a Name");
                return;
            }
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
            axios.delete('https://info3103.cs.unb.ca:24842/signin', axiosConfig)
                .then((res) => {
                    router.push('/');
                })
                .catch((err) => {
                    this.res = err;
                });
            }
    }
}
</script>
