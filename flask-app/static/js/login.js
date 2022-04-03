function try_login(event) {
  const url = "/login";
  const data = {
    'email' : document.getElementById('email').value,
    'password': document.getElementById('password').value,
  };

  console.log(data);

  fetch(url, {
    "method": "POST",
    "mode" : "cors",
    "redirect": "follow",
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