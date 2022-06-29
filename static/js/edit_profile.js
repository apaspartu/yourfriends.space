let modal_change_photo_open = false;

let change_photo_button = document.querySelector('.change-photo'); 
let modal_change_photo = document.querySelector('.modal-change-photo');
let change_photo_back = document.querySelector('.modal-change-photo .mback');
let close_modal = document.querySelector('#close-modal');

change_photo_button.addEventListener('click', function() {
    modal_change_photo.classList.toggle('open');
});

change_photo_back.addEventListener('click', function() {
    modal_change_photo.classList.toggle('open');
});

close_modal.addEventListener('click', function() {
    modal_change_photo.classList.toggle('open');
});