<script>
  import navigationState from '$lib/navigationState';
  import loadStore from '$lib/loadstore';
</script>

{#if $navigationState == 'loading'}
  <style>
    #loading-opaque {
      height: 100%;
      opacity: 0.9 !important;
      background-color: #1d1e23 !important;
    }

    :global(main, html, body) {
      display: block !important;
      background-color: #1d1e23 !important;
      width: 100% !important;
      height: 100% !important;
      margin: 2px !important;
      padding: 0px !important;
    }

    .only-on-loading {
      display: block !important;
    }

    /* https://codepen.io/WebSonata/pen/bRaONB */
    #preloader {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      opacity: 1 !important;
      z-index: 9999;
    }

    .loader-on {
      display: block;
      position: relative;
      left: 50%;
      top: 50%;
      width: 200px;
      height: 150px;
      margin: -75px 0 0 -75px;
      border-radius: 50%;
      overflow: visible !important;
      z-index: 10000;
      font-size: 18px;
      font-weight: bold;
    }

    #loader {
      display: block;
      position: relative;
      left: 50%;
      top: 50%;
      width: 150px;
      height: 150px;
      margin: -75px 0 0 -75px;
      border-radius: 50%;
      border: 3px solid transparent;
      border-top-color: #9370db;
      -webkit-animation: spin 2s linear infinite;
      animation: spin 2s linear infinite;
      z-index: 9999;
    }
    #loader:before {
      content: '';
      position: absolute;
      top: 5px;
      left: 5px;
      right: 5px;
      bottom: 5px;
      border-radius: 50%;
      border: 3px solid transparent;
      border-top-color: #ba55d3;
      -webkit-animation: spin 3s linear infinite;
      animation: spin 3s linear infinite;
    }
    #loader:after {
      content: '';
      position: absolute;
      top: 15px;
      left: 15px;
      right: 15px;
      bottom: 15px;
      border-radius: 50%;
      border: 3px solid transparent;
      border-top-color: #ff00ff;
      -webkit-animation: spin 1.5s linear infinite;
      animation: spin 1.5s linear infinite;
    }
    @-webkit-keyframes spin {
      0% {
        -webkit-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        transform: rotate(0deg);
      }
      100% {
        -webkit-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        transform: rotate(360deg);
      }
    }
    @keyframes spin {
      0% {
        -webkit-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        transform: rotate(0deg);
      }
      100% {
        -webkit-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        transform: rotate(360deg);
      }
    }
  </style>
{/if}

<div id="loading-opaque">
  <div id="preloader">
    <div id="loader" />
    <div class="loader-on only-on-loading" style="display: none">
      <h1 style="opacity: 1 !important;">{$loadStore || 'Loading...'}</h1>
    </div>
  </div>
  <slot />
</div>
