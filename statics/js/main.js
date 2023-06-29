const todoList = document.querySelector(".todos");

todoList.addEventListener("keydown", (e) => {
   if (e.keyCode == 13) {
      e.preventDefault();
      e.target.blur();
   }
});

function check(el) {
   const taskId = el.id;
   const span = el.nextElementSibling;
   const parent = el.closest("li");

   if (el.checked) {
      span.removeAttribute("contenteditable");
      parent.classList.add("complete");
      update(taskId, "complete", 1);
   } else {
      span.setAttribute("contenteditable", "true");
      parent.classList.remove("complete");
      update(taskId, "complete", 0);
   }
}

function edit(el) {
   if (el.dataset.name != el.textContent) {
      const taskId = el.closest("li").id;

      el.dataset.name = el.textContent;
      update(taskId, "title", el.textContent);
   }
}

function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
         var cookie = cookies[i].trim();
         if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
         }
      }
   }
   return cookieValue;
}

function update(id, key, value) {
   var formData = new FormData();

   formData.append(key, value);

   // formData.append("csrfmiddlewaretoken", "{{ csrf_token }");
   fetch(`update/${id}/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
         "X-Requested-With": "XMLHttpRequest",
         "X-CSRFToken": getCookie("csrftoken"),
      },

      body: formData,
   })
      .then((response) => response.text())
      .then((data) => {
         location.reload();
      });
}

// function update_0(id, status) {
//    // Launch an AJAX request
//    const xhr = new XMLHttpRequest();
//    xhr.open("POST", `update/${id}/`);
//    xhr.withCredentials = true;
//    // xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//    xhr.setRequestHeader("Content-Type", "multipart/form-data");
//    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
//    var fd = new FormData();
//    fd.append("complete", status);

//    // Set the data to be sent in the request body
//    // const data = {
//    //    complete: status,
//    // };

//    // Convert the data to a JSON string and send the request
//    // xhr.send(JSON.stringify(data));
//    xhr.send(fd);

//    // Handle the response
//    xhr.onload = function () {
//       // This function executes when we receive a successful response from the backend
//       // Unpack the response
//       // const response = JSON.parse(xhr.responseText);
//       // const result = response.result;
//       // Update the HTML page
//       // console.log(xhr.responseText);
//    };
// }
