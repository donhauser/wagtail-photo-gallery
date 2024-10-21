
$(document).ready(function () {
    
    let photoSwipe = document.querySelectorAll('.pswp')[0];
    
    let images = [];
    
    $('.photo-gallery-container-images img').each((index, img) => {
        var data = {
            src: $(img).data('image-src'),
            w: $(img).data('image-width'),
            h: $(img).data('image-height')
        }
        images.push(data)
    }).each((index, img) => {
        $(img).click(() => {
            var options = {
                index : index
            };

            // Initializes and opens PhotoSwipe
            var gallery = new PhotoSwipe(photoSwipe, PhotoSwipeUI_Default, images, options);
            gallery.init();
        });
    });
});
