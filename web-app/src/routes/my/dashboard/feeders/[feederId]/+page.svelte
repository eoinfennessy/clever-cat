<script>
  export let data;
</script>

<h1 class="text-4xl">{data.feeder.name}</h1>
<p class="text-primary-content">{data.feeder.description}</p>

<div class="divider" />

<div class="card lg:card-side bg-base-100 shadow-xl mt-5">
  <div class="card-body">
    <h2 class="text-2xl">Model</h2>
    <p class="text-primary-content mb-4">{data.model.model}</p>
    <div class="card card-compact w-fit bg-base-200 text-primary-content">
      <div class="card-body">
        <p>Pets this model detects</p>
        {#each data.pets as pet}
          <div class="badge badge-accent">{pet.name}</div>
        {/each}
      </div>
    </div>
  </div>
</div>

<div class="card lg:card-side bg-base-100 shadow-xl mt-5">
  <div class="card-body">
    <h2 class="text-2xl mb-3">Feed Schedules</h2>
    <div class="card card-compact w-52 bg-base-200 text-primary-content">
      <div class="card-body">
        {#each data.feedSchedules as feedSchedule}
          <p class="card-title">Pet Name: {feedSchedule.expand.pet.name}</p>
          <p>Amount to Dispense: {feedSchedule.amount_grams}g</p>
          <p>Feed Frequency: {feedSchedule.frequency_hours} hours</p>
          <div class="card-actions justify-end">
            <button class="btn btn-sm btn-secondary">Edit</button>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>

<div class="card lg:card-side bg-base-100 shadow-xl mt-5">
  <div class="card-body">
    <h2 class="text-2xl mb-3">Last Feeds:</h2>
    <div class="card card-compact w-52 bg-base-200 text-primary-content">
      <div class="card-body">
        {#each data.lastFeeds as lastFeed}
          <p class="card-title">Pet: {lastFeed.items[0].expand.pet.name}</p>
          <p>Time of Last Feed:</p>
          <p>{new Date(lastFeed.items[0].created).toLocaleString()}</p>
          <p>Amount Dispensed: {lastFeed.items[0].grams_dispensed}g</p>
        {/each}
      </div>
    </div>
  </div>
</div>
