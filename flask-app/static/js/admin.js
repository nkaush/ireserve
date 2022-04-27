function call_stored_procedure(event) {
  const url = "/call-stored-procedure";
  const data = { };

  var btn = document.getElementById("stored-procedure-button")
  var btn_text = document.getElementById("stored-procedures-status-text")
  var btn_spinner = document.getElementById("stored-procedure-spinner")
  
  btn.disabled = true;
  btn_text.innerHTML = "Loading...";
  btn_spinner.style.display = "inline";

  fetch(url, {
    "method": "POST",
    "mode" : "cors",
    "headers": {
        "Content-Type": "application/json; charset=UTF-8"
    },
    "body": JSON.stringify(data)
  })
  .then(function(response) {
    console.log(response.url);
    
    if (response.status < 400) {
      response.json().then((data) => {
        console.log(data);
        var msg = document.getElementById('message');
        msg.className = "";
        msg.classList.add("success", "alert", "alert-success")
        msg.innerHTML = data.message;
        document.getElementById('table-row-' + room_id).style.display = "none";
      });
    } else {
      response.json().then((data) => {
        console.log(data);
        var msg = document.getElementById('message');
        msg.className = "";
        msg.classList.add("alert", "alert-warning", "alert-dismissible", "fade", "show")
        msg.innerHTML = data.message;
      });
    }
  })
  .catch(err => {
    console.error(err.message);
    err.json().then((data) => {
      console.log(data);
      var msg = document.getElementById('message');
      msg.className = "";
      msg.classList.add("warning", "alert", "alert-warning")
      msg.innerHTML = data.message;
    });
  });

  btn.disabled = false;
  btn_text.innerHTML = "Compute"
  btn_spinner.style.display = "none";
  return false;
}