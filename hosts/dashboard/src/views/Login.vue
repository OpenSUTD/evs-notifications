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

			<v-btn @click="login">
				Login
				<v-progress-circular indeterminate
					v-if="loading"
					class="ml-2"
					size="16"
					width="1" />
			</v-btn>
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
			loading: false,
			failed: false,
		};
	},
	methods: {
		login() {
			this.loading = true;

			let account = {
				username: this.username,
				password: this.password,
			};

			this.$store.dispatch('login', account)
			.then(() => { this.$router.push('/balance') })
			.catch(() => {
				this.failed = true;
				this.password = '';
			})
			.finally(() => { this.loading = false });
		},

		demo() {
			this.loading = true;

			this.$store.dispatch('demo')
			.then(() => { this.$router.push('/balance') })
			.finally(() => { this.loading = false });
		}
	},
};
</script>

<style scoped>
#login {
	margin: auto;
}
</style>
