function add_user_data(event) {
    const url = "/register"
    const data = {
        'FirstName' : document.getElementById('first_name').value,
        'LastName': document.getElementById('last_name').value,
        'Email': document.getElementById('email').value,
        'HashedPassword': document.getElementById('password').value,
    };

    console.log(data);
    console.log(JSON.stringify(data))

    // fetch(url, {
    //     "method": "POST",
    //     "mode" : "cors",
    //     "redirect": "manual",
    //     "headers": {
    //         "Content-Type": "application/json"
    //     },
    //     "body": JSON.stringify(data)
    // })
    // .then(function(response) {
    //     response.json().then((data) => {
    //         console.log(data);
    //         document.getElementById('message').innerHTML = data.message;
    //     });
    // })
    // .catch(err => {
    //     console.error(err);
    //     document.getElementById('message').innerHTML = err.message;
    // });
    return false;
}