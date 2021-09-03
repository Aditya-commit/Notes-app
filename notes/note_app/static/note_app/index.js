function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

window.addEventListener('load', function() {

    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/display/', true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    xhr.onload = function(response) {
        let jsondata = this.responseText;

        if (jsondata != 'no data available') {

            data = JSON.parse(jsondata);
            let html = '';
            for (let i = 0; i < data['title'].length; i++) {
                html += `<div class="noteCard my-2 mx-2 card" style="width: 18rem;">
                        <div class="card-body">
                            <h5 class="card-title">Note ${i+1}</h5>
                            <h3>${data['title'][i]}</h3>
                            <p class="card-text">${data['text'][i]}</p>
                            <button>
                                <a href="delete/${data['id'][i]}" class='delete'>Delete</a>
                            </button>
                        </div>
                    </div>`;
            }

            document.getElementById('notes').innerHTML = html
        } else {
            document.getElementById('notes').innerHTML = `<h3>Please enter something to display on screen</h3>`
        }
    }
    xhr.send();
})

// Adding notes on click

document.getElementById('addBtn').addEventListener('click', function() {
    let title = document.getElementById('addTitle');
    let text = document.getElementById('addTxt');

    if (title.value == "" && text.value == "") {
        alert("Can't add an empty note");
    } else {
        let data = {
            'title': title.value,
            'text': text.value
        }

        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/display/', true);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.onload = function(response) {

            responsecode=JSON.parse(this.responseText)

            if (responsecode['status'] == 200) {
                document.getElementById('notes').innerHTML += `<div class="noteCard my-2 mx-2 card" style="width: 18rem;">
                                                                    <div class="card-body">
                                                                        <h5 class="card-title">Note ${responsecode['noteno']}</h5>
                                                                        <h3>${title.value}</h3>
                                                                        <p class="card-text">${text.value}</p>
                                                                        <button>
                                                                            <a href="delete/${responsecode['id']}" class='delete'>Delete</a>
                                                                        </button>   
                                                                    </div>
                                                                </div>`;

                title.value="";
                text.value="";
            }


        }
        xhr.send(JSON.stringify(data))
    }
})