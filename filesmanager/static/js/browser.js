window.onload = function () {
    // Upload btn
    var btn_upload = document.getElementById("upload-btn");
    var btn_input_upload = document.getElementById("upload-input");
    var form_upload = document.getElementById("upload-form");

    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the button that opens the modal and the download link
    var btn_list = document.getElementsByClassName("table-btn-show-link");
    var url_list = document.getElementsByClassName("download-url");

    // Get the message paragraph
    var msg = document.getElementById("modal-content-url");
    var btn_copy = document.getElementById("modal-content-url-copy");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal
    for(var i = 0; i < btn_list.length; i++) {
        btn = btn_list[i]
        btn.id = i
        btn.onclick = function () {
            btn_copy.textContent = "Copy";
            modal.style.display = "block";
            url = url_list[this.id].href;
            /* Copy the text inside the text field */
            msg.textContent = url;
            btn_copy.onclick = function () {
                navigator.clipboard.writeText(url);
                btn_copy.textContent = "Copied!";
            }
        }
    
    }
    
    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    btn_upload.onclick = function () {
        btn_input_upload.click();
    }

    btn_input_upload.onchange = function () {
        form_upload.submit();
        alert("Uploaded!");
    }
}