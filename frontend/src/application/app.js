import '../styles/tailwindcss.css';
import htmx from 'htmx.org/dist/htmx';
import Alpine from 'alpinejs';
import Swiper from 'swiper';
import axios from '../components/axiosFactory';
import { detect } from 'detect-browser';

import '../components/sidebar';
import SwiperComponent from '../components/Swiper';

window.document.addEventListener('DOMContentLoaded', function () {
  window.console.log('dom ready 1');
});

const browser = detect();
const {
  APPLICATION_SERVER_KEY,
  CREATE_WP_SUBSCRIPTION,
  SEND_NOTIFICATION
} = window.WEB_PUSH_CFG;
const sw = window.SW_URL;
window.htmx = htmx;

function urlBase64ToUint8Array (base64String) {
  // https://gist.github.com/Klerith/80abd742d726dd587f4bd5d6a0ab26b6#file-urlbase64touint8array-js
  var padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  var base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');

  var rawData = window.atob(base64);
  var outputArray = new Uint8Array(rawData.length);

  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function saveSubscribeObj (active, subscription) {
  // sends the subscription info to backend server
  const subscriptionJson = subscription.toJSON();
  const endpointParts = subscriptionJson.endpoint.split('/');
  const registrationId = endpointParts[endpointParts.length - 1];
  const data = {
    browser: browser.name.toUpperCase(),
    p256dh: subscriptionJson.keys.p256dh,
    auth: subscriptionJson.keys.auth,
    name: 'notification-subscription',
    registration_id: registrationId,
    active: active
  };

  axios
    .post(CREATE_WP_SUBSCRIPTION, data)
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}

function subscribe (registration) {
  const options = {
    userVisibleOnly: true, // required by chrome
    applicationServerKey: urlBase64ToUint8Array(APPLICATION_SERVER_KEY)
  };

  registration.pushManager.subscribe(options).then(
    function (subscription) {
      console.log(subscription.endpoint);
      // The push subscription details needed by the application
      // server are now available, and can be sent to it using,
      // for example, an XMLHttpRequest.
      saveSubscribeObj(true, subscription);
      setupTriggerButton(subscription);
    },
    function (error) {
      // During development it often helps to log errors to the
      // console. In a production environment it might make sense to
      // also report information about errors back to the
      // application server.
      console.log(error);
    }
  );
}

function setupTriggerButton (subscription) {
  const triggerNotificationButton = document.getElementById(
    'triggerNotificationButton'
  );
  triggerNotificationButton.classList.toggle('hidden', false);

  triggerNotificationButton.addEventListener('click', () => {
    const subscriptionJson = subscription.toJSON();
    const endpointParts = subscriptionJson.endpoint.split('/');
    const registrationId = endpointParts[endpointParts.length - 1];
    const data = {
      registration_id: registrationId
    };

    axios
      .post(SEND_NOTIFICATION, data)
      .then(function (response) {
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
  });
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register(sw)
      .then(registration => {
        console.log('SW registration succeeded:', registration);
        navigator.serviceWorker.ready.then(function (registration) {
          console.log('[SW] is active:', registration.active);

          registration.pushManager
            .getSubscription()
            .then(function (subscription) {
              if (!subscription) {
                subscribe(registration);
              } else {
                setupTriggerButton(subscription);

                const subscriptionJson = subscription.toJSON();
                console.log(
                  `already has subscription ${JSON.stringify(subscriptionJson)}`
                );
              }
            });
        });
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Alpine JS Scripts
window.Alpine = Alpine;
Alpine.data('SwiperComponent', SwiperComponent);
Alpine.start();

window.Swiper = Swiper;

if (process.env.NODE_ENV === 'development') {
  // enable logging for htmx in development server
  window.htmx.logAll();
}


const installButton = document.getElementById('installButton');

window.addEventListener('beforeinstallprompt', event => {
  console.log('👍', 'beforeinstallprompt', event);
  // Stash the event so it can be triggered later.
  window.deferredPrompt = event;
  // Remove the 'hidden' class from the install button container
  installButton.classList.toggle('hidden', false);
});

installButton.addEventListener('click', () => {
  console.log('👍', 'butInstall-clicked');
  const promptEvent = window.deferredPrompt;
  if (!promptEvent) {
    // The deferred prompt isn't available.
    return;
  }
  promptEvent.prompt();
  promptEvent.userChoice.then(choice => {
    console.log('👍', 'userChoice', choice);
    // Reset the deferred prompt variable, since
    // prompt() can only be called once.
    window.deferredPrompt = null;
    // Hide the install button.
    installButton.classList.toggle('hidden', true);
  });
});
