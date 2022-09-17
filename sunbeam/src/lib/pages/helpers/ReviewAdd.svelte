<script lang="ts">
  import { browser } from '$app/environment';

  import { page } from '$app/stores';
  import { enums } from '$lib/enums/enums';
  import loadstore from '$lib/loadstore';
  import navigationState from '$lib/navigationState';
  import { addReviewHandler, loginUser } from '$lib/request';
  import { genError } from '$lib/strings';
  import Button from '$lib/base/Button.svelte';

  export let data: any;
  export let type: string;

  async function addReview() {
    $loadstore = 'Adding...';
    $navigationState = 'loading';
    let token = $page.data.token;
    if (!token) {
      loginUser();
      return false;
    }
    let userID = $page.data.user.id;

    let review = document.querySelector('#review-text');
    let starRating = document.querySelector('#star-rating');

    let res = await addReviewHandler(
      data.user.id,
      type,
      null,
      (review as HTMLInputElement).value,
      (starRating as HTMLInputElement).value
    );
    $navigationState = 'loaded';
    if (res.ok) {
      alert({
        id: 'review-add',
        title: 'Review added!',
        message: 'Your review has been added!',
        type: enums.AlertType.Success
      });
      return;
    } else {
      alert({
        id: 'review-add',
        title: 'Error!',
        message: genError(await res.json()),
        type: enums.AlertType.Error
      });
      return;
    }
  }
</script>

<h2>Lets review!</h2>
<label for="rating">On a scale of 1 to 10, how much did you like this {type}?</label><br />
<input
  class="slider range-slider"
  type="range"
  id="star-rating"
  min="0.1"
  max="10"
  style="width: 100%"
  value="5"
  step="0.1"
  data-output="rating-desc"
/>
<p id="rating-desc" style="color: white;" />
<label for="review-text">Enter your review here</label><br />
<textarea
  class="fform"
  id="review-text"
  placeholder="Write your review here. This must be at least 7 characters!"
  minlength="9"
  style="width: 100%; border-radius: 4px 4px 4px 4px;"
  required
/>
<Button href={'#'} onclick={() => addReview()} id="review-add" class="button">Add Review</Button>
