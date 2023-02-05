const { createApp } = Vue;
function initApp(data) {
    const app = createApp({
        data() {
            return {
                blogs: data.blogs
            }
        },
        methods: {
                edit_blog: function (blog) {
                    location.assign('/manage/blogs/edit?id=' + blog.id);
                },
                delete_blog: function (blog) {
                    if (confirm('确认要删除“' + blog.name + '”？删除后不可恢复！')) {
                        $.post('/api/blogs/' + blog.id + '/delete', function (r) {
                            location.reload();
                        });
                    }
                }
        }
    });
    app.mount('#app');
    const page = createApp({
        data() {
            console.log(data.page)
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
    $.get('/api/blogs', {
        page: page
    }, function (r) {
        initApp(r);
    });
});