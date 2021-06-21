// file tha handle the fact of adding to cart

let cart = document.getElementsByClassName('tip')[3];
let addBtn = document.querySelector('.cart-btn');
let input = document.getElementById('add-input');

let product = {
    category: window.location.pathname.split('/')[2],
    id: window.location.pathname.split('/')[3],
    labelSizes: Array.from(document.querySelectorAll('label[id="size__radio"]')),
    colors: Array.from(document.querySelectorAll('input[name="color__radio"]')),
    color: function () {
        for (x in this.colors) {
            if (this.colors[x].checked) {
                return this.colors[x].id
            }
        }
        return null
    },
    size: function () {
        // console.log(labelSizes)
        for (x in this.labelSizes) {
            if (this.labelSizes[x].className == 'active') {
                return this.labelSizes[x].innerText
            }
        }
        return null
    }
}


function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break
            }
        }
    }
    return cookieValue;
}

let csrftoken = getToken('csrftoken');
console.log(`The csrfToken is ${csrftoken}`);


function makeFetch(product, addBtn = null) {
    cart.textContent = Number(cart.textContent) + Number(input.value)

    let url = '/add_to_cart/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            'order_quantity':cart.textContent,
            'input': input.value,
            'productId': product.id,
            'category': product.category,
            'color': product.color(),
            'size': product.size()
        })
    })
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log(data)

        })
    
    
}



function addTocart(e) {
    e.preventDefault()

    if ((product.color() && product.size())) {
        makeFetch(product, addBtn)

    } else if (addBtn && product.color() && product.labelSizes.length < 1) {
        makeFetch(product, addBtn)
    } else if (addBtn && product.labelSizes.length < 1 && product.colors.length < 1) {
        makeFetch(product, addBtn)
    } else {
        alert('You have to make choices with sizes colors')
    }

    


}

// Button add activate
try {
    addBtn.addEventListener('click', addTocart)
} catch (e) {
    console.log('you cannot add something to the cart')
}

// addBtn.addEventListener('click', (e) => {
//     console.log(product.color().id)
// })
