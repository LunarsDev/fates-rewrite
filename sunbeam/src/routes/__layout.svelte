<script lang="ts">
  import Header from '$lib/header/Header.svelte';

  import navigationState from '$lib/navigationState';
  import inputstore from '$lib/inputstore';
  import alertStore from '$lib/alertstore';
  import PageLoader from '$lib/base/PageLoader.svelte';

  import { browser } from '$app/env';
  import loadstore from '$lib/loadstore';
  import alertstore from '$lib/alertstore';
  import { errorStore } from '$lib/alertstore';
  import { apiUrl, lynxUrl } from '$lib/config';
  import * as logger from '$lib/logger';
  import menustore from '$lib/menustore';

  import { navigating, session } from '$app/stores';

  import './../css/tailwind.css';
  import { enums } from '$lib/enums/enums';
  import Alert from '$lib/base/Alert.svelte';

  function llhandler() {
    logger.info('Nav', 'Called lazy load handler');
    var lazyloadImages;

    if ('IntersectionObserver' in window) {
      lazyloadImages = document.querySelectorAll('.lazy');
      if (lazyloadImages.length < 1) {
        logger.info('Nav', 'No lazy load images found');
        return;
      }
      var imageObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var image = entry.target;
            image.classList.remove('lazy');
            imageObserver.unobserve(image);
          }
        });
      });

      lazyloadImages.forEach(function (image) {
        imageObserver.observe(image);
      });
    } else {
      var lazyloadThrottleTimeout;
      lazyloadImages = document.querySelectorAll('.lazy');

      function lazyload() {
        if (lazyloadThrottleTimeout) {
          clearTimeout(lazyloadThrottleTimeout);
        }

        lazyloadThrottleTimeout = setTimeout(function () {
          var scrollTop = window.pageYOffset;
          lazyloadImages.forEach(function (img) {
            if (img.offsetTop < window.innerHeight + scrollTop) {
              img.src = img.dataset.src;
              img.classList.remove('lazy');
            }
          });
          if (lazyloadImages.length == 0) {
            document.removeEventListener('scroll', lazyload);
            window.removeEventListener('resize', lazyload);
            window.removeEventListener('orientationChange', lazyload);
          }
        }, 20);
      }

      document.addEventListener('scroll', lazyload);
      window.addEventListener('resize', lazyload);
      window.addEventListener('orientationChange', lazyload);
    }
  }

  if (browser) {
    function docReady(fn) {
      // see if DOM is already available
      if (document.readyState === 'complete' || document.readyState === 'interactive') {
        // call on next available tick
        setTimeout(fn, 1);
      } else {
        document.addEventListener('DOMContentLoaded', fn);
      }
    }

    docReady(llhandler);
	window.llhandler = llhandler
  }

  $: {
    if ($navigating) {
      logger.info('Nav', `isNavigating: ${$navigating.from} -> ${$navigating.to}`);
      if ($navigating.to.host != $navigating.from.host) {
        logger.info('Nav', 'navigating to different host');
        $navigationState = 'loaded';
      } else {
        $inputstore = [];
        $loadstore = 'Loading...';
        $navigationState = 'loading';
      }
    }
    if (!$navigating) {
      $navigationState = 'loaded';
      if (browser) {
        llhandler();
      }
      $menustore.open = '';
    }
  }

  // Insert alertstore into window
  if (browser) {
    window.user = () => {
      if ($session.session.token) {
        return {
          id: $session.session.user.id,
          token: $session.session.token,
          apiUrl: apiUrl,
          lynxUrl: lynxUrl
        };
      } else {
        return null;
      }
    };

    // Keep this
    window.alert = (opt) => {
      if (!opt) {
        opt = '';
      }

      if (typeof opt !== 'object') {
        // In this special case, make a new object with Alert type, this is for backward compatibility with window.alert()
        opt = {
          title: 'Info',
          id: 'string-alert',
          show: true,
          message: `${opt}` || '[empty alert]',
          type: enums.AlertType.Alert,
          buttons: []
        };
      }

      if (!opt.show) {
        opt.show = true;
      }
      if (!opt.title) {
        logger.error('No title in alertstore');
        return;
      }
      if (!opt.message) {
        logger.error('No message in alertstore');
        return;
      }

      // Backwards compatibility
      if (opt.input) {
        opt.input.type = enums.AlertInputType.Text;
        opt.submit = opt.input.function || opt.submit;
        opt.inputs = [opt.input];
      } else if (opt.inputs) {
        if (opt.inputs.length > 0 && opt.inputs[0].function) {
          opt.submit = opt.inputs[0].function;
        }
      }

      if (opt.validate && opt.inputs && opt.inputs.length > 0) {
        opt.inputs[0].validate = opt.validate;
      }

      if (!opt.id) {
        opt.id = 'alert-generic';
      }

      if (!opt.type) {
        opt.type = enums.AlertType.Alert;
      }

      if (!opt.buttons) {
        opt.buttons = [];
      }

      $alertstore = opt;

      $errorStore = false;

      $navigationState = 'loaded'; // An alert = page loaded
    };

    if (window.location.pathname === '/alert/test') {
      alert({
        title: 'Test Alert',
        message: 'This is a Test Alert!',
        id: 1030404,
        type: enums.AlertType.Alert,
        inputs: [
          {
            id: 'mew3',
            label: 'Test Input',
            required: true,
            placeholder: `Enter some random stuff here and click Submit!`,
            multiline: false, // Set to "true", for Multi-line input
            type: enums.AlertInputType.Text,
            function: (value) => {
              logger.info('AlertTest', value.indexMap);
              alert({
                title: 'Test Alert',
                message: `Textbox 1: "${value.toLines() || 'nothing'}"<br>Textbox 2: "${
                  value.toLines(1) || 'nothing'
                }"`,
                id: 1030404,
                type: enums.AlertType.Info,
                close: () => {
                  alert({
                    title: 'Test Alert',
                    message: "You've closed the alert!",
                    id: 1030404,
                    type: enums.AlertType.Success
                  });
                }
              });
            }
          },
          {
            id: 'mew2',
            label: 'Test Input 2',
            required: false,
            placeholder: `Enter some random stuff here and click Submit!`,
            multiline: false, // Set to "true", for Multi-line input
            type: enums.AlertInputType.Text
          },
          {
            id: 'mew27',
            label: 'Test Input 3',
            required: true,
            placeholder: `Upload some random ass files please`,
            type: enums.AlertInputType.File,
            multipleFiles: true
          }
        ]
      });
    }
  }
</script>

<svelte:head>
  <meta
    name="keywords"
    content="discord bot, discord bot list, fateslist, fates list, bot list, discord list, list of bots, list of bot, bot, discord bots, fateslist bots, fates list"
  />
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</svelte:head>

<Header />
<main style="background-color: #1D1E23 !important;">
  <PageLoader>
    <slot />
  </PageLoader>
</main>

{#if $alertStore}
  <Alert
    bind:showError={$errorStore}
    close={$alertStore.close}
    inputs={$alertStore.inputs || []}
    buttons={$alertStore.buttons || []}
    show={$alertStore.show}
    supabase={null}
    submit={$alertStore.submit}
    title={$alertStore.title}
    icon={$alertStore.icon}
    type={$alertStore.type}
    id={$alertStore.id}>{@html $alertStore.message.replaceAll('\n', '<br/>')}</Alert
  >
{/if}

<style lang="scss" global>
  @import './../css/base.scss';
  @import './../css/tw-patch.scss';
  .footer {
    margin-left: 3px;
  }
  pre {
    color: white !important;
  }
</style>
