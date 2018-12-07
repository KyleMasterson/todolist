<template>
    <div>
        <h1 v-if="$root.user.screenName===null||$root.user.screenName===''">Welcome home, {{ $root.user.username }}</h1>
		<h1 v-else>Welcome home, {{ $root.user.screenName }}</h1>
        <br>
        <button class="btn btn-primary" v-on:click="gotoProfile">Your Profile</button>
        <button class="btn btn-primary" v-on:click="gotoUsers">Find Friends</button>
        <h2>Todo Lists:</h2>
        <button class="btn btn-primary" v-on:click="listFlip">New List</button>
        <div v-if="makeList">
            <p>List Name </p>
            <input Type="text" v-model="name" placeholder="Name" v-on:keyup.enter="addList">
            <p>List Discription</p>
            <input Type="text" v-model="description" placeholder = "Description" v-on:keyup.enter="addList">
            <br>
            <button class="btn btn-success" v-on:click="addList">Add List</button>
        </div>
        <br>
        <br>
        <div id="table" v-if="lists.length > 0">
            <table>
                <thead>
                    <tr>
                        <td>Your Lists</td>
                    </tr>
                </thead>
            </table>

            
        
            <table>
                <tbody>
                    <tr class="tbl-row" v-for="row in lists" >
                        <td v-on:click="getItems(row.id)">
                            {{ row.title }}
                        </td>
                        <td v-on:click="getItems(row.id)">
                            {{ row.description }}
                        </td>
                        <td>
                            <button class="btn btn-danger" v-on:click="removeList(row.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <br>
            <div v-if="currList!==0">
                <button class="btn btn-primary" v-on:click="itemFlip">New Item</button>
                <div v-if="makeItem ===true">
                    <p>Item Name</p>
                    <input Type="text" v-model="itemName" placeholder="Name" v-on:keyup.enter="addItem">
                    <p>Item Discription</p>
                    <input Type="text" v-model="itemDesc" placeholder = "Description" v-on:keyup.enter="addItem">
                    <br>
                    <button class="btn btn-success" v-on:click="addItem">Add Item</button>
                </div>
                <div v-if="update">
                    <p>Item Name</p>
                    <input Type="text" v-model="itemName" placeholder="Name" v-on:keyup.enter="updateItem">
                    <p>Item Discription</p>
                    <input Type="text" v-model="itemDesc" placeholder = "Description" v-on:keyup.enter="updateItem">
                    <br>
                    <button class="btn btn-success" v-on:click="updateItem">Update Item</button>
                </div>
                <table v-if="items.length > 0">
                    <thead>
                        <tr>
                            <td>Items</td>
                        </tr>
                    </thead>
                </table>
                <table v-if="items.length > 0">
                    <tr class="tbl-row" v-for="item in items">
                        <td>
                            {{item.title}}
                        </td>
                        <td>
                            {{item.description}}
                        </td>
                        <td>
                            <button class="btn btn-success" v-on:click="updateFlip(item)">Update</button>
                        </td>
                        <td>
                            <button class="btn btn-danger" v-on:click="removeItem(item.id)">Delete</button>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    
    data() {
        return {
            name: '',
            description: '',
            itemName: '',
            itemDesc: '',
            currList: 0,
            lists: [],
            items: [],
            res: "",
            makeList: false,
            makeItem: false,
            update: false,
            currItem: 0
        }
    },
    methods:{
        updateFlip: function(item){
            this.update = !this.update;
            this.currItem = item.id;
            this.itemName = item.title;
            this.itemDesc = item.description;
        },
        listFlip: function(){
            this.makeList = !this.makeList;
            this.currList = 0;
        },
        itemFlip: function(){
            this.makeItem = !this.makeItem;
        },
        currZero: function(){
            this.currList = 0;
        },
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
			axios.get('https://info3103.cs.unb.ca:24842/lists', {
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
        removeList: function(listId){
            this.currZero();
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
            };
            	axios.delete('https://info3103.cs.unb.ca:24842/lists/' + listId, {
			}, axiosConfig)
			.then((res) => {
				this.res=res.data;
			})
			.catch((err) => {
				this.res= err;
            });
            this.lists = [];
            this.getLists();
        },
        addList: function(){
            if(this.name === null || this.name === '') {
                alert("Please enter a Name!");
                return;
            }
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
            };
            axios.post('https://info3103.cs.unb.ca:24842/lists', {
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
            this.listFlip();
        },
        getItems: function(list){
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
			};
			axios.get('https://info3103.cs.unb.ca:24842/lists/' + list + '/items', axiosConfig)
			.then((res) => {
				this.items = res.data['items'];
			})
			.catch((err) => {
				this.res= err;
            });
            this.currList=list;
        },
        addItem: function(){
            if(this.itemName === null || this.itemName === '') {
                alert("Please enter a Name!");
                return;
            }
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
            };
            	axios.post('https://info3103.cs.unb.ca:24842/lists/' + this.currList + '/items', {
				title: this.itemName,
				description: this.itemDesc
			}, axiosConfig)
			.then((res) => {
				this.res=res.data;
			})
			.catch((err) => {
				this.res= err;
            });
            this.items = [];
            this.itemName ='';
            this.itemDesc='';
            this.getItems(this.currList);
            this.itemFlip(); 
        },
        removeItem: function(itemId){
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
            };
            	axios.delete('https://info3103.cs.unb.ca:24842/lists/' + this.currList + '/items/' + itemId, {
			}, axiosConfig)
			.then((res) => {
				this.res=res.data;
			})
			.catch((err) => {
				this.res= err;
            });
            this.items = [];
            this.getItems(this.currList);
        },
        updateItem: function(){
            let axiosConfig = {
				headers: {
					'Content-Type': 'application/json;charset=UTF-8',
					"Access-Control-Allow-Origin": "*",
				}
            };
            axios.put('https://info3103.cs.unb.ca:24842/lists/' + this.currList + '/items/' + this.currItem, { 
                title: this.itemName,
                description: this.itemDesc
            }, axiosConfig)
			.then((res) => {
				this.res=res.data;
			})
			.catch((err) => {
				this.res= err;
            });
            this.updateFlip(0);
            this.getItems(this.currList);
        }
        
    },
    beforeMount() {
            this.getLists();
    }

}
</script>

