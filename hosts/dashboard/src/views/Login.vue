<template>
	<div id="login">
		<v-form @keyup.native.enter="login">
			<v-text-field
				v-model="username"
				prepend-icon="person"
				name="username"
				label="Username"
				placeholder="20000xxx"
				type="text"
				autocomplete="username"
				autofocus />
			<v-text-field
				v-model="password"
				prepend-icon="lock"
				name="password"
				label="Password"
				type="password"
				autocomplete="current-password" />

			<v-btn @click="login">Login</v-btn>
			<p v-if="failed" class="mt-2 red--text">
				Login failed. Please try again.
			</p>
		</v-form>

		<v-btn flat outline class="ma-4" @click="demo">Demo</v-btn>
	</div>
</template>

<script>
export default {
	name: 'Login',
	data() {
		return {
			username: '',
			password: '',
			failed: false,
		};
	},
	methods: {
		login() {
			let account = {
				username: this.username,
				password: this.password,
			};

			this.$store.dispatch('login', account)
			.then(() => { this.$router.push('/balance') })
			.catch(() => {
				this.failed = true;
				this.password = '';
			});
		},

		demo() {
			this.$store.dispatch('demo')
			.then(() => { this.$router.push('/balance') });
		}
	},
};
</script>

<style scoped>
#login {
	margin: auto;
}
</style>
