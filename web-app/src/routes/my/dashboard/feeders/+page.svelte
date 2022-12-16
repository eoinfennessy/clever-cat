<script>
    export let data;
    import { getImageUrl } from '$lib/utils.js'
</script>

{#each data.feeders as feeder}
  <div class="card lg:card-side bg-base-100 shadow-xl mb-5">
    <figure><img src={getImageUrl(feeder.collectionId, feeder.id, feeder.thumbnail, '300x300')} alt="Feeder"/></figure>
    <div class="card-body">
      <h2 class="card-title">{feeder.name}</h2>
      <p>{feeder.description}</p>
      <div class="card-actions justify-end">
        <a href="/my/dashboard/feeders/{feeder.id}">
          <button class="btn btn-primary">View Feeder</button>
        </a>
      </div>
    </div>
  </div>
{/each}

<div class="mt-10">
  <a href="/my/dashboard/feeders/new">
    <button class="btn btn-secondary btn-wide gap-2">
      Add a New Feeder
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="white" viewBox="0 0 52 52" stroke="currentColor">
        <path d="M26,0C11.664,0,0,11.663,0,26s11.664,26,26,26s26-11.663,26-26S40.336,0,26,0z M38.5,28H28v11c0,1.104-0.896,2-2,2s-2-0.896-2-2V28H13.5c-1.104,0-2-0.896-2-2s0.896-2,2-2H24V14c0-1.104,0.896-2,2-2s2,0.896,2,2v10h10.5c1.104,0,2,0.896,2,2S39.604,28,38.5,28z"/>
      </svg>
    </button>
  </a>
</div>