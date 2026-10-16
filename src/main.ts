import '@/assets/main.css';

import {createApp} from 'vue';
import App from '@/App.vue';
import router from '@/router';
import {i18n} from "@/i18n";
import {createPinia} from 'pinia'

const app = createApp(App);

app
    .use(createPinia())
    .use(router)
    .use(i18n);

app.mount('#app');
