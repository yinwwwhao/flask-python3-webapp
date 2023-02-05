var url = new URL(location.href);
console.log(url);
if (url.searchParams.has('id')) {
    ID = url.searchParams.get('id');
} else {
    ID = '';
}
const { createApp } = Vue;
function initApp(blog) {
    createApp({
        data() {
            return blog;
        },
        methods: {
            submit: function () {
                $.post('/api/blogs', this.$data, function (r) {
                    if (r.id) {
                        //location.assign('/api/blogs/' + r.id);
                        location.assign('/manage/blogs');
                    } else {
                        alert(r.message.error.type, r.message.error.text);
                    }
                });
            },
        },
    }).mount("#app");
}
$(function () {
    if (ID) {
        $.get("/api/blogs/" + ID, function (blog) {
            blog.id = ID;
            initApp(blog);
        });
    } else {
        initApp({
            name: "",
            summary: "",
            content: "",
            tag: "",
        });
    }
});