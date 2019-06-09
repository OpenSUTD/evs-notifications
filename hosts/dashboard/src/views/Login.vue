<template>
	<div id="login">
		<v-btn @click="login">Login</v-btn>
	</div>
</template>

<script>
export default {
	name: 'Login',
	methods: {
		login() {
	    let account = {
	      username: '20000173',
	      password: null,
	    };
	    this.$store.dispatch('login', account)
	    .then(() => { this.$router.push('/balance') });
		},
	},
};
</script>

<style scoped>
#login {
	height: 100%;
	margin: auto;
	padding-top: 60px;
}
</style>
