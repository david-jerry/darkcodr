import Swiper from "swiper";

export default function SwiperComponent() {
  return {
    swiper: {},

    initSwiper() {
      let swiper;
      swiper = new Swiper(this.$refs.container, {
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
        loop: true,
        speed: 1000,
        spaceBetween: 0,
        breakpoints: {
          320: { slidesPerView: 1, spaceBetween: 20 },
          480: { slidesPerView: 2, spaceBetween: 30 },
          640: { slidesPerView: 3, spaceBetween: 40 },
          768: { slidesPerView: 4, spaceBetween: 30 },
          1524: { slidesPerView: 5, spaceBetween: 30 },
        },
      });
      return this.swiper = swiper;
    },

    prevSlide() {
      let swiper;
      swiper = new Swiper(this.$refs.container, {
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
        loop: true,
        speed: 1000,
        spaceBetween: 0,
        breakpoints: {
          320: { slidesPerView: 1, spaceBetween: 20 },
          480: { slidesPerView: 2, spaceBetween: 30 },
          640: { slidesPerView: 3, spaceBetween: 40 },
          768: { slidesPerView: 4, spaceBetween: 30 },
          1524: { slidesPerView: 5, spaceBetween: 30 },
        },
      });
      swiper.slidePrev();
    },

    nextSlide() {
      let swiper;
      swiper = new Swiper(this.$refs.container, {
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
        loop: true,
        speed: 1000,
        spaceBetween: 0,
        breakpoints: {
          320: { slidesPerView: 1, spaceBetween: 20 },
          480: { slidesPerView: 2, spaceBetween: 30 },
          640: { slidesPerView: 3, spaceBetween: 40 },
          768: { slidesPerView: 4, spaceBetween: 30 },
          1524: { slidesPerView: 5, spaceBetween: 30 },
        },
      });
      swiper.slideNext();
    },
  };
}
