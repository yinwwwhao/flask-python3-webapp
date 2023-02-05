function validateEmail(email) {
    var re = /^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$/;
    return re.test(email.toLowerCase());
}
function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}
function setCookie(cname, cvalue) {
    document.cookie = cname.toString() + "=" + cvalue.toString() + ";";
}
function getCookie(cname) {
    var re = new RegExp(`${cname}=(.*?);`);
    var cookie = re.exec(document.cookie + ";");
    if (cookie) {
        return cookie[1];
    } else {
        return null;
    }
}
async function run_ver(app) {
    if (!getCookie("ver_time")) {
        return;
    }
    var $send = $("#send");
    var $input = $("#ver_input")
    $send.addClass("uk-hidden");
    $input.toggleClass("uk-width-2-3", "uk-width-1-1")

    for (let t = Number(getCookie("ver_time")) / 1000; t != 0; t--) {
        app.tips = `${t}秒后重发`;
        setCookie("ver_time", t * 1000);
        await sleep(1000);
    }
    
    app.tips = '邮箱验证码';
    setCookie("ver_time", "");

    $input.toggleClass("uk-width-1-1", "uk-width-2-3")
    $send.removeClass("uk-hidden");
}

const { createApp } = Vue;
$(function () {
    const app = createApp({
        data() {
            return {
                name: "",
                email: "",
                password1: "",
                password2: "",
                verification: "",
                tips:"邮箱验证码"
            };
        },
        mounted() {
            run_ver(this);
        },
        methods: {
            submit: function () {

                if (!this.name.trim()) {
                    UIkit.notification({
                        message: "请输入名字。",
                        status: "danger",
                    });
                    return;
                } else if (!this.email) {
                    UIkit.notification({
                        message: "请输入邮箱。",
                        status: "danger",
                    });
                } else if (!validateEmail(this.email.trim().toLowerCase())) {
                    UIkit.notification({
                        message: "请输入正确的邮箱地址。",
                        status: "danger",
                    });
                    return;
                } else if (this.password1.length < 6) {
                    UIkit.notification({
                        message: "密码长度至少为6个字符。",
                        status: "danger",
                    });
                    return;
                } else if (this.password1 !== this.password2) {
                    UIkit.notification({
                        message: "两次输入的密码不一致。",
                        status: "danger",
                    });
                    return;
                } else if (!this.verification) {
                    UIkit.notification({
                        message: "请输入验证码。",
                        status: "danger",
                    });
                    return;
                }

                var email = this.email.trim().toLowerCase();
                var name = this.name.trim();
                var code = this.verification.trim();

                $.post(
                    "/api/users",
                    {
                        name: name,
                        email: email,
                        passwd: CryptoJS.SHA1(email + ":" + this.password1).toString(),
                        code: code
                    },
                    function (r) {
                        if (r) {
                            if (r.message.error.text === 'code') {
                            UIkit.notification({
                                message: "验证码错误。",
                                status: "danger"
                            });
                        } else if (r.message.error.text === 'Email is already in use.') {
                            UIkit.notification({
                                message: "该用户已注册。",
                                status: "danger"
                            });
                        } else {
                            UIkit.notification({
                                message: r.message.error.type+r.message.error.text,
                                status: "danger"
                            });
                        }
                            return;
                        } else {
                            location.assign("/");
                    }
                    }
                );
            },
            send: async function () {
                if (!this.email) {
                    UIkit.notification({
                        message: "请输入邮箱。",
                        status: "danger",
                    });
                    return;
                }
                if (!validateEmail(this.email.trim().toLowerCase())) {
                    UIkit.notification({
                        message: "请输入正确的邮箱地址。",
                        status: "danger",
                    });
                    return;
                }
                $.post("/api/send_verification", { email: this.email });
                setCookie("ver_time", 60000);
                await run_ver(this);
            },
        },
    });
    app.mount("#app");
});
