
const { createApp } = Vue;

function initApp(data) {
    const upload_file = createApp({
        data() {
            return {
                private: false,
            };
        },
        methods: {
            submit: function () {
                if (!document.getElementById("upload").files[0]) {
                    UIkit.notification({
                        message: "请上传文件！",
                        status: "danger",
                    });
                    return;
                }
                var file = document.getElementById("upload").files[0];
                if (file.type.substring(0, 5) != "image") {
                    UIkit.notification({
                        message: "请上传图片！",
                        status: "danger",
                    });
                    return;
                }
                var reader = new FileReader();
    
                var that = this;
                reader.onload = function (e) {
                    var urlData = e.target.result.split(",")[1];
    
                    $.post(
                        "/api/atlas/create",
                        {
                            data: urlData,
                            filetype: file.name.split(".")[file.name.split(".").length - 1],
                            private: that.private,
                        },
                        function (r) {
                            location.reload();
                        }
                    );
                };
                reader.readAsDataURL(file);
            },
            loadimg: function () {
                var reader = new FileReader();
                var file = document.getElementById("upload").files[0];
                reader.onload = function (e) {
                    var urlData = e.target.result;
                    document.getElementById(
                        "result"
                    ).innerHTML = `<img data-src="${urlData}" width="300" uk-img>`;
                };
                reader.readAsDataURL(file);
            },
        },
    })
    upload_file.mount("#upload-file");


    const app = createApp({
        data() {
            return {
                images: data.atlas,
            };
        },
        methods: {
            delete_image: function (i) {
                if (confirm("确认要删除？删除后不可恢复！")) {
                    $.post("/api/atlas/delete", { id: i.id }, function () {
                        location.reload();
                    });
                }
            },
            re_private: function (id, boolean) {
                $.post("/api/atlas/private", { id: id, private: boolean }, function (r) {
                    location.reload();
                });
            },
        },
    })
    app.mount("#app");

    
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
$.get('/api/atlas', {
    page: page
}, function (r) {
    initApp(r);
});
