import PhotoSwipeLightbox from 'https://cdn.jsdelivr.net/npm/photoswipe@5.4.4/dist/photoswipe-lightbox.esm.min.js';
import PhotoSwipe from 'https://cdn.jsdelivr.net/npm/photoswipe@5.4.4/dist/photoswipe.esm.min.js';

const lightbox = new PhotoSwipeLightbox({
  gallery: '.photo-gallery-container-images',
  children: 'a',
  pswpModule: PhotoSwipe
});

lightbox.init();
