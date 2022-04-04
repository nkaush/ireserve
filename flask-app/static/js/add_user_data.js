function add_user_data(event) {
    const url = "/register";
    const data = {
      'FirstName' : document.getElementById('first_name').value,
      'LastName' : document.getElementById('last_name').value,
      'Email' : document.getElementById('email').value,
      'HashedPassword' : document.getElementById('password').value,
    };
  
    console.log(data);
  
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
      if (response.redirected) {
        window.location.href = response.url;
      }
    })
    .catch(err => {
      console.error(err.message);
    });
  
    return false;
  }