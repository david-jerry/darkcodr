(self.webpackChunkpython_webpack_boilerplate=self.webpackChunkpython_webpack_boilerplate||[]).push([[143],{2044:function(e,n,t){"use strict";t(3462);var i=t(5450),o=t.n(i),s=t(4306),r=t(2051),a=t(9669),l=t.n(a);l().defaults.xsrfHeaderName="X-CSRFTOKEN",l().defaults.xsrfCookieName="csrftoken",l().defaults.timeout=15e3;var c=l(),d=t(3631);t(1786),window.document.addEventListener("DOMContentLoaded",(function(){window.console.log("dom ready 1")}));const p=(0,d.qY)(),{APPLICATION_SERVER_KEY:w,CREATE_WP_SUBSCRIPTION:u,SEND_NOTIFICATION:g}=window.WEB_PUSH_CFG,f=window.SW_URL;function h(e){for(var n=(e+"=".repeat((4-e.length%4)%4)).replace(/\-/g,"+").replace(/_/g,"/"),t=window.atob(n),i=new Uint8Array(t.length),o=0;o<t.length;++o)i[o]=t.charCodeAt(o);return i}function P(e){const n=document.getElementById("triggerNotificationButton");n.classList.toggle("hidden",!1),n.addEventListener("click",(()=>{const n=e.toJSON().endpoint.split("/"),t={registration_id:n[n.length-1]};c.post(g,t).then((function(e){return e})).catch((function(e){console.log(e)}))}))}window.htmx=o(),"serviceWorker"in navigator&&window.addEventListener("load",(()=>{navigator.serviceWorker.register(f).then((e=>{console.log("SW registration succeeded:",e),navigator.serviceWorker.ready.then((function(e){console.log("[SW] is active:",e.active),e.pushManager.getSubscription().then((function(n){if(n){P(n);const e=n.toJSON();console.log(`already has subscription ${JSON.stringify(e)}`)}else!function(e){const n={userVisibleOnly:!0,applicationServerKey:h(w)};e.pushManager.subscribe(n).then((function(e){console.log(e.endpoint),function(e,n){const t=n.toJSON(),i=t.endpoint.split("/"),o=i[i.length-1],s={browser:p.name.toUpperCase(),p256dh:t.keys.p256dh,auth:t.keys.auth,name:"notification-subscription",registration_id:o,active:!0};c.post(u,s).then((function(e){console.log(e)})).catch((function(e){console.log(e)}))}(0,e),P(e)}),(function(e){console.log(e)}))}(e)}))}))})).catch((e=>{console.log("SW registration failed: ",e)}))})),window.Alpine=s.Z,s.Z.data("SwiperComponent",(function(){return{swiper:{},initSwiper(){let e;return e=new r.ZP(this.$refs.container,{autoplay:{delay:5e3,disableOnInteraction:!1},loop:!0,speed:1e3,spaceBetween:0,breakpoints:{320:{slidesPerView:1,spaceBetween:20},480:{slidesPerView:2,spaceBetween:30},640:{slidesPerView:3,spaceBetween:40},768:{slidesPerView:4,spaceBetween:30},1524:{slidesPerView:5,spaceBetween:30}}}),this.swiper=e},prevSlide(){let e;e=new r.ZP(this.$refs.container,{autoplay:{delay:5e3,disableOnInteraction:!1},loop:!0,speed:1e3,spaceBetween:0,breakpoints:{320:{slidesPerView:1,spaceBetween:20},480:{slidesPerView:2,spaceBetween:30},640:{slidesPerView:3,spaceBetween:40},768:{slidesPerView:4,spaceBetween:30},1524:{slidesPerView:5,spaceBetween:30}}}),e.slidePrev()},nextSlide(){let e;e=new r.ZP(this.$refs.container,{autoplay:{delay:5e3,disableOnInteraction:!1},loop:!0,speed:1e3,spaceBetween:0,breakpoints:{320:{slidesPerView:1,spaceBetween:20},480:{slidesPerView:2,spaceBetween:30},640:{slidesPerView:3,spaceBetween:40},768:{slidesPerView:4,spaceBetween:30},1524:{slidesPerView:5,spaceBetween:30}}}),e.slideNext()}}})),s.Z.start(),window.Swiper=r.ZP;const b=document.getElementById("installButton");window.addEventListener("beforeinstallprompt",(e=>{console.log("👍","beforeinstallprompt",e),window.deferredPrompt=e,b.classList.toggle("hidden",!1)})),b.addEventListener("click",(()=>{console.log("👍","butInstall-clicked");const e=window.deferredPrompt;e&&(e.prompt(),e.userChoice.then((e=>{console.log("👍","userChoice",e),window.deferredPrompt=null,b.classList.toggle("hidden",!0)})))}))},1786:function(){window.console.log("sidebar is loaded")}},function(e){e.O(0,[259],(function(){return 2044,e(e.s=2044)})),e.O()}]);
//# sourceMappingURL=app.38eadbaf.js.map