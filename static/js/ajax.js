// c'est de l'ajax perso, no Jquery mm si le template utiliser est full de jquery
// l'objectif est de tenter l'ajax sans jquery pour connaitre un peu plus javaScript

// an object that represent filtering system
let filter = {
    minAmount: document.getElementById('minamount'),
    maxAmount: document.getElementById('maxamount'),
    btnRange: document.getElementById('btn-filter'),
    sizeList: Array.from(document.querySelectorAll('.sidebar__sizes input[type=checkbox]')),
    colorList: Array.from(document.querySelectorAll('.sidebar__color input[type=checkbox]')),
    pagination: Array.from(document.querySelectorAll('.pagination__option a')),
    categoryItems: (category) => {
        items = Array.from(document.querySelectorAll(`.${category} a`))
        return items
    }
}


//  using an async function to make what need do done ! -->Yves
async function loadData(url) {
    let response = await fetch(url)
    // console.log(response.status)
    return await response.json()
}

function setItem(item, categories) {
    //  delta_days represent la duree en jour entre deux date
    let category = '';
    let label = '';
    let today = new Date();
    let created_at = new Date(item.created_at);

    let delta_days = Math.round((today.getTime() - created_at.getTime()) /
        (1000 * 60 * 60 * 24)) //(1000 * 60 * 60 * 24)>millisecond in a day

    for (i in categories) {
        if (item.category == categories[i].id) {
            category = categories[i].name// var is forbiden but ueful here to remove the last character
            var cat = categories[i].name.slice(0, -1)
        }
    }
    let url = `http://127.0.0.1:8000/product/${cat}Product/${item.id}/`;
    // utilisation de condition ternaire pour se jouer les pro
    let price = item.sale_price ? `$$${item.sale_price} <span>${item.price} </span>` : `$ ${item.price}`;

    if (!item.red_quantity && !item.grey_quantity && !item.black_quantity && !item.quantity) {
        label = '<div class="label stockout">out of stock</div>';
    } else if ((delta_days < 3 && self.sale_price) || (delta_days < 3)) {
        label = '<div class="label new">New</div>';
    } else if (self.sale_price) {
        label = '<div class="label sale">Sale</div>';
    } else {
        label = '';
    }

    return {
        url,
        price,
        label

    }
}


// sert à remplir les balises produits de données précises
function pushData(array = [], categories) {
    // The listElement will contain all Html Element 
    let listElement = []
    let bodyToFill = document.getElementsByClassName('row boxies');
    // 
    array.forEach((item, i) => {
        let element =
            `
                    <div class="col-lg-4 col-md-6">
                        <div class="product__item ">
                            <div class="product__item__pic set-bg box" style="background-image: url(${item.thumnail});" data-setbg="${item.thumnail}">
                                ${setItem(item, categories).label}
                                <ul class="product__hover">
                                    <li><a href="${item.thumnail}" class="image-popup"><span
                                                class="arrow_expand"></span></a></li>
                                    <li><a href="#"><span class="icon_heart_alt"></span></a></li>
                                    <li><a href="#"><span class="icon_bag_alt"></span></a></li>
                                </ul>
                            </div>
                            <div class="product__item__text">
                                <h6><a href="${setItem(item, categories).url}">${item.name}$</a></h6>
                                <div class="rating">
                                    <i class="fa fa-star"></i>
                                    <i class="fa fa-star"></i>
                                    <i class="fa fa-star"></i>
                                    <i class="fa fa-star"></i>
                                    <i class="fa fa-star"></i>
                                </div>
                                <div class="product__price">
                                ${setItem(item, categories).price}
                                </span></div>
                            </div>
                        </div>
                    </div>
        `
        listElement.push(element)
    })
    // // filling The body with data
    let body = ''
    listElement.forEach((item, i) => {
        body += item
    })
    bodyToFill[0].innerHTML = body;
}

function eachInData(data) {
    // remove repeat data
    for (x in data) {
        for (y in data) {
            if (x != y && data[y] == data[x]) {
                delete data[y]
            }
        }
    }
    return data
}


