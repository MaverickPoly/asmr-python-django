function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}


function addToCart(product_id) {
    fetch("add_to_cart/", {
       method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({id: product_id}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
        else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error: " + error);
    });
}

function removeFromCart(product_id) {
    console.log(product_id);
    fetch("remove_from_cart/", {
       method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({id: product_id}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
        else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error: " + error);
    });
}
