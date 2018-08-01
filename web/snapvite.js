var g_currentPhoneNumber = null;
var g_currentUserName = null;


Vue.mixin({
  methods: {
    displayPhoneNumber: function(phoneNumber) {
      var result = '';
      var pos = 0;
      for (var i = 0; i < phoneNumber.length; i++) {
        if (pos == 3  ||  pos == 6) {
          result += '-';
        }
        pos++;
        result += phoneNumber[i];
      }
      return result;
    },
    displayDate: function(dateString) {
      // Expects the format yyyy-mm-dd
      let parts = dateString.split('-');
      // Note - Javascript counts months from 0, hence the -1 for that part.
      let date = new Date(parts[0], parts[1] - 1, parts[2]);
      return `${getDayString(date)}, ${getMonthString(date)} ${date.getDate()}`;
    },
    displayTime: function(dateTime) {
      if (dateTime.getHours() == 0  &&  dateTime.getMinutes() == 0) {
        return 'end of day';
      }
      var time = dateTime.toLocaleTimeString();
      time = time.substring(0, time.indexOf(':', 3)) + ' ' + time.substr(time.length - 2);
      return time;
    },
    httpRequest: async function(method, url, body, callback = null, errorHandler = null) {
      var init = {
        method: method
      };
      switch (method) {
        case 'POST':
        case 'PATCH':
          init.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
          };
          init.body = body;
          break;
      }
      try {
        let response = await fetch(url, init);
        if (response.status != 200) {
          let body = await response.text();
          throw(body);
        }
        let json = await response.json();
        log('httpRequest: Response: ' + JSON.stringify(json));
        if (callback) {
          callback(json);
        }
      }
      catch (error) {
        log('httpRequest: Fetch exception: ' + error);
        if (errorHandler) {
          errorHandler(error);
        }
        else {
          this.httpError(error);
        }
      };
    },
    httpError: function(error) {
      vue_infoDialog.show('Network Request Failed', 'Debug info: ' + error, true);
    }
  }
});


var APP_STATE = {
  NONE:       'NONE',
  SIGN_IN:    'SIGN_IN',
  VITE_LIST:  'VITE_LIST',
  VITE_VIEW:  'VITE_VIEW' 
};


var vue_signIn = new Vue({
  el: '#signIn',
  data: {
    phoneNumber: '',
    verificationCode: '',
    vbool_verify: false
  },
  methods: {
    show: function() {
      this.$el.style.display = 'block';
      this.phoneNumber = '';
      this.verificationCode = '';
      this.vbool_verify = false;
    },
    register_onClick: function() {
      let json = {
        phoneNumber: stripPhoneNumber(this.phoneNumber)
      };
      if (!json.phoneNumber) {
        vue_infoDialog.show('Invalid Phone Number', 'Please enter a 10 digit phone number', true);
        return;
      }

      this.httpRequest('POST', '/users', JSON.stringify(json), () => {
        this.vbool_verify = true;
      });
    },
    verify_onClick: function() {
      let phoneNumberStripped = stripPhoneNumber(this.phoneNumber); 
      let json = {
        phoneNumber: phoneNumberStripped,
        validationCode: this.verificationCode
      };
      this.httpRequest('PATCH', '/users', JSON.stringify(json), (json) => {
        this.httpRequest('GET', '/users/' + phoneNumberStripped, null, (json) => {
          setCookie('phoneNumber=' + phoneNumberStripped);
          g_currentPhoneNumber = phoneNumberStripped;

          if (json.user.userName) {
            setCookie('userName=' + json.user.userName);
            g_currentUserName = json.user.userName;
          }
          else {
            vue_userDialog.show();
          }

          vue_root.updateAppState(APP_STATE.VITE_LIST);
        });
      }, (error) => {
        if (JSON.parse(error).code == '404') {
          vue_infoDialog.show('Verification Failure', 'Incorrect Verification Code', true);
        }
      });
    }
  }
});


var vue_userDialog = new Vue({
  el: '#userDialog',
  data: {
    userName: ''
  },
  methods: {
    show: function() {
      this.userName = g_currentUserName;
      this.$el.classList.add('active');
    },
    setUserName_onClick: function() {
      let json = {
        phoneNumber: g_currentPhoneNumber,
        userName: this.userName
      };
      this.httpRequest('PATCH', '/users', JSON.stringify(json), () => {
        setCookie('userName=' + this.userName);
        g_currentUserName = this.userName;
        this.$el.classList.remove('active');
      });
    },
    cancel_onClick: function() {
      this.$el.classList.remove('active');
    },
    signOut_onClick: function() {
      this.$el.classList.remove('active');
      g_currentPhoneNumber = '';
      g_currentUserName = '';
      deleteCookie('userName');
      deleteCookie('phoneNumber');
      vue_root.updateAppState(APP_STATE.SIGN_IN);
    }
  }
});


var vue_viteList = new Vue({
  el: '#viteList',
  data: {

  },
  methods: {
    show: function() {
      this.$el.style.display = 'block';
      
    }
  }
});


var vue_infoDialog = new Vue({
  el: '#infoDialog',
  data: {
    title: '',
    message: ''
  },
  methods: {
    show: function(title, message, timeout = false) {
      this.title = title;
      this.message = message;
      this.$el.classList.add('active');
      if (timeout) {
        setTimeout(() => { 
          this.$el.classList.remove('active'); 
        }, 2500);
      }
    },
    okay_onClick: function() {
      this.$el.classList.remove('active');
    }
  }
});


var vue_root = new Vue({
  el: '#root',
  data: {
    appState: APP_STATE.NONE
  },
  mounted: function() {
    window.addEventListener('popstate', function(event) {
      updateAppState(event.state.appState, false);
    });

    g_currentPhoneNumber = getCookie('phoneNumber');
    g_currentUserName = getCookie('userName');
    if (!g_currentPhoneNumber  ||  !g_currentUserName) {
      this.updateAppState(APP_STATE.SIGN_IN, false);
    }
    else {
      this.updateAppState(APP_STATE.VITE_LIST, false);
    }
  },
  methods: {
    updateAppState: function(appState, updateBrowserState = true) {
      if (updateBrowserState == true) {
        history.pushState({appState: appState}, '', '');
      }

      vue_signIn.$el.style.display = 'none';
      vue_viteList.$el.style.display = 'none';

      if (appState == APP_STATE.SIGN_IN) {
        this.$el.style.display = 'none';
      }
      else {
        this.$el.style.display = 'block';
      }

      if (appState == APP_STATE.SIGN_IN) {
        vue_signIn.show();
      }
      else if (appState == APP_STATE.VITE_LIST) {
        vue_viteList.show();
      }
    },
    user_onClick: function() {
      vue_userDialog.show();
    }
  }
});