const main = async function () {
    const clothes = await loadData('http://127.0.0.1:8000/api/ClotheProduct-list/');
    const accessories = await loadData('http://127.0.0.1:8000/api/AccessorieProduct-list/');
    const cosmetics = await loadData('http://127.0.0.1:8000/api/CosmeticProduct-list/');
    const categories = await loadData('http://127.0.0.1:8000/api/Category-list/');
    
    // bon le checkbox a besoin de factorisation, mais bon
    // ça marche
    function checkbox(e) {
        let data = []
        // console.log(e)
        for (x in filter.sizeList) {
            if (filter.sizeList[x].checked || filter.colorList[x].checked) {
                for (y in clothes) {
                    let black = clothes[y].black_quantity > 0 ? 'black' : '';
                    let red = clothes[y].red_quantity > 0 ? 'reds' : '';
                    let grey = clothes[y].grey_quantity > 0 ? 'greys' : '';
                    if (clothes[y].size == filter.sizeList[x].id ||
                        black == filter.colorList[x].id ||
                        red == filter.colorList[x].id ||
                        grey == filter.colorList[x].id) {
                        data.push(clothes[y])
                    }
                }
            } if (filter.colorList[x].checked) {
                for (y in accessories) {
                    let black = accessories[y].black_quantity > 0 ? 'black' : '';
                    let red = accessories[y].red_quantity > 0 ? 'reds' : '';
                    let grey = accessories[y].grey_quantity > 0 ? 'greys' : '';
                    console.log(accessories[y])
                    if (black == filter.colorList[x].id || red == filter.colorList[x].id ||
                        grey == filter.colorList[x].id) {
                        data.push(accessories[y])
                        console.log('puting the data....')
                    }
                }
            }
        }
        let filtered_data = eachInData(data)
        pushData(filtered_data, categories)
    }


    function categoryFilter(e) {
        let tagName = e.path[2].className
        let click = e.target.textContent
        // tagName --> women(Female) or men(Male) or accessories or cosmestics...
        let data = []
        // console.log(e.path[2])
        let clothe = '';
        switch (tagName) {
            case 'kid':
                clothe = 'kid'
                break;
            case 'women':
                clothe = 'Female'
                break;
            case 'men':
                clothe = 'Male'
                break;
        }

        if (tagName == 'accessories') {
            for (x in accessories) {
                if (accessories[x].product_options == click) {
                    data.push(accessories[x])
                }
            }
            
        } else if (tagName == 'cosmetics') {
            for (x in cosmetics) {
                if (cosmetics[x].product_options == click) {
                    data.push(cosmetics[x])
                }
            }
        } else {
            // debugger
            // switch (tagName) {
            //     case 'women':
            //         tagName = 'Female'
            //         break;
            //     case 'men':
            //         tagName = 'Male'
            //         break;
            //     case 'kid':
            //         break;
            // }
            for (x in clothes) {
                if (clothes[x].gender == clothe
                    && clothes[x].product_options == click ) {
                        data.push(clothes[x])
                        console.log('female or male')
                    
                } else {
                    for (x in clothes) {
                        if (clothes[x].for_kid == 'Yes'
                            && clothes[x].product_options == click) {
                            console.log('kid is true')
                            data.push(clothes[x])
                        }
                    }
                }
            }
        }
        // pushing data on the DOM
        let filtered_data = eachInData(data)
        pushData(filtered_data, categories)

    }


    function shopPrice() {
        let data = []
        function forPrice(array) {
            // fait le traval de filterby price
            array.forEach(item => {
                let price = item.sale_price ? item.sale_price : item.price
                if (filter.minAmount.value.replace('$', '') <= price && price <= filter.maxAmount.value.replace('$', '')) {
                    data.push(item)
                }
            })
        }
        forPrice(clothes)
        forPrice(cosmetics)
        forPrice(accessories)

        // pushing data on the DOM
        let filtered_data = eachInData(data)
        pushData(filtered_data, categories)  
    }

    // addinng event for eac item the filter
    filter.categoryItems('women').forEach(item => {
       item.addEventListener('click', categoryFilter)
    })

    filter.categoryItems('accessories').forEach(item => {
        item.addEventListener('click', categoryFilter)
    })
    
    filter.categoryItems('kid').forEach(item => {
        item.addEventListener('click', categoryFilter)
    })

    filter.categoryItems('men').forEach(item => {
        item.addEventListener('click', categoryFilter)
    })

    filter.categoryItems('cosmetics').forEach(item => {
        item.addEventListener('click', categoryFilter)
    })
    // Adding event to the checkbox Form
    filter.sizeList.forEach((item, i) => {
        item.addEventListener('change', checkbox);

    })
    filter.colorList.forEach((item => {
        item.addEventListener('change', checkbox);
    }))

    // shop by price
    filter.btnRange.addEventListener('click', shopPrice)

}()


















