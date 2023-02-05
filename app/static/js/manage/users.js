const { createApp } = Vue;
function initApp(data) {
    const app = createApp({
        data() {
            return {
                users: data.users,
            }
        }
    })
    app.mount('#app');
    const page = createApp({
        data() {
            return {
                page: data.page
            }
        },
    })
    page.mount('#page');
}
var url = new URL(location.href);
if (url.searchParams.has('page')) {
    page = url.searchParams.get('page');
} else {
    page = '1';
}
$(function() {
        $.get('/api/users', {
                page: page
            }, function (r) {
                initApp(r);
            });
        });