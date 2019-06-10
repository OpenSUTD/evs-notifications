<template>
  <div id="notifications">
    <h1 class="mb-3">Notifications</h1>
    <p>Set up Telegram notifications when your credit balance falls below a preset threshold.</p>
    <a class="ma-3" href="https://t.me/evs_notification_bot">
    	<v-hover>
	    	<img 
	    		slot-scope="{ hover }" 
	    		:class="`elevation-${hover ? 4 : 0}`"
	    		src="https://telegram.org/img/t_logo.png">
	    </v-hover>
    </a>
  </div>
</template>

<script>
export default {
  name: 'Notifications',
};
</script>

<style scoped>
#notifications {
  height: 100%;
  width: 70%;
  margin: auto;
  padding-top: 60px;
}

a {
	display: inline-block;
}

img {
	height: 128px;
	border-radius: 50%;
}

</style>