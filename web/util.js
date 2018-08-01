

function stripPhoneNumber(phoneNumber) {
  var result = '';
  for (var i = 0; i < phoneNumber.length; i++) {
    if (phoneNumber[i] >= '0' && phoneNumber[i] <= '9') {
      result += phoneNumber[i];
    }
  }
  if (result.length < 10) {
      return null;
  }
  result = result.substr(result.length - 10);
  return result;
}


function getCookie(key) {
    var value = ' ' + document.cookie;
    var start = value.indexOf(' ' + key + '=');
    if (start == -1) {
        value = null;
    }
    else {
        start = value.indexOf('=', start) + 1;
        var end = value.indexOf(';', start);
        if (end == -1) {
            end = value.length;
        }
        value = value.substring(start, end);
        if (value == 'null') {
          value = null;
        }
    }
    return value;
}

function setCookie(keyValue) {
  document.cookie = keyValue + '; expires=Fri, 31 Dec 9999 23:59:59 GMT';
          
}

function deleteCookie(key) {
    document.cookie = key + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};


function log(text) {
  var date = new Date();
  console.log(date.toLocaleTimeString() + ' - ' + text);
}