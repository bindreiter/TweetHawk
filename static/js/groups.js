// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}



document.addEventListener('DOMContentLoaded', function () {
  var checkbox = document.querySelector('input[type="checkbox"]');
  console.log('Send Request to start monitor mode');

  checkbox.addEventListener('change', function () {
    if (checkbox.checked) {
      // do this
      console.log('Send Request to start monitor mode');
      const Http = new XMLHttpRequest();
      Http.open("POST", "auto");
      Http.send();  
    } else {
      // do that
      console.log('Send Request to stop monitor mode');
      const Http = new XMLHttpRequest();
      Http.open("POST", "auto");
      Http.send();   
      
    }
  });
});










