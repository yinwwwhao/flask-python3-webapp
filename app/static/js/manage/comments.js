const { createApp } = Vue;
function initApp(data) {
    const app = createApp({
        data() {
            return {
                comments: data.comments,
            }
        },
        methods: {
            delete_comment: function (comment) {
                if (confirm('确认要删除评论“' + comment.content + '”？删除后不可恢复！')) {
                    $.post('/api/comments/' + comment.id + '/delete', function (r) {
                        location.reload();
                    });
                }
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
$(function () {
    $.get('/api/comments', {
        page: page
        }, function (r) {
        initApp(r);
    });
    });