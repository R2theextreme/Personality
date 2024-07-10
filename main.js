import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

createApp(App).use(router).mount('#app');
$(document).ready(function() {
    $('.tag').click(function() {
        $(this).toggleClass('selected');
    });
});
