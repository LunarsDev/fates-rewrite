<script lang="ts">
  import { browser } from '$app/env';

  import { session } from '$app/stores';

  export let data: any;
  export let type: string;

  import Reviews from '$lib/base/Reviews.svelte';
  import { nextUrl } from '$lib/config';
  import { enums } from '$lib/enums/enums';
  import loadstore from '$lib/loadstore';
  import navigationState from '$lib/navigationState';
  import { parseState } from '$lib/request';
  import * as logger from '$lib/logger';

  let reviewPage = 1;
  let reviews: any = {};

  let userHasMovedReviewPage = false;

  async function getReviewPage(page: number) {
    if (page != 1) {
      $loadstore = 'Loading...';
      $navigationState = 'loading';
      userHasMovedReviewPage = true;
    }
    let targetType = enums.ReviewType.bot;
    if (type == 'server') {
      targetType = enums.ReviewType.server;
    }

    let url = `${nextUrl}/reviews/${data.user.id}?page=${page}&target_type=${targetType}`;

    if ($session.session.token) {
      url += `&user_id=${$session.session.user.id}`;
    }

    let res = await fetch(url);
    if (res.ok) {
      reviews = await res.json();
      reviewPage = page;
    } else if (userHasMovedReviewPage) {
      let data = await res.json();
      alert(data.reason);
    }
    $navigationState = 'loaded';
    setTimeout(setupInputs, 300);
  }
  if (browser) {
    getReviewPage(1);
  }
  let setupInputs = () => {
    let slider = document.querySelectorAll('.range-slider');
    // Update the current slider value (each time you drag the slider handle)
    for (let i = 0; i < slider.length; i++) {
      let outputId = slider[i].getAttribute('data-output');
      if (!outputId) {
        continue;
      }
      let el = document.getElementById(outputId);
      if (!el) {
        // Give time for dom load
        setTimeout(setupInputs, 300);
      }

      if (outputId == 'rating-desc-avg') {
        // Special case
        let state = parseState(slider[i].value);
        slider[i].innerHTML = el.innerHTML = state + ', ' + slider[i].value;
        continue;
      }

      el.innerHTML = 'Drag the slider to change your rating'; // Display the default slider value
      slider[i].oninput = function () {
        let output = document.getElementById(this.getAttribute('data-output'));
        logger.debug('ReviewList', 'Got oninput output of: ', output);
        let state = parseState(this.value);
        output.innerHTML = state + ', ' + this.value;
      };
    }
  };
</script>

{#if reviews.reviews && reviews.reviews.length > 0}
  <br />
  <span style="font-size: 18px;" class="white"
    >Showing reviews {reviews.from} to {reviews.from + reviews.reviews.length} of {reviews.stats
      .total} total reviews</span
  ><br />
  <label for="rating-avg" style="font-size: 18px;" class="white"
    >Average Rating: <i class="material-icons">star</i>{Number(
      parseFloat(reviews.stats.average_stars)
    ).toFixed(1)}/10.0</label
  ><br />
  <span class="white">
    <input
      disabled
      id="rating-avg"
      class="slider range-slider"
      type="range"
      name="rating"
      min="0.1"
      max="10"
      value={reviews.stats.average_stars}
      style="width: 100%"
      step="0.1"
      tabindex="-1"
      data-output="rating-desc-avg"
    />
    <p id="rating-desc-avg" />
  </span>
  {#if reviews.user_review}
    <Reviews
      review={reviews.user_review}
      index={-1}
      reply={false}
      targetId={data.user.id}
      targetType={type}
    />
    <hr />
  {/if}
  {#each reviews.reviews as review, index}
    {#if !reviews.user_review || review.id != reviews.user_review.id}
      <article class="review-root review-section">
        <Reviews
          review={review}
          index={index}
          reply={false}
          targetId={data.user.id}
          targetType={type}
        />
      </article>
    {:else}
      <article class="review-root review-section">
        <Reviews
          review={review}
          index={index}
          reply={false}
          targetId={data.user.id}
          targetType={type}
          edittable={false}
        />
      </article>
    {/if}
  {/each}
{/if}
<div class="text-center">
  <nav aria-label="Bot Review Pagination">
    <ul>
      {#if reviewPage > 1}
        <li class="page-item">
          <a href={'#'} class="page-link white" on:click={() => getReviewPage(reviewPage - 1)}
            >Previous</a
          >
        </li>
      {/if}
      {#if reviews.stats}
        {#each Array.from({ length: Math.ceil(reviews.stats.total / reviews.per_page) }, (_, i) => i + 1) as page}
          <li class="page-item" id="page-{page}">
            <a href={'#'} class="page-link white" on:click={() => getReviewPage(page)}>{page}</a>
          </li>
        {/each}
        {#if reviewPage !== Math.ceil(reviews.stats.total / reviews.per_page)}
          <li class="page-item">
            <a href={'#'} class="page-link white" on:click={() => getReviewPage(reviewPage + 1)}
              >Next</a
            >
          </li>
        {/if}
      {/if}
    </ul>
  </nav>
</div>
