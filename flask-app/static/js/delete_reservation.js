function delete_reservation(event) {
    const url = "/reservation/delete";
    const data = {
      'ReservationID' : document.getElementById('reservation_id').value,
      
    };
  
    console.log(data);
  
    fetch(url, {
      "method": "DELETE",
      "mode" : "cors",
      "headers": {
          "Content-Type": "application/json; charset=UTF-8"
      },
      "body": JSON.stringify(data)
    })
    .then(function(response) {
      console.log(response.url);
      response.json().then((data) => {
        document.getElementById('message').classList.add("success", "alert", "alert-success")
        document.getElementById('message').innerHTML = data.message;
      });
    })
    .catch(err => {
      console.error(err.message);
      err.json().then((data) => {
        console.log(data);
        document.getElementById('message').classList.add("warning", "alert", "alert-warning")
        document.getElementById('message').innerHTML = data.message;
      });
    });
  
    return false;
  }