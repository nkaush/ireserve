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
      if (response.redirected) {
        window.location.href = response.url;
      }
    })
    .catch(err => {
      console.error(err.message);
    });
  
    return false;
  }