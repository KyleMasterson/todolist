<template>
    <div>
        <h1>Looks like you wandered off the beaten path</h1>
        <button type="button" class="btn btn-primary" v-on:click="goToIndex">Back to Safety</button>
    </div>
</template>
<script>
export default {
    methods: {
        goToIndex: function(){
            this.$router.push('/');
        }
    }
}
</script>
