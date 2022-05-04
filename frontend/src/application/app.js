// This is the scss entry file
import "../styles/tailwindcss.css";
import htmx from "htmx.org/dist/htmx";
import Alpine from "alpinejs";
import Swiper from "swiper";

import '../components/sidebar';

window.htmx = htmx;

import SwiperComponent from "../components/Swiper";


window.document.addEventListener("DOMContentLoaded", function () {
    window.console.log("dom ready 1");
});


// Alpine JS Scripts
window.Alpine = Alpine;
Alpine.data('SwiperComponent', SwiperComponent);
Alpine.start();

window.Swiper = Swiper;

if (process.env.NODE_ENV === "development") {
    // enable logging for htmx in development server
    window.htmx.logAll();
}
