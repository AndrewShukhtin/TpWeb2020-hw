// AJAX for posting
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
    if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function create_like(id, type) {
  var csrftoken = getCookie('csrftoken');

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $.ajax({
    url: 'http://localhost:8000/ajax/',
    type: 'post',
    data: {id: id, type: type},
    success: function(data) {
      var doc = document.getElementById(type + id)
      if ( doc.value == data.likes_count) {
          alert('Вы уже лайкали этот пост! ' + type)
      }
      doc.value = data.likes_count
      doc.min = data.likes_count
        doc.max =  data.likes_count
    },
    failure: function(data) {
      alert('Oшибочка!')
    }
  })
};

function mark_as_correct(qid) {
  var csrftoken = getCookie('csrftoken');

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $.ajax({
    url: 'http://localhost:8000/answer/ajax/correct',
    type: 'post',
    data: {id: qid},
    success: function(data) {
      document.getElementById('correct' + qid).innerHTML = "Correct!"
      var button = document.getElementById('button' + qid)
      button.parentNode.removeChild(button)
    },
    failure: function(data) {
      alert('Oшибочка!')
    }
  })
}