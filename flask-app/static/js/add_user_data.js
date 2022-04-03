function add_user_data(event) {
    
    const data = {
        'FirstName' : document.getElementById('first_name').value,
        'LastName': document.getElementById('last_name').value,
        'Email': document.getElementById('email').value,
        'HashedPassword': document.getElementById('password').value,
    };

    console.log(data);

    fetch("/users", {
        "method": "POST",
        "mode" : "cors",
        "headers": {
            "Content-Type": "application/json; charset=UTF-8"
        },
        "body": JSON.stringify(data)
    })
    .then(function(response) {
        response.json().then((data) => {
            console.log(data);
            document.getElementById('message').innerHTML = data.message;
        });
    })
    .catch(err => {
        console.error(err);
        document.getElementById('message').innerHTML = err.message;
    });
    return false;
}