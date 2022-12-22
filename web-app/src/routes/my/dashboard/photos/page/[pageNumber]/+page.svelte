<script>
    export let data;

    import { getImageUrl } from '$lib/utils.js'
    import { onMount, onDestroy } from 'svelte';
    import PocketBase from 'pocketbase';

    async function handlePetPhotosEvents(event) {
      console.log(event)
      switch (event.action) {
        case 'create':
          event.record.expand.pet = pb.collection('pets').getOne(event.record.pet)
          data.photos.items = [event.record, ...data.photos.items]
          break;
        case 'update':
          console.log('updated');
          break;
        case 'delete':
          console.log('deleted');
          break;
      }
    }

    let pb;
    let unsubscribe;
    onMount(async () => {
        pb = new PocketBase('https://clever-cat-pb.eoinfennessy.com/')
        pb.authStore.loadFromCookie(data.pb_cookie)
        unsubscribe = await pb.collection(
          'pet_photos').subscribe('*', (event) => handlePetPhotosEvents(event))
    })

    onDestroy(() => unsubscribe?.());
</script>

<div class="flex flex-wrap justify-start gap-5">
  {#each data.photos.items as photo}
    <div class="flex-initial card card-compact w-64 bg-base-100 shadow-xl">
      <figure><img src={getImageUrl(photo.collectionId, photo.id, photo.photo, '256x256')} alt="Pet"/></figure>
      <div class="card-body">
        <p>{photo.expand.pet.name}: {(photo.confidence * 100).toFixed(2)}% confidence</p>
        <div class="card-actions justify-between">
          <button class="btn btn-primary">View</button>
          <button class="btn btn-primary">Tag</button>
        </div>
      </div>
    </div>
  {/each}
</div>

<div class="flex flex-wrap gap-2">
  {#if data.photos.page > 1}
    <div class="mt-10">
      <a href="/my/dashboard/photos/page/{data.photos.page - 1}">
        <button class="btn btn-secondary gap-2">
          <svg class="h-6 w-6 fill-current md:h-8 md:w-8" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"></path>
          </svg>
          Prev.
        </button>
      </a>
    </div>
  {/if}

  {#if data.photos.page < data.photos.totalPages}
    <div class="mt-10">
      <a href="/my/dashboard/photos/page/{data.photos.page + 1}">
        <button class="btn btn-secondary gap-2">
          Next
          <svg class="h-6 w-6 fill-current md:h-8 md:w-8" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"></path>
          </svg>
        </button>
      </a>
    </div>
  {/if}
</div>