// Get the modal
// let modal = document.getElementById("myModal");
// Get the button that opens the modal and 
// When the user clicks the button, open modal
// Fetch informations from api with id movie
// const comment = document.querySelectorAll("button");
// for (let i = 0; i < comment.length; i++) {
//     comment[i].addEventListener("click", function(e) {
//         e.preventDefault();
//         modal.style.display = "block";
//         console.log("ouverture du modal?")
//   })  
// }

// Get the <span> element that closes the modal and
// when the user clicks on <span> (x), close the modal
// let span = document.getElementsByClassName("close")[0];
// span.onclick = function() {
//   modal.style.display = "none";
// }
// When the user clicks anywhere outside of the modal, close it


let modal = document.getElementById("myModal");
const entete = document.getElementsByClassName("afficher");
const contenu = document.getElementsByClassName("contenu");
for (let i = 0; i < entete.length; i++) {
  entete[i].addEventListener("click", function (e){
    e.preventDefault();
    contenu[i].style.display = "block";
  });
  let span = document.getElementsByClassName("fermer");
  span[i].style.float = 'right';
  span[i].onclick = function() {
    contenu[i].style.display = "none";
  };
  contenu[i].onclick = function() {
    contenu[i].style.display = "none";
  };
};

let image_modal = document.getElementById("imageModal");
const show_image_modal = document.getElementsByClassName("show_image_modal");
const image = document.getElementsByClassName("image");
for (let i = 0; i < show_image_modal.length; i++) {
  console.log("click on show_image_modal ?");
  console.log(i);
  console.log(show_image_modal.length);
  show_image_modal[i].addEventListener("click", function (e){
    e.preventDefault();
    image[i].style.display = "block";
  });
  let close_image = document.getElementsByClassName("close_image");
  close_image[i].style.float = 'right'
  close_image[i].onclick = function() {
    image[i].style.display = "none";
  };
  image[i].onclick = function() {
    image[i].style.display = "none";
  };
};

// window[i].onclick = function() {
//   contenu[i].style.display = "none";
// }
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//     contenu.style.display = "none";
//   }
// };

