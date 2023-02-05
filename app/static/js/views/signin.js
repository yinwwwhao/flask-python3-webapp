function validateEmail(email) {
    var re = /^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$/;
    return re.test(email.toLowerCase());
}
const { createApp } = Vue;
$(function () {
    createApp({
        data() {
            return {
                email: "",
                passwd: "",
            };
        },
        methods: {
            submit: function () {
                if (!this.email) {
                    UIkit.notification({
                        message: "请输入邮箱。",
                        status: "danger",
                    });
                    return;
                } else if (!this.passwd) {
                    UIkit.notification({
                        message: "请输入密码。",
                        status: "danger",
                    });
                    return;
                } else if (this.passwd.length < 6) {
                    UIkit.notification({
                        message: "密码长度至少为6个字符。",
                        status: "danger",
                    });
                    return;
                } else if (!validateEmail(this.email.trim().toLowerCase())) {
                    UIkit.notification({
                        message: "请输入正确的邮箱地址。",
                        status: "danger",
                    });
                    return;
                }

                var email = this.email.trim().toLowerCase();
                var that = this;
                $.ajaxSettings.async = false;
                $.getJSON("/api/users", function (r) {
                    for (let x in r.users) {
                        if (email.trim().toLowerCase() === r.users[x].email) {
                            that.signin = true;
                            break;
                        }
                    }
                });
                $.ajaxSettings.async = true;
                if (!this.signin) {
                    UIkit.notification({
                        message: "暂无该用户。",
                        status: "danger",
                    });
                    return;
                }

                $.post(
                    "api/authenticate",
                    {
                        email: email,
                        passwd: this.passwd,
                    },
                    function (r) {
                        if (!r) {
                            location.assign("/");
                        } else {
                            UIkit.notification({
                                'message': '密码错误。',
                                'status': 'danger'
                            });
                        }
                    }
                );
            },
        },
    }).mount("#app");
});
