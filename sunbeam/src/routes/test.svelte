<script lang="ts">
  import Button from '$lib/base/Button.svelte';
  import { subNotifs } from '$lib/request';
  import { session } from '$app/stores';
  let token = $session.session.token;
  let id = '';

  if (token) {
    id = $session.session.user.id;
  }
</script>

<!--Put all allowed Tailwind CSS classes here so they are built-->
<h1 class="text-3xl font-bold underline">Hello world!</h1>
<button
  class="duration-75 transform hover:scale-125 transition ease-linear bg-teal-400 px-6 py-2 m-4 inline"
  >75</button
>
<button
  class="transition-none duration-500 transform px-6 py-2 m-4 inline
               bg-teal-400 hover:bg-indigo-400
               border-2 border-red-500 hover:border-yellow-500
               hover:text-white
               hover:opacity-50
               hover:shadow-md
               hover:scale-125">None</button
>

<button
  class="transition-all duration-500 transform px-6 py-2 m-4 inline
               bg-teal-400 hover:bg-indigo-400
               border-2 border-red-500 hover:border-yellow-500
               hover:text-white
               hover:opacity-50
               hover:shadow-md
               hover:scale-125">All</button
>

<button
  class="transition duration-500 transform px-6 py-2 m-4 inline
               bg-teal-400 hover:bg-indigo-400
               border-2 border-red-500 hover:border-yellow-500
               hover:text-white
               hover:opacity-50
               hover:shadow-md
               hover:scale-125">Default</button
>

<button
  class="transition-colors duration-500 transform px-6 py-2 m-4 inline
               bg-teal-400 hover:bg-indigo-400
               border-2 border-red-500 hover:border-yellow-500
               hover:text-white
               hover:opacity-50
               hover:shadow-md
               hover:scale-125">Colors</button
>

<button
  class="transition-opacity duration-500 transform px-6 py-2 m-4 inline
               bg-teal-400 hover:bg-indigo-400
               border-2 border-red-500 hover:border-yellow-500
               hover:text-white
               hover:opacity-50
               hover:shadow-md
               hover:scale-125">Opacity</button
>

<button
  class="transition-shadow duration-500 transform px-6 py-2 m-4 inline
               bg-teal-400 hover:bg-indigo-400
               border-2 border-red-500 hover:border-yellow-500
               hover:text-white
               hover:opacity-50
               hover:shadow-md
               hover:scale-125">Shadow</button
>

<button
  class="transition-transform duration-500 transform px-6 py-2 m-4 inline
               bg-teal-400 hover:bg-indigo-400
               border-2 border-red-500 hover:border-yellow-500
               hover:text-white
               hover:opacity-50
               hover:shadow-md
               hover:scale-125">Transform</button
>

<Button class="vr-test" onclick={() => subNotifs(id, token)}>Test VR</Button>
<div class="flex items-center" />

<!--Force add textarea styles-->
<textarea class="textarea" />

<div
  class="relative overflow-hidden bg-no-repeat bg-cover max-w-xs"
  data-mdb-ripple="true"
  data-mdb-ripple-color="light"
>
  <img src="https://mdbcdn.b-cdn.net/img/new/fluid/city/113.webp" class="max-w-xs" alt="Louvre" />
  <a href="#!">
    <div
      class="absolute top-0 right-0 bottom-0 left-0 w-full h-full overflow-hidden bg-fixed opacity-0 hover:opacity-100 transition duration-300 ease-in-out"
      style="background-color: rgba(251, 251, 251, 0.2)"
    />
  </a>
</div>
<img src="https://mdbootstrap.com/img/new/slides/041.jpg" class="max-w-full h-auto" alt="..." />

<div class="flex justify-center">
  <div class="mb-3 xl:w-96">
    <label for="exampleFormControlTextarea1" class="form-label inline-block mb-2 text-gray-700"
      >Example textarea</label
    >
    <textarea
      class="
          form-control
          block
          w-full
          px-3
          py-1.5
          text-base
          font-normal
          text-gray-700
          bg-white bg-clip-padding
          border border-solid border-gray-300
          rounded
          transition
          ease-in-out
          m-0
          focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
        "
      id="exampleFormControlTextarea1"
      rows="3"
      placeholder="Your message"
    />
  </div>
</div>

<div class="block p-6 rounded-lg shadow-lg bg-white max-w-sm">
  <form>
    <div class="form-group mb-6">
      <label for="exampleInputEmail1" class="form-label inline-block mb-2 text-gray-700"
        >Email address</label
      >
      <input
        type="email"
        class="form-control
          block
          w-full
          px-3
          py-1.5
          text-base
          font-normal
          text-gray-700
          bg-white bg-clip-padding
          border border-solid border-gray-300
          rounded
          transition
          ease-in-out
          m-0
          focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
        placeholder="Enter email"
      />
      <small id="emailHelp" class="block mt-1 text-xs text-gray-600"
        >We'll never share your email with anyone else.</small
      >
    </div>
    <div class="form-group mb-6">
      <label for="exampleInputPassword1" class="form-label inline-block mb-2 text-gray-700"
        >Password</label
      >
      <input
        type="password"
        class="form-control block
          w-full
          px-3
          py-1.5
          text-base
          font-normal
          text-gray-700
          bg-white bg-clip-padding
          border border-solid border-gray-300
          rounded
          transition
          ease-in-out
          m-0
          focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
        id="exampleInputPassword1"
        placeholder="Password"
      />
    </div>
    <div class="form-group form-check mb-6">
      <input
        type="checkbox"
        class="form-check-input appearance-none h-4 w-4 border border-gray-300 rounded-sm bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer"
        id="exampleCheck1"
      />
      <label class="form-check-label inline-block text-gray-800" for="exampleCheck1"
        >Check me out</label
      >
    </div>
    <button
      type="submit"
      class="
        px-6
        py-2.5
        bg-blue-600
        text-white
        font-medium
        text-xs
        leading-tight
        uppercase
        rounded
        shadow-md
        hover:bg-blue-700 hover:shadow-lg
        focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0
        active:bg-blue-800 active:shadow-lg
        transition
        duration-150
        ease-in-out">Submit</button
    >
  </form>
</div>

<img
  src="https://google.com"
  on:error={function () {
    this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
  }}
  alt="test"
  width="1000px;"
/>
