let vue = new Vue({
   el: '#form',
   delimiters: ['${', '}'],
   data: {
       // v-model
       username: '',
       password: '',
       emailcode: '',
       email: '',

       // v-show
       error_username: false,
       error_password: false,
       error_email: false,
       error_emailcode: false,

       // v-message
       error_username_msg: '请输入长度3-8的字母数字字符！',
       error_password_msg: '请输入长度8-16的字符！',
       error_email_msg: '邮箱格式不正确！',
       error_emailcode_msg: '验证码输入有误！',

       // 邮箱验证码相关变量
       emailcode_btn: '发送验证码',
       send_flag: false,

   },
    methods: {
       send_emailcode: function() {
           // 发送邮箱验证码
           // 1.判断邮箱验证码是否正在发送
           if (this.send_flag) {
               return;
           }

           // 2.修改发送状态
           this.send_flag = true;

           // 3.校验用户输入的邮箱
           this.check_email();
           if (this.error_email) {
               this.send_flag = false;
               return;
           }

           // 4.发送邮箱验证码
           var url = '/code/send_emailcode/' + this.email + '/';
           axios.get(url, {
               responseType: 'json'
           }).then(response => {
               if (response.data.code == '200') {
                   let num = 60;
                   var i = setInterval(() => {
                       if (num == 1) {
                           clearInterval(i);
                           this.emailcode_btn = '发送验证码';
                           this.send_flag = false;
                       } else {
                           num -= 1;
                           this.emailcode_btn = '倒计时：' + num + '秒';
                       }
                   }, 1000, 60)
                   // 显示测试验证码提示
                   if (response.data.msg) {
                       console.log(response.data.msg);
                   }
               } else {
                   if (response.data.code == '4001') {
                       this.error_email_msg = response.data.errormsg;
                       this.error_email = true;
                   }
                   // 重置发送状态
                   this.send_flag = false;
               }
           }).catch(error => {
               console.log(error.response);
               this.send_flag = false;
           });

       },

       check_emailcode: function() {
           // 邮箱验证码格式校验
           let reg = /^\d{6}$/;
           if (!reg.test(this.emailcode)) {
               this.error_emailcode = true;
               this.error_emailcode_msg = '验证码必须是6位数字';
           } else {
               this.error_emailcode = false;
           }

           if (!this.error_emailcode) {
               axios.get('/code/check_emailcode/' + this.email + '/?emailcode=' + this.emailcode).then(response => {
                   let code = response.data.code
                   if (code != 200) {
                       this.error_emailcode = true;
                       this.error_emailcode_msg = response.data.errormsg;
                   } else {
                       this.error_emailcode = false;
                   }
               });
           }
       },

       // 校验用户名(只能输入3-8位字母数字字符)
       check_uname: function() {
           // 1.格式校验
           let reg = /^[A-Za-z][A-Za-z0-9_]{2,7}$/;
           if (!reg.test(this.username)) {
               this.error_username = true;
           } else {
               this.error_username = false;
           }

           // 2.用户名是否重复注册校验
           if (!this.error_username) {
               axios.get('/user/check_username/' + this.username + '/', {
                   responseType: 'json'
               }).then(response => {
                   if (response.data.count == 1) {
                       this.error_username_msg = '当前用户名已经注册';
                       this.error_username = true;
                   } else {
                       this.error_username = false;
                   }
               }).catch(error => {
                   console.log(error.response);
               });
           }
       },

       // 校验密码
       check_pwd: function() {
           let reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/;
           if (!reg.test(this.password)) {
               this.error_password = true;
           } else {
               this.error_password = false;
           }
       },

       // 校验邮箱
       check_email: function() {
           // 1.格式校验
           let reg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
           if (!reg.test(this.email)) {
               this.error_email = true;
           } else {
               this.error_email = false;
           }

           // 2.邮箱是否重复注册校验
           if (!this.error_email) {
               axios.get('/user/check_email/' + this.email + '/', {
                   responseType: 'json'
               }).then(response => {
                   if (response.data.count == 1) {
                       this.error_email_msg = '邮箱已经被注册';
                       this.error_email = true;
                   } else {
                       this.error_email = false;
                   }
               }).catch(error => {
                   console.log(error.response);
               });
           }
       },

       // 监听表单提交事件
       reg_sub: function() {
           this.check_uname();
           this.check_email();
           this.check_pwd();
           this.check_emailcode();

           if (this.error_username || this.error_email || this.error_password || this.error_emailcode) {
               // 阻止表单提交
               window.event.returnValue = false;
           }
       }

    }
});
